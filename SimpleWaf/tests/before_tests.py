import sys
sys.path.append('../code')
import DB_Wrapper
from vars_for_global_use import *
WAF_IP_ADDRESS = "127.0.0.1"
PORT = 3333
url = f"http://{WAF_IP_ADDRESS}:{PORT}"
def before_test(func):
    ### decorator func ###
    def wrapper(*args, **kwargs):
        ### reset the ip of loopback ###
        DB_Wrapper.delete_attacker("127.0.0.1")
        return func(*args, **kwargs)  # Execute the wrapped function
    return wrapper