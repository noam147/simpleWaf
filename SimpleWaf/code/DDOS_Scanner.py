import time
import threading
from Attack_Scanner import IAttack_Scanner
import requests
from tornado.httputil import HTTPServerRequest
"""method of find attack - get a dict that saves - ip_add with number of requests, if goes over N requests - this is ddos"""
"""will be a scanner each second to clear the dict"""

# new method is to see when webs gets 'full' -
# we will create a dict of web and amount of msgs
# each scan will take 5 minutes until reset

# maybe the ddos scan will output diffrent things based on condition:
# available conditions:
# 1. Do not pass msg to server but do not block user (if the web is in full mode)
# 2. Block user for a dat or something (do not sure when we actually want to block...)
TIME_OF_SCAN_ON_MINUTES = 5
NUM_ALLOWED_REQUESTS_PER_MIN = 100
NUM_REQUESTS_UNTIL_WEB_FULL = TIME_OF_SCAN_ON_MINUTES * NUM_ALLOWED_REQUESTS_PER_MIN
class DDOSScanner(IAttack_Scanner):
    _MAX_NUMBER_OF_REQUESTS_PER_SECOND = 100
    _ip_addresses_and_amount_of_requests:dict = {}
    _webs_and_msgs:dict = {} #value- hostname:str; key- number of msgs to this hostname
    ### there is GIL in cpython and thus we do not need to be afraid to insert to dict even though we use detach threads

    @staticmethod
    def _clear_scan():
        """func will clear the dict - use lock to prevent inserting/updating dict at same time"""
        DDOSScanner._ip_addresses_and_amount_of_requests.clear()
    @staticmethod
    def activate_at_start():
        t = threading.Thread(target=DDOSScanner.__thread_clear_scan,daemon=True)
        t.start()
    @staticmethod
    def __thread_clear_scan():
        while True:
            time.sleep(TIME_OF_SCAN_ON_MINUTES*60)
            DDOSScanner._clear_scan()

    @staticmethod
    def is_zipbomb_msg(data: HTTPServerRequest) -> bool:
        """func check if content is more than 10mb"""
        return len(data.body) > 1000 * 1024 * 1024 * 3 # 3gb in bytes

    @staticmethod
    def is_big_msg(data: HTTPServerRequest) -> bool:
        """func check if content is more than 10mb"""
        return len(data.body) > 10 * 1024 * 1024  # 10mb in bytes

    @staticmethod
    def scan(data: HTTPServerRequest) -> bool:
        try:
            ip_address = data.remote_ip
            host_name = data.host_name
        except Exception:
            return True#if we can't accsess the ip - this is an attacker
        if DDOSScanner.is_zipbomb_msg(data.body):
            return True#if the msg is above the really big size - this is an attack

        ### there is GIL in cpython and thus we do not need to be afraid to insert to dict even though we use detach threads

        if host_name not in DDOSScanner._webs_and_msgs:
            ### maybe insert also the ip or something, but probably general dict of ip will do the job
            DDOSScanner._webs_and_msgs[host_name] = 1
        else:
            DDOSScanner._webs_and_msgs[host_name] += 1
        if DDOSScanner._webs_and_msgs[host_name] > NUM_REQUESTS_UNTIL_WEB_FULL:
            ### if web is full check for size of msg###
            if DDOSScanner.is_big_msg(data.body):
                return True

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
