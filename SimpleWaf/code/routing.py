import json
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler, HTTPError
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPResponse
from tornado.escape import json_decode
import DB_Wrapper
from urllib.parse import urlparse, urlencode
from SearchAttackHelper import SearchAttacks
from vars_for_global_use import *
from typing import Any

PORT_APP = 5000
EXAMPLE_WEBSITE_PORT = 5001


class WAFRequestHandler(RequestHandler):
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
        self.set_status(code)
        self.finish()

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
        # Check if user is an attacker
        ip_address = self.request.remote_ip
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

    def _write_response(self, response: HTTPResponse):
        for header, value in response.headers.get_all():
            if header.lower() not in ("content-length", "transfer-encoding", "content-encoding"):
                self.set_header(header, value)
        self.write(response.body)


def make_app():
    return Application([
        (r"/(.*)", WAFRequestHandler),
    ])


if __name__ == "__main__":
    import DDOS_Scanner
    DDOS_Scanner.DDOSScanner.activate_at_start()
    """DB_Wrapper.db_config ={
        "host": "localhost",
        "user": "root",
        "password": "guytu0908",
        "database": "wafDataBase"
    }"""
    app = make_app()
    app.listen(PORT_APP)
    print(f"Running Tornado app on port {PORT_APP}")
    IOLoop.current().start()
