import requests
WAF_IP_ADDRESS = "127.0.0.1"
PORT = 5000
url = f"http://{WAF_IP_ADDRESS}:{PORT}"
def t1est_1()->bool:
    #does not work at this moment ->
    #need to put https in url, and some headres are prablomatic
    existing_web_host_name = "dns.google"
    headers = {
        "Host": existing_web_host_name
    }
    response = requests.get(url,headers=headers)
    print(response)
def t1est_2()->bool:
    not_existing_web_host_name = "my_not_existing_site.com"
    headers = {
        "Host": not_existing_web_host_name
    }

    response = requests.get(url,headers=headers)
    print(response)
def activate_all_tests():
    t1est_1()
    t1est_2()
if __name__ == '__main__':
    activate_all_tests()
