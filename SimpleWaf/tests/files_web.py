from flask import Flask, request
import requests
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def handle_request():
    print("Files found: "+str(request.files))

app.run(debug=True, host="0.0.0.0", port=3333)