import os
from tornado.httputil import HTTPServerRequest
from tornado.httpclient import HTTPResponse,HTTPRequest
from io import BytesIO
import socket
SERVER_IP = '127.0.0.1'
SERVER_PORT = 47777
def check_if_msg_from_server(data:HTTPServerRequest) -> bool:
    #todo make better checking, now this is weak...
    server_header = data.headers.get('WEB_NAME')
    if server_header:
        return True
    return False

def get_req_with_code(data:HTTPServerRequest,body:str,code=200):
    return HTTPResponse(
        request=HTTPRequest(data.full_url()),
        code=code,
        buffer=BytesIO(body.encode("utf-8")),
        request_time=data.request_time()
    )
def handle_server_msg(data:HTTPServerRequest):
    action = data.headers.get('ACTION')
    if not action:
        return get_req_with_code(data,'ERROR',403)
    if action == 'LOG':
        return send_log_file(data)
    return get_req_with_code(data,'ERROR',404)
def send_log_file(data:HTTPServerRequest):
    #with http probably. at server it will send one
    host_name = data.headers.get('WEB_NAME')
    if not host_name:
        return get_req_with_code(data, "Error", 401)
    host_name = host_name.replace("/","")
    host_name = host_name.replace("\\","")
    file_path = "logs/outer/"+host_name
    if os.path.exists(file_path):
        with open(file_path,"r") as f:
            log_content: str = f.read()

    else:
        return get_req_with_code(data, "Error", 402)
    return get_req_with_code(data, log_content)
def get_prefs() -> None:
    #todo activate this func with while True loop.
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((SERVER_IP,SERVER_PORT))
            sock.sendall(chr(33)+"{'key':'THIS IS WAF'}\n")
            data = sock.recv(2056)
            data = data.decode('utf-8')
            #todo prase the data into memory handler
    except Exception as e:
        print('ho no. can not get prefs of websites. PLEASE ACTIVATE THE SERVER')

