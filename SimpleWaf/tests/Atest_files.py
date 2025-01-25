import requests
import before_tests
from before_tests import *

@before_test
def t1_est_real_file():
    """this for testing in real world - when try this - put in routing.py line 79(for now):
     new_url = f"https://{website_ip}:/{path}" """
    host_name = "mysite.com"
    headers = {
        "Host": host_name
    }
    ### open in bin -rb and not r ###
    with open('exampleFile.txt', 'rb') as f:
        # Prepare the file to be uploaded
        files = {
            'file': ('exampleFile.txt', f, 'text/plain'),
            'fil e2': ('exampleFile.pdf', f, 'text/plain')
        }
        data = {
            'user': '123',
            'pass': 'hello'
        }
        #files = {'file': f}
        response = requests.post(url, headers=headers,files=files,data=data)
    print(response)
    assert response.status_code == WEBSITE_NOT_RESPONDING_CODE

@before_test
def t2_est_mal_file():
    """this for testing in real world - when try this - put in routing.py line 79(for now):
     new_url = f"https://{website_ip}:/{path}" """
    host_name = "mysite.com"
    headers = {
        "Host": host_name
    }
    ### open in bin -rb and not r ###
    with open('exampleFile.txt', 'rb') as f:
        # Prepare the file to be uploaded
        files = {
            'file': ('exampleFile.txt', f, 'text/plain'),
            'fil e2': ('exampleFile.php', f, 'text/plain')
        }
        data = {
            'user': '123',
            'pass': 'hello'
        }
        #files = {'file': f}
        response = requests.post(url, headers=headers,files=files,data=data)
    print(response)
    assert response.status_code == ATTACK_FOUND_CODE
def activate_all_tests():
    #t1_est_real_web()
    t1_est_real_file()
    t2_est_mal_file()
if __name__ == '__main__':
    activate_all_tests()