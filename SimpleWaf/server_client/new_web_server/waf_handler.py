import requests
import socket
import DB_Wrapper
import json
GET_PREF_CODE = chr(33)
INSERT_ATTACKER_CODE = chr(34)
url_of_waf = "http://127.0.0.1:5000"
def get_log_file_of_web(hostname) -> str:
    headers = {'ACTION':'LOG',
               'WEB_NAME':hostname}
    try:
        response :requests.Response = requests.get(url_of_waf,headers=headers)
    except Exception:
        return 'Error'
    return response.text if response.status_code == 200 else 'Error'
def update_waf_when_new_web(hostname, ip_add):
    headers = {'ACTION': 'NEW_WEB',
               'WEB_NAME': hostname,
               'IP':ip_add}
    try:
        response: requests.Response = requests.get(url_of_waf, headers=headers)
    except Exception:
        return 'Error'
    return response.text if response.status_code == 200 else 'Error'


def update_prefs(json_msg, hostname):
    headers = {
        'ACTION': 'UPDATE_WEB',
        'WEB_NAME': hostname,
        'sql_level': str(json_msg.get("sql_level", "")),
        'xss_defence': str(json_msg.get("xss_defence", "")),
        'hpp_defence': str(json_msg.get("hpp_defence", "")),
        'file_attack_level': str(json_msg.get("file_attack_level", "")),
        'to_send_email': str(json_msg.get("to_send_email", "")),
        'os_level': str(json_msg.get("os_level", "")),
        'port': str(json_msg.get("port", "")),
        'isHttps': str(json_msg.get("isHttps", ""))
    }

    try:
        response: requests.Response = requests.get(url_of_waf, headers=headers)
    except Exception:
        return 'Error'

    return response.text if response.status_code == 200 else 'Error'


def get_log_file_of_admin_all_webs() ->str:
    headers = {'ACTION': 'ADMIN_LOG'}
    try:
        response: requests.Response = requests.get(url_of_waf, headers=headers)
    except Exception:
        return 'Error'
    return response.text if response.status_code == 200 else 'Error'


def insert_attacker(ip_address,free_date):
    pass
def check_if_msg_from_waf(msg:str) -> bool:
    if len(msg) < 4:
        return False
    codemsg = msg[0]

    if codemsg != GET_PREF_CODE:
        return False
    try:
        data = json.loads(msg[1:])
        if data['key'] != 'THIS IS WAF':
            return False
    except Exception as e:
        return False
    return True
def handle_waf(sock,msg:str):
    code_msg = msg[0]
    if code_msg == GET_PREF_CODE:
        send_pref(sock)
def getting_data():
    WEBSITES_IP = 'websites_ip'
    WEBSITE_LOGIN = 'website_login'
    ATTACKERS = 'attackers'
    ATTACKERS_SCORE = 'attackers_score'
    PREFERENCES = 'preferences'
    data_dict = {}
    data_dict[WEBSITES_IP] = {}
    webs_info = DB_Wrapper.get_table_values(WEBSITES_IP)
    for curr_web in webs_info:
        host_name:str = curr_web[0]
        host_name = host_name.lower()
        ip_add:str = curr_web[1]
        data_dict[WEBSITES_IP][host_name] = ip_add

    data_dict[PREFERENCES] = {}
    prefs = DB_Wrapper.get_table_values(PREFERENCES)
    for curr_pref in prefs:
        host_name:str = curr_pref[0]
        host_name = host_name.lower()
        # for better lookup time in runtime #
        data_dict[PREFERENCES][host_name] = curr_pref

    ### the attackers dict will contain the key ip and value free date
    data_dict[ATTACKERS] = {}
    # those will be kept as normal dict
    attackers_data = DB_Wrapper.get_table_values(ATTACKERS)
    for data_cell in attackers_data:
        attacker_ip = data_cell[0]
        if attacker_ip == "127.0.0.1":
            continue#todo remove in production
        attacker_freedate = data_cell[1]
        str_attacker_free_date = attacker_freedate.strftime("%Y-%m-%d")
        data_dict[ATTACKERS][attacker_ip] = str_attacker_free_date
    return json.dumps(data_dict)
def send_pref():
    return getting_data()
