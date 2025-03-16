from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler, HTTPError, stream_request_body
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPResponse, httputil
from tornado.escape import json_decode
import DB_Wrapper
from urllib.parse import urlparse, urlencode

import Preferences_Items
from XSS_Prevent import XSS_Preventer
import slow_loris_detect
from SearchAttackHelper import SearchAttacks
from vars_for_global_use import *
from collections import defaultdict
import time
from datetime import datetime
import logger
from Preferences import Preferences
import urllib.parse
import socket
from io import BytesIO
import memory_handler
import ServerHandler
from SQLI_Prevnter import SQLI_Preventer
PORT_APP = 5000


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
        ### for testing ###
        #if ip_add == "127.0.0.1":
        #    return False
        return memory_handler.get_is_ip_attacker(ip_add)

    def alert_to_logger(self, host_name: str, ip_attacker: str, attack_method: str):
        l = logger.Logger()
        current_formatted_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        timeout = str(DB_Wrapper.calc_days_until_free_for_attack(ip_attacker))
        timeout += "d"#add the d for days
        data = logger.LogInfo(host_name, ip_attacker, attack_method, timeout, current_formatted_time)
        l.log(data)
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

            self.alert_to_logger(self.request.host_name, ip_attacker=ip_address, attack_method="SLOW_LORIS")
            DB_Wrapper.when_find_attacker(ip_address)


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
        except socket.error as e:
            print("Error forwarding request: website is not reachable")
        except Exception as e:
            print(f"Error forwarding request: {e}")
            return None

    async def prepare_request(self, path):

        ### this for checking if msg came from Server and not from regular client ###
        if ServerHandler.check_if_msg_from_server(self.request):
            print('msg from server detected')
            respond = ServerHandler.handle_server_msg(self.request)
            print(respond)
            self._write_response(respond)
            return

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

        website_ip = memory_handler.get_ip_by_host_name(host_name)
        #website_ip = DB_Wrapper.get_ip_address_by_host_name(host_name.decode())
        if not website_ip:
            print("Website does not exist")
            self.send_empty_msg_with_code(WEBSITE_NOT_EXIST_CODE)
            return

        # For debug
        # await self._see_params()

        ### need optimazation - to not fetch from db each time... ###
        pref_of_host_name_in_memory = Preferences.get_preferences_of_website(host_name)
        if pref_of_host_name_in_memory == None:
            pref_of_host_name_in_memory = Preferences.get_generic_prefs(host_name)
        # Check for attacks
        current = SearchAttacks(self.request)
        name_of_attack = current.search_attacks(pref_of_host_name_in_memory)
        if name_of_attack == "":#if there is no attack
            pass
        else:#if there was an attack
            #alert db

            ### todo - send to the server the creds of attacker so that the serve can save it in his db
            #DB_Wrapper.when_find_attacker(ip_address)

            free_date = DB_Wrapper.calc_attacker_free_date(ip_address,1)
            memory_handler.data_dict[memory_handler.ATTACKERS][ip_address] = free_date

            #alert logger
            self.alert_to_logger(host_name, ip_attacker=ip_address, attack_method=name_of_attack)
            #abort request
            self.send_empty_msg_with_code(ATTACK_FOUND_CODE)
            return
        ### replace the xss and sql todo check with prefrences before###
        self.request = XSS_Preventer.edit_request(self.request)
        self.request = SQLI_Preventer.edit_request(self.request)
        ### need optimazation - to not fetch from db each time... ###
        pref_of_host_name_in_memory = memory_handler.get_prefs_of_web(host_name)
        #memory_handler.data_dict[Preferences]
        if pref_of_host_name_in_memory == None:
            print("NEED TO ENTER PREF FOR THIS WEB: "+host_name)
            new_url = f"https://{website_ip}/{path}"
        else:
            #fetching from db:
            #pref_of_host_name_from_db = DB_Wrapper.get_preferences_by_host_name(host_name)
            if pref_of_host_name_in_memory.isHttps:
                new_url = "https://"
            else:
                new_url = "http://"
            new_url+= f"{website_ip}:{pref_of_host_name_in_memory.port}/{path}"


        if self.request.query_arguments:
            query_string = urlencode({k: v[0].decode() for k, v in self.request.query_arguments.items()})
            new_url = f"{new_url}?{query_string}"


        ### for non aski characters in a url (like chrs in hebrew)###
        new_url = urllib.parse.quote(new_url, safe=":/")

        return new_url

    async def get(self, path):
        new_url = await self.prepare_request(path)

        if new_url:
            response = await self.forward_request(new_url, "GET", headers=self.request.headers)
            if not response:
                self.send_empty_msg_with_code(WEBSITE_NOT_RESPONDING_CODE)
                return

            #response.headers.add("X-CSRFToken", self.xsrf_token)
            new_response_body = response.body  # Keep binary data unchanged


            modified_response = HTTPResponse(
                request=HTTPRequest(response.effective_url),
                code=response.code,
                headers=httputil.HTTPHeaders(response.headers),
                buffer=BytesIO(new_response_body if isinstance(response.body, bytes) else new_response_body.decode()),  # New response body
                request_time=response.request_time
            )
            self.set_status(response.code)
            self._write_response(modified_response)

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
        host_name = urlparse(self.request.full_url()).hostname
        # Check if the chunk size is too small
        if not slow_loris_detect.check_chunk(len(chunk)):
            print(f"Blocked a tiny message from IP {ip_address}")
            self.send_empty_msg_with_code(ATTACK_FOUND_CODE)
            self.alert_to_logger(host_name.decode() if isinstance(host_name,bytes) else host_name,ip_address,"Slow_Loris")
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
    def add_clickjacking_defence(self,response: HTTPResponse):
        ##### CLICKJACKING #####
        ### this is old header that sometimes does not work ###
        response.headers.add("X-Frame-Options", "SAMEORIGIN")
        ### this is the new and imporved header that really work ###
        response.headers.add("Content-Security-Policy", "frame-ancestors 'self';")

    def _write_response(self, response: HTTPResponse):
        self.add_clickjacking_defence(response)
        if not self._finished:
            for header, value in response.headers.get_all():
                if header.lower() not in ("content-length", "transfer-encoding", "content-encoding"):
                    self.set_header(header, value)
            if response.code != 304:
                ### in 304 we do not have a body ###
                self.write(response.body)
            self.finish()
            self._finished = True




def make_app():
    connections = defaultdict(list)
    connection_timeout_handles = defaultdict(lambda: None)
    chunk_timeout_handles = defaultdict(lambda: None)
    settings = {
        "xsrf_cookies": False,
    }
    return Application([
        (r"/(.*)", WAFRequestHandler,
         dict(connections=connections, connection_timeout_handles=connection_timeout_handles,
              chunk_timeout_handles=chunk_timeout_handles)),
    ], **settings)
def get_prefs_from_server():
    while True:
        if ServerHandler.get_prefs():
            return
        print("activate Server")
        time.sleep(4)

if __name__ == "__main__":
    get_prefs_from_server()

    import DDOS_Scanner
    DDOS_Scanner.DDOSScanner.activate_at_start()
    """DB_Wrapper.db_config = {
        "host": "localhost",
        "user": "root",
        "password": "guytu0908",
        "database": "wafDataBase"
    }"""

    app = make_app()
    app.listen(PORT_APP)
    print(f"Running Tornado app on port {PORT_APP}")
    IOLoop.current().start()
