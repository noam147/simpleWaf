from flask import Flask, request
import requests
from before_tests import *
import urllib.parse
app = Flask(__name__)

### establish a new server to get the req from the WAF and check if it got the actually '<' to the &lg shape
@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def handle_request():
    print(f"Method: {request.method}")
    print(f"Headers: {request.headers}")
    print(f"Body: {request.get_data(as_text=True)}")
    body = request.get_data(as_text=True)
    body = urllib.parse.unquote(body)
    if "<" in body or ">" in body:
        print("TEST FAILED! FOUND IN BODY")
    else:
        print("TEST PASSED!")
    return "Request received!", 200

@before_test
def t1est():
    ### requirements: ###
    # in dbwrapper: special_insert_or_update_website_ip("loopback.com","127.0.0.1")

    app.run(debug=False, host="0.0.0.0", port=5001)
    host_name = "loopback.com/<script>"
    headers = {
        "Host": host_name,
        "yay":"my mal script <script>alert(1)</script>"
    }
    data = {
        'user': '123',
        'pass': 'hellooo<script>alert(1)</script>'
    }
    response = requests.post(url, headers=headers, data=data)
    print(response)
if __name__ == '__main__':
    t1est()
