import json
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler, HTTPError, stream_request_body
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPResponse, httputil
from tornado.escape import json_decode
import DB_Wrapper
from urllib.parse import urlparse, urlencode
import slow_loris_detect
from SearchAttackHelper import SearchAttacks
from vars_for_global_use import *
from typing import Any, Optional, Awaitable
from collections import defaultdict
import time
import logger
import inspect
PORT_APP = 5000
EXAMPLE_WEBSITE_PORT = 5001


@stream_request_body
class WAFRequestHandler(RequestHandler):
    def initialize(self, connections, chunk_timeout_handles, connection_timeout_handles):
        self.connections = connections
        self.chunk_timeout_handles = chunk_timeout_handles
        self.connection_timeout_handles = connection_timeout_handles
        self._finished = False

    async def _see_params(self):
        """
        prints request details.
        used for debugging.
        """
        print(f"raw data: {self.request.body}")
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            json_data = json_decode(self.request.body)
            print(f"JSON Data: {json_data}")

        print(f"Files: {self.request.files}")
        user_ip = self.request.remote_ip
        print(f"User IP: {user_ip}")

    def is_attacker(self, ip_add):
        return DB_Wrapper.is_ip_blocked(ip_add)


    def send_empty_msg_with_code(self, code):
        if not self._finished:
            self.set_status(code)
            self.finish()
            self._finished = True
            self._finished = True

    async def stop_connections_for_ip(self, ip_address):
        """
        Stop all active connections for a specific IP address by sending a response
        and clearing associated resources.
        """
        if ip_address not in self.connections:
            return

        # Iterate through all connections for this IP and close them
        for connection in self.connections[ip_address]:
            try:
                connection.set_status(ATTACK_FOUND_CODE)  # Service Unavailable
                connection.finish("Your connections were terminated due to suspicious activity.")
            except Exception as e:
                print(f"Error finishing connection for IP {ip_address}: {e}")

        # Clear the connection timeouts
        if ip_address in self.connection_timeout_handles:
            IOLoop.current().remove_timeout(self.connection_timeout_handles[ip_address])
            del self.connection_timeout_handles[ip_address]

        # Clear the chunk timeouts
        if ip_address in self.chunk_timeout_handles and self.chunk_timeout_handles[ip_address]:
            IOLoop.current().remove_timeout(self.chunk_timeout_handles[ip_address])
            del self.chunk_timeout_handles[ip_address]

        # Remove the connections for this IP
        del self.connections[ip_address]

    def prepare(self):
        ip_address = self.request.remote_ip

        # add timeout to the connection
        self.connection_timeout_handles[ip_address] = IOLoop.current().add_timeout(
            time.time() + slow_loris_detect.MAX_CONNECTION_TIME,
            lambda: self.send_empty_msg_with_code(ATTACK_FOUND_CODE)
        )

        # Add the current connection to the active connections list
        connection = self
        self.connections[ip_address].append(connection)

        # search slow loris
        if not slow_loris_detect.check_connection(len(self.connections[ip_address])):
            print(f"detected too many connections, connections: {self.connections}")
            IOLoop.current().add_callback(self.stop_connections_for_ip, ip_address)
            self.send_empty_msg_with_code(ATTACK_FOUND_CODE)

    async def forward_request(self, new_url, method, body=None, headers=None):
        client = AsyncHTTPClient()
        try:
            request = HTTPRequest(
                url=new_url,
                method=method,
                body=body,
                headers=headers or {}
            )
            response = await client.fetch(request, raise_error=False)
            return response
        except Exception as e:
            print(f"Error forwarding request: {e}")
            return None

    async def prepare_request(self, path):
        ip_address = self.request.remote_ip

        # all data was transferred therefor canceling the connection timeout
        if ip_address in self.connection_timeout_handles:
            IOLoop.current().remove_timeout(self.connection_timeout_handles[ip_address])

        # Check if user is an attacker
        if self.is_attacker(ip_address):
            print("Attacker found!")
            self.send_empty_msg_with_code(ATTACKER_CODE)
            return

        # Get website IP from DB
        host_name = urlparse(self.request.full_url()).hostname
        website_ip = DB_Wrapper.get_ip_address_by_host_name(host_name)
        if not website_ip or website_ip == DB_Wrapper.ERROR_IP_ADDRESS:
            print("Website does not exist")
            self.send_empty_msg_with_code(WEBSITE_NOT_EXIST_CODE)
            return

        # For debug
        # await self._see_params()

        # Check for attacks
        current = SearchAttacks(self.request)
        if current.search_attacks():
            self.send_empty_msg_with_code(ATTACK_FOUND_CODE)
            return

        # Construct the target URL
        new_url = f"{self.request.protocol}://{website_ip}:{EXAMPLE_WEBSITE_PORT}/{path}"
        # For production: new_url = f"{self.request.protocol}://{website_ip}/{path}"
        if self.request.query_arguments:
            query_string = urlencode({k: v[0].decode() for k, v in self.request.query_arguments.items()})
            new_url = f"{new_url}?{query_string}"

        return new_url

    async def get(self, path):
        new_url = await self.prepare_request(path)
        if new_url:
            response = await self.forward_request(new_url, "GET", headers=self.request.headers)
            if not response:
                self.send_empty_msg_with_code(WEBSITE_NOT_RESPONDING_CODE)
                return
            self.set_status(response.code)
            self._write_response(response)

    async def post(self, path):
        new_url = await self.prepare_request(path)
        if new_url:
            response = await self.forward_request(new_url, "POST", body=self.request.body, headers=self.request.headers)
            if not response:
                self.send_empty_msg_with_code(WEBSITE_NOT_RESPONDING_CODE)
                return
            self.set_status(response.code)
            self._write_response(response)

    def data_received(self, chunk: bytes):
        ip_address = self.request.remote_ip

        # Check if the chunk size is too small
        if not slow_loris_detect.check_chunk(len(chunk)):
            print(f"Blocked a tiny message from IP {ip_address}")
            self.send_empty_msg_with_code(ATTACK_FOUND_CODE)
            if self.request.connection.stream:
                self.request.connection.stream.close()
            return

        # Cancel any existing timeout handles for this IP if a valid chunk was received
        if ip_address in self.chunk_timeout_handles and self.chunk_timeout_handles[ip_address]:
            IOLoop.current().remove_timeout(self.chunk_timeout_handles[ip_address])

        # Set a new timeout for the next chunk
        self.chunk_timeout_handles[ip_address] = IOLoop.current().add_timeout(
            time.time() + slow_loris_detect.MAX_TIME_BETWEEN_CHUNKS,
            lambda: self.send_empty_msg_with_code(ATTACK_FOUND_CODE)
        )

        # Append the chunk to the request body
        self.request.body += chunk

    def on_finish(self):
        ip_address = self.request.remote_ip

        # Clear connection timeout
        if ip_address in self.connection_timeout_handles:
            IOLoop.current().remove_timeout(self.connection_timeout_handles[ip_address])
            del self.connection_timeout_handles[ip_address]

        # Clear chunk timeout
        if ip_address in self.chunk_timeout_handles and self.chunk_timeout_handles[ip_address]:
            IOLoop.current().remove_timeout(self.chunk_timeout_handles[ip_address])
            del self.chunk_timeout_handles[ip_address]

        # Remove the connection from connections
        if ip_address in self.connections:
            if self in self.connections[ip_address]:
                self.connections[ip_address].remove(self)
            if not self.connections[ip_address]:
                del self.connections[ip_address]

    def _write_response(self, response: HTTPResponse):
        if not self._finished:
            for header, value in response.headers.get_all():
                if header.lower() not in ("content-length", "transfer-encoding", "content-encoding"):
                    self.set_header(header, value)
            self.write(response.body)
            self.finish()
            self._finished = True
        #defend clickjacking:
        #wrong way:
        #self.request.headers["X-Frame-Options"] = "SAME-ORIGIN"
        #this is the msg from the client to the server, we want the msg from server to client thus:
        #right way:
        self.set_header("X-Frame-Options", "SAMEORIGIN")





def make_app():
    connections = defaultdict(list)
    connection_timeout_handles = defaultdict(lambda: None)
    chunk_timeout_handles = defaultdict(lambda: None)

    return Application([
        (r"/(.*)", WAFRequestHandler,
         dict(connections=connections, connection_timeout_handles=connection_timeout_handles,
              chunk_timeout_handles=chunk_timeout_handles)),
    ])


if __name__ == "__main__":
    import DDOS_Scanner
    DDOS_Scanner.DDOSScanner.activate_at_start()
    DB_Wrapper.db_config ={
        "host": "localhost",
        "user": "root",
        "password": "guytu0908",
        "database": "wafDataBase"
    }
    app = make_app()
    app.listen(PORT_APP)
    print(f"Running Tornado app on port {PORT_APP}")
    IOLoop.current().start()
