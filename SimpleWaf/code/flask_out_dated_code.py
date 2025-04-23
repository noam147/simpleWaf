from flask import Flask, request, jsonify, abort, Response
import requests
from urllib.parse import urlparse, urlencode
import DB_Wrapper
from jsonpatch import multidict
from multidict import MultiDict
from werkzeug.datastructures import FileStorage

from SearchAttackHelper import SearchAttacks

from vars_for_global_use import *

app = Flask(__name__)
PORT_APP = 5000

EXAMPLE_WEBSITE_PORT = 5001


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


def is_attacker(ip_add: str) -> bool:
    return DB_Wrapper.is_ip_blocked(ip_add)


def send_empty_msg_with_code(code: int):
    return "", code, None


@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def process_request(path):
    """
    the function gets a request sent from the user and process it using the waf logic
    :param path: the path of the request sent
    :return: the response to send
    """
    # check if user is attacker:
    ip_address = request.environ['REMOTE_ADDR']
    print(ip_address)
    if is_attacker(ip_address):
        print("attacker found!")
        return send_empty_msg_with_code(ATTACKER_CODE)

    # Extract website address and get IP from DB
    host_name = urlparse(request.base_url).hostname
    # host_name = request.headers.get("Host", "")
    website_ip = DB_Wrapper.get_ip_address_by_host_name(host_name)

    print(str(host_name) + " - " + str(website_ip))
    if website_ip is None or website_ip == DB_Wrapper.ERROR_IP_ADDRESS:
        print("abort- website not exist")
        return send_empty_msg_with_code(WEBSITE_NOT_EXIST_CODE)
    ### for debug ###
    _see_params()

    ### check attacks ###
    current = SearchAttacks(request)
    if current.search_attacks():
        return send_empty_msg_with_code(ATTACK_FOUND_CODE)  # attack found
        # DB_Wrapper.insert_into_attackers()#need to insert into table

    # Construct the target URL
    ### code for testing ###
    new_url = f"{request.scheme}://{website_ip}:{EXAMPLE_WEBSITE_PORT}/{path}"
    # new_url = f"https://{website_ip}/{path}"# - need to check when to use https
    ### flask working on http- but most websites on https ###

    ### code for production ###
    # new_url = f"{request.scheme}://{website_ip}/{path}"

    # Handle query parameters
    if request.query_string:
        query_string = urlencode(request.args.to_dict())
        new_url = f"{new_url}?{query_string}"

    host_header = request.headers.get('host')
    if host_header == '':
        return jsonify({"error": "Bad Request", "message": "Host header is missing"}), 400
    response = requests.Response
    # Forward the request
    if request.method == 'GET':
        try:
            response = requests.get(new_url, timeout=1)
        except Exception as e:
            print(e)
            return send_empty_msg_with_code(WEBSITE_NOT_RESPONDING_CODE)
    elif request.method == 'POST':
        response = requests.post(new_url, data=request.data, timeout=1)
    else:
        abort(500)  # we are not handling other requests right now

    # maybe this is the way to get back responses to client?
    """response_to_client = Response(
        response.content,
        status=response.status_code,
        headers=dict(response.headers)
    )
    return response_to_client"""
    # return response
    ### there are some headers that causing flask not to work ###
    # for example: Content-Encoding: gzip, Transfer-Encoding: chunked
    return response.content, response.status_code, response.headers.items()


if __name__ == "__main__":
    app.run(port=PORT_APP)
