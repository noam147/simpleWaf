from flask import Flask, request, jsonify
from jsonpatch import multidict
from multidict import MultiDict
from werkzeug.datastructures import FileStorage

app = Flask(__name__)

@app.route('/', defaults = {'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def process_request(path):
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

if __name__ == "__main__":
    app.run()