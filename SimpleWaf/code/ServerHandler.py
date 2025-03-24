import os
from tornado.httputil import HTTPServerRequest
from tornado.httpclient import HTTPResponse,HTTPRequest
from io import BytesIO
import requests
from logger import _OuterLogger,_InnerLogger
import memory_handler
import json
SERVER_IP = '127.0.0.1'
SERVER_PORT = 47777
get_db_rout = "data_base"
alert_attacker_rout = "attacker_alert"
def check_if_msg_from_server(data:HTTPServerRequest) -> bool:
    #todo make better checking, now this is weak...
    server_header = data.headers.get('ACTION')
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
    print(action)
    if not action:
        return get_req_with_code(data,'ERROR',403)
    if action == 'LOG':
        return send_log_file(data)
    if action == 'ADMIN_LOG':
        print("need to send log")
        return send_admin_log_file(data)
    return get_req_with_code(data,'ERROR',404)
def send_log_file(data:HTTPServerRequest):
    #with http probably. at server it will send one
    host_name:str = data.headers.get('WEB_NAME')
    if not host_name:
        return get_req_with_code(data, "Error", 401)
    host_name = host_name.replace("/","")
    host_name = host_name.replace("\\","")
    log_content = _OuterLogger().get_logged_data(host_name)
    if not log_content:
        return get_req_with_code(data, "Error", 402)
    return get_req_with_code(data, log_content)
def get_prefs() -> bool:
    url = f"http://{SERVER_IP}:{SERVER_PORT}/{get_db_rout}"
    headers_for_auth = {'Key':'THIS IS WAF'}
    try:
        response = requests.get(url,headers=headers_for_auth)
        memory_handler.data_dict = json.loads(response.text)
    except Exception as e:
        return False
    return True
def alert_attacker(ip_add:str,free_date:str,host_name_attacked:str, attack:str):
    url = f"http://{SERVER_IP}:{SERVER_PORT}/{alert_attacker_rout}?ip={ip_add}&free_date={free_date}&hostname={host_name_attacked}&attack={attack}"
    headers_for_auth = {'Key': 'THIS IS WAF'}
    try:
        response = requests.get(url, headers=headers_for_auth)
    except Exception as e:
        pass


def send_admin_log_file(data:HTTPServerRequest):
    log_content = _InnerLogger().get_logged_data()
    if not log_content:
        return get_req_with_code(data, "Error", 402)
    return get_req_with_code(data, log_content)