from flask import Flask, request, send_file
import sys
sys.path.append("../code")
import DB_Wrapper
FILES_PATH = "public/"
import requests
app = Flask(__name__)
### todo : think on cookies system- can use nodejs for cookies, or check flask ones,
### todo : when user tries to sign up - give him cookie and send verfication mail
@app.route('/signUp',methods=['POST'])
def handle_request():

    #if the web does not in the waf lists?
    try:
        print("hi")
        jsonVars = request.json
        print(jsonVars)
        host_name = jsonVars['host_name']
        username = jsonVars['username']
        ### check if name is not already exsist ###
        password = jsonVars['password']
        email = jsonVars['email']

        if not host_exist_in_db(host_name):
            return {"status": "failed", "message": "host name does not exist in db"}
        if DB_Wrapper.check_if_username_exist_in_website_login(username):
            return {"status": "failed", "message": "username already exist"}
        DB_Wrapper.insert_into_website_login(host_name,username,password,email)
        return {"status": "success", "message": "Sign-up request received"}
    except Exception as e:
        print(e)
        print("sending error")
        return {"status":"error"}

def host_exist_in_db(hostname)->bool:
    result = DB_Wrapper.get_ip_address_by_host_name(hostname)
    if result == DB_Wrapper.ERROR_IP_ADDRESS:
        return False
    return True

@app.route('/signUp',methods=['GET'])
def getSignUpPage():
    """the order of moves:
    first the user send req to url in our web like: web/signup
    we will provide the user with the html content first,
    in the html content there is a script tag that contains the js file name,
    the user's computer will auto send req to get this js file"""
    htmlContentPath = FILES_PATH+"signUpScreen.html"
    return send_file(htmlContentPath)
@app.route('/signUpScreen.js',methods=['GET'])
def getSignUpJsFile():
    jsContentPath = FILES_PATH + "signUpScreen.js"
    return send_file(jsContentPath)

app.run(debug=True, host="127.0.0.1", port=12345)

