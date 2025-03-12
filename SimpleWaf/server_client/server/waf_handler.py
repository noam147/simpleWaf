import requests
url_of_waf = "http://127.0.0.1:5000"
def get_log_file_of_web(hostname) -> str:
    headers = {'ACTION':'LOG',
               'WEB_NAME':hostname}
    try:
        response :requests.Response = requests.get(url_of_waf,headers=headers)
    except Exception:
        return 'Error'
    return response.text if response.status_code == 200 else 'Error'

    #todo - make it in gui good for client - in client side

get_log_file_of_web('mysite.com')