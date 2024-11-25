<<<<<<< HEAD
from flask import Flask, request, jsonify, abort
import requests
from urllib.parse import urlparse, urlencode
import DB_Wrapper
=======
from flask import Flask, request, jsonify
from jsonpatch import multidict
from multidict import MultiDict
from werkzeug.datastructures import FileStorage
>>>>>>> e1a02a3055a7566bd0625b4dadd3db91a66da19e

app = Flask(__name__)


@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def process_request(path):
<<<<<<< HEAD

    # Extract website address and get IP from DB
    website_addr = urlparse(request.base_url).hostname
    website_ip = DB_Wrapper.getWebsiteIp(website_addr)
    print(website_addr + " - " + website_ip)
    if website_ip is None:
        print("abort")
        abort(404)

    # Construct the target URL
    ### code for testing ###
    new_url = f"{request.scheme}://{website_ip}:5001/{path}"

    ### code for production ###
    #new_url = f"{request.scheme}://{website_ip}/{path}"

    # Handle query parameters
    if request.query_string:
        query_string = urlencode(request.args.to_dict())
        new_url = f"{new_url}?{query_string}"

    # Forward the request
    if request.method == 'GET':
        response = requests.get(new_url)
    else:
        response = requests.post(new_url, data=request.data)

    return response.content, response.status_code, response.headers.items()

=======
    def see_params():
        """this is not a real func,it's just to see the syntax"""
        url_arg:MultiDict = request.args
        headers = request.headers
        general_data:bytes = request.data
        print(general_data)
        #if request.content_type == 'application/json':
        if request.is_json:
            json_data = request.json
        print(request.files)
        if 'file' in request.files:
            files:MultiDict = request.files# This is a MultiDict of all uploaded files
            file:FileStorage = files['file'] # Access the specific file uploaded with the field name 'file'
            print(file.mimetype)
            print(file.name)

        user_ip = request.remote_addr
        print(user_ip)
        return
    #see_params()
    host_header = request.headers.get('host')
    if host_header == '':
        return jsonify({"error": "Bad Request", "message": "Host header is missing"}), 400
    return f"you reached {host_header}"
>>>>>>> e1a02a3055a7566bd0625b4dadd3db91a66da19e

if __name__ == "__main__":
    app.run(port=5000)
