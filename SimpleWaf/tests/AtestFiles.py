

###delte this code when merged ###
import sys
sys.path.append('../code')
import DB_Wrapper
import requests
from vars_for_global_use import *
WAF_IP_ADDRESS = "127.0.0.1"
PORT = 5000
url = f"http://{WAF_IP_ADDRESS}:{PORT}"
def before_test(func):
    ### decorator func ###
    def wrapper(*args, **kwargs):
        ### reset the ip of loopback ###
        DB_Wrapper.delete_attacker("127.0.0.1")
        return func(*args, **kwargs)  # Execute the wrapped function
    return wrapper
### until HERE ###

### todo undo the comment when the files branch will be merged!!! ###
#from before_tests import *

@before_test
def t1est_file_traversal():
    print("File Traversal Test:")

    mal_img = "..%2f..%2f..%2f..%2fetc%2fpsswd"
    url_to_send = f"http://phisherWeb.com:{PORT}/imgs/{mal_img}"
    response = requests.get(url_to_send)
    if response.status_code == ATTACK_FOUND_CODE:
        print("test passed!")
    else:
        print("test failed! got code:"+str(response.status_code))

def main():
    t1est_file_traversal()
if __name__ == '__main__':
    main()