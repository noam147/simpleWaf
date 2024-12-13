
from flask import Flask, request, jsonify, abort
import requests
from urllib.parse import urlparse, urlencode
import DB_Wrapper
from jsonpatch import multidict
from multidict import MultiDict
from werkzeug.datastructures import FileStorage
import SQLI_Modules.SQLI_Scanner as SQLI_s

app = Flask(__name__)


def _see_params():
    """
    the function is meant for debug
    the function prints the data from the request given
    :return:
    """
    url_arg: MultiDict = request.args
    headers = request.headers
    general_data: bytes = request.data
    print(b"raw data: " + general_data)
    # if request.content_type == 'application/json':
    if request.is_json:
        json_data = request.json
    print("files: " + str(request.files))
    if 'file' in request.files:
        files: ImmutableMultiDict = request.files  # This is a MultiDict of all uploaded files
        file: FileStorage = files['file']  # Access the specific file uploaded with the field name 'file'
        print("file mimetype: " + file.mimetype)
        print("file name: " + file.name)

    user_ip = request.remote_addr
    print("user ip: " + user_ip)
    return


@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def process_request(path):
    """
    the function gets a request sent from the user and process it using the waf logic
    :param path: the path of the request sent
    :return: the response to send
    """
    # Extract website address and get IP from DB
    website_addr = urlparse(request.base_url).hostname
    website_ip = DB_Wrapper.getWebsiteIp(website_addr)
    print(str(website_addr) + " - " + str(website_ip))
    if website_ip is None:
        print("abort")
        abort(404)
    ### for debug ###
    _see_params()

    # Construct the target URL
    ### code for testing ###
    new_url = f"{request.scheme}://{website_ip}:5001/{path}"

    ### code for production ###
    # new_url = f"{request.scheme}://{website_ip}/{path}"

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


if __name__ == "__main__":
    app.run(port=5000)
