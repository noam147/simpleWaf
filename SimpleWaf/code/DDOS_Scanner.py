import time
import threading
from Attack_Scanner import IAttack_Scanner
import requests
from tornado.httputil import HTTPServerRequest
"""method of find attack - get a dict that saves - ip_add with number of requests, if goes over N requests - this is ddos"""
"""will be a scanner each second to clear the dict"""
class DDOSScanner(IAttack_Scanner):
    _MAX_NUMBER_OF_REQUESTS_PER_SECOND = 15
    _ip_addresses_and_amount_of_requests:dict = {}
    _lock = threading.Lock()#for thread clearing the dict
    @staticmethod
    def _clear_scan():
        """func will clear the dict - use lock to prevent inserting/updating dict at same time"""
        with DDOSScanner._lock:
            DDOSScanner._ip_addresses_and_amount_of_requests.clear()
    @staticmethod
    def activate_at_start():
        t = threading.Thread(target=DDOSScanner.__thread_clear_scan,daemon=True)
        t.start()
    @staticmethod
    def __thread_clear_scan():
        while True:
            time.sleep(1)
            DDOSScanner._clear_scan()

    @staticmethod
    def scan(data: HTTPServerRequest) -> bool:
        try:
            ip_address = data.remote_ip
            #ip_address = data.environ['REMOTE_ADDR']
        except Exception:
            print("can")
            return True#if we can't accsess the ip - this is an attacker
        with DDOSScanner._lock:
            ### insert ip to dict ###
            if ip_address not in DDOSScanner._ip_addresses_and_amount_of_requests:
                #if ip not in the dict
                DDOSScanner._ip_addresses_and_amount_of_requests[ip_address] = 1
            else:
                DDOSScanner._ip_addresses_and_amount_of_requests[ip_address] += 1
            ### check if ip passed the limit of requests per second ###
            if DDOSScanner._ip_addresses_and_amount_of_requests[ip_address] > DDOSScanner._MAX_NUMBER_OF_REQUESTS_PER_SECOND:
                print("attackerrrrr, ip= "+ip_address)
                return True
            return False


def check_ddos():
    response = requests.get("https://kidum-me.com/")
    fake_ip = '11.1.1.1'
    headers = {'X-Forwarded-For': fake_ip}
    exmple_req = requests.Request(method="get",headers=headers)
    while True:
        DDOSScanner.scan(exmple_req)
def check2():
    from unittest.mock import Mock
    import requests

    # Create a mock for your 'data' object to simulate a WSGI-like request environment
    mock_data = Mock()
    mock_data.environ = {'REMOTE_ADDR': '11.1.1.1'}  # Set the IP address here

    # Your request object would look like this (request is from the requests library, not WSGI)
    exmple_req = requests.Request(method="GET", headers={"ip_src": "11.1.1.1"})
    exmple_req.environ = mock_data.environ
    while True:
        DDOSScanner.scan(exmple_req)

