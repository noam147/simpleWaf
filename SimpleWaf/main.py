from flask import Flask, request, jsonify, abort
import requests
from urllib.parse import urlparse, urlencode
import DB_Wrapper

app = Flask(__name__)


@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def process_request(path):

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


if __name__ == "__main__":
    app.run(port=5000)
