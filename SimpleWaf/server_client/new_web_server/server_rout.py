from flask import Flask, session, request, jsonify,redirect,url_for
import DB_Wrapper
import unlogged_user_menu
import logged_user_menu
import waf_handler
app = Flask(__name__)
app.secret_key = 'dragon_castle_key_secure'
UNLOGGED = 'Guest'
SERVER_PORT = 47777

#todo add gui pages
def get_file_content(file_path):
    try:
        with open(file_path,"r") as f:
            return f.read()
    except Exception:
        return "Try again later"
@app.route('/')
def open_screen():
    file_path = "../web_files/index.html"
    return get_file_content(file_path)
@app.route('/login', methods=['GET'])
def get_login_screen():
    file_path = "../web_files/login.html"
    return get_file_content(file_path)
@app.route('/add_website', methods=['GET'])
def get_add_website_screen():
    file_path = "../web_files/add_website.html"
    return get_file_content(file_path)
@app.route('/add_user', methods=['GET'])
def get_add_user_screen():
    file_path = "../web_files/add_user.html"
    return get_file_content(file_path)
@app.route('/add_user', methods=['POST'])
def add_user_route():
    json_msg = request.get_json()
    success, message = unlogged_user_menu.add_user(json_msg)
    return jsonify({"success": success, "message": message})
@app.route('/add_website', methods=['POST'])
def add_website_route():
    json_msg = request.get_json()
    success, message = unlogged_user_menu.add_website(json_msg)
    return jsonify({"success": success, "message": message})


@app.route('/login', methods=['POST'])
def login_route():
    json_msg = request.get_json()
    success, message = unlogged_user_menu.login(json_msg)
    if success:
        username = json_msg["username"]
        set_username(username)
        host_name = DB_Wrapper.get_host_name_for_user(username)
        set_host_name(host_name)
    return jsonify({"success": success, "message": message})


@app.route('/see_preferences', methods=['GET'])
def see_preferences_route():
    hostname = get_session_host_name()
    if hostname == UNLOGGED:
        return redirect(url_for("login_route"))
    success, data = logged_user_menu.see_preferences(hostname)
    return jsonify({"success": success, "data": data})

@app.route('/set_preferences', methods=['POST'])
def set_preferences_route():
    hostname = get_session_host_name()
    if hostname == UNLOGGED:
        return redirect(url_for("login_route"))
    json_msg = request.get_json()
    success, message = logged_user_menu.set_preferences(json_msg, hostname)
    return jsonify({"success": success, "message": message})

@app.route('/log_file', methods=['GET'])
def see_log_file_route():
    hostname = get_session_host_name()
    if hostname == UNLOGGED:
        return redirect(url_for("login_route"))
    success, log_data = logged_user_menu.see_log_file(hostname)
    return jsonify({"success": success, "log_data": log_data})
@app.route('/data_base', methods=['GET'])
def get_db():
    #this is only to WAF...
    key = request.headers.get("key","nothing")
    print(request.headers)
    if key != 'THIS IS WAF':
        return ""
    return waf_handler.send_pref()
def set_username(username:str):
    session['credentials_U'] = username
def set_host_name(hostname:str):
    session['credentials_H'] = hostname

def get_session_username():
    return session.get("credentials_U", UNLOGGED)
def get_session_host_name():
    return session.get("credentials_H", UNLOGGED)
if __name__ == '__main__':
    app.run(debug=True,port=SERVER_PORT)#todo change debug in production to false
