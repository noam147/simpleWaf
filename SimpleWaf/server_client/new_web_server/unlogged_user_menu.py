import DB_Wrapper

ADD_USER_MSG_CODE = chr(1)
ADD_WEBSITE_MSG_CODE = chr(2)
LOGIN_CODE = chr(3)

def add_user(json_msg) -> tuple[bool,str]:
    ### bool is result if went good, str is an explnation of what happend wrong###
    try:
        host_name = json_msg["host_name"]
        username = json_msg["username"]
        password = json_msg["password"]
        email = json_msg["email"]
    except Exception:
        return False,"msg is corrupted, check json values"
    if not DB_Wrapper.get_if_host_name_exist(host_name):
        return False,"Error with host_name, sign up your website before."
    if DB_Wrapper.check_if_username_exist_in_website_login(username):
        return False, "username already existing."
    if DB_Wrapper.insert_into_website_login(host_name,username,password,email):
        return True,""
    return False,"error with db"
def is_valid_ip(ip_add:str) -> bool:
    """when inserting ip func will check if ip is a real ip"""
    parts = ip_add.split(".")
    # we will take just ipv4 for now
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit():
            return False
        num = int(part)
        if num < 0 or num > 255:
            return False
       #for zeros at start like 01
        if part != str(num):
            return False
    return True
def add_website(json_msg) -> tuple[bool,str]:
    try:
        print(json_msg)
        host_name:str = json_msg["host_name"]
        ip_add = json_msg["ip_add"]
    except Exception:
        return False, "msg is corrupted, check json values"
    host_name = host_name.lower()#to prevent mismtach in capitals.
    if not is_valid_ip(ip_add):
        return False, "ip address is not supported."
    if DB_Wrapper.get_if_ip_exist(ip_add):
        return False, "ip already exist in WAF lists."
    if DB_Wrapper.get_if_host_name_exist(host_name):
        return False, "host name already exist in WAF lists."
    DB_Wrapper.special_insert_or_update_website_ip(host_name, ip_add)
    from waf_handler import update_waf_when_new_web
    update_waf_when_new_web(host_name,ip_add)
    return True,""
def login(json_msg) -> tuple[bool,str]:
    try:
        username = json_msg["username"]
        password = json_msg["password"]
    except Exception:
        return False,"msg is corrupted, check json values"
    if DB_Wrapper.verify_login_into_website_login(username, password):
        return True,username
    return False,"login failed"
