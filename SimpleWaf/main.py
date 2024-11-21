from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', defaults = {'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def process_request(path):
    host_header = request.headers.get('host')
    if host_header == '':
        return jsonify({"error": "Bad Request", "message": "Host header is missing"}), 400
    return f"you reached {host_header}"

if __name__ == "__main__":
    app.run()