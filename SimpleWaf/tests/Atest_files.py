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
    return response.status_code == WEBSITE_NOT_RESPONDING_CODE

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
    return response.status_code == ATTACK_FOUND_CODE

@before_test
def t3_est_mal_file_with_changing_format():
    """after checks - when the boundary is not exactly the same - the requests does not take the argument with the bad boundary"""
    """after check - the attribute filename= is really the one who indicating that the var is file"""
    """after check - if the filename contains any \" signs - the requests lib just ignores is"""

    host_name = "mysite.com"
    boundary = "--06303c6fe430409dd45ac2224feebd3b"
    url = "http://127.0.0.1:3333"
    headers = {
        "Host": host_name,
        "Content-Type": f"multipart/form-data; boundary={boundary[2:]}"
    }
    file_content = open("exampleFile.txt", "rb").read()
    raw_body = (
        f"{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"user\"\r\n\r\n"
        f"123\r\n"
        f"{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"pass\"\r\n\r\n"
        f"hello\r\n"
        f"{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"file\"; filename=\"exampleFile.txt\"\r\n"
        f"Content-Type: text/plain\r\n\r\n"
        f"{file_content.decode('utf-8')}\r\n"
        f"{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"file2\"; filename=\"a\"a\"a\"\r\n"
        f"Content-Type: text/plain\r\n\r\n"
        f"{file_content.decode('utf-8')}\r\n"
        f"{boundary}--"
    )
    response = requests.post(url, headers=headers, data=raw_body)
    print(response)

def activate_all_tests():
    import time
    #t1_est_real_web()

    #t1_est_real_file()
    #t2_est_mal_file()

    t3_est_mal_file_with_changing_format()
if __name__ == '__main__':
    print("hiiii")
    activate_all_tests()
print("wow..")