from werkzeug.serving import WSGIRequestHandler, run_simple
import socket


class SlowLorisProtectedHandler(WSGIRequestHandler):
    def handle(self):
        self.request.settimeout(5)  # Timeout in seconds for headers
        try:
            super().handle()
        except socket.timeout:
            print("Connection timed out while waiting for headers")
            self.close_connection = True


if __name__ == "__main__":
    from my_flask_app import app
    run_simple('127.0.0.1', 5000, app, request_handler=SlowLorisProtectedHandler)
