from flask import Flask, request, send_file

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
        username = jsonVars['username']
        ### check if name is not already exsist ###
        password = jsonVars['password']
        email = jsonVars['email']
        return {"status": "success", "message": "Sign-up request received"}
    except Exception as e:
        print("sending error")
        return {"status":"error"}



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