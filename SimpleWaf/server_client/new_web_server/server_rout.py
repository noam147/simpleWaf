from flask import Flask,render_template, session, request, jsonify,redirect,url_for,send_file
import DB_Wrapper
import unlogged_user_menu
import logged_user_menu
import waf_handler
import json
from collections import Counter
import EmailSending
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
    content = get_file_content(file_path)
    username,hostname = get_session_username(),get_session_host_name()
    if username == UNLOGGED or hostname == UNLOGGED:
        #if user did not log just pass the filecontent
        return content
    keyword = "Guest"
    index = content.find(keyword)
    if index == -1:
        return content

    partA = content[:index] +"\""+username+"\"<br>You Are Connected to The website: \""+hostname+"\"<br><a href=\"/logout\">Logout</a>"

    partB = content[index+len(keyword):]
    return partA + partB
@app.route('/images/<img_name>')
def get_img(img_name):
    img_name = img_name.replace("\\", "")
    img_name = img_name.replace("/", "")
    file_path = f"../web_files/images/{img_name}"
    print(file_path)
    try:
        # Sending the image file
        return send_file(file_path, mimetype='image/png')  # Adjust the mimetype if needed
    except FileNotFoundError:
        return "Image not found", 404
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
@app.route('/logout')
def logout():
    #if the user will save the cookie, he will still be able to login with that cookie
    session.pop("credentials_U", None)
    session.pop("credentials_H", None)
    return redirect(url_for("open_screen"))

@app.route('/see_preferences', methods=['GET'])
def see_preferences_route():
    hostname = get_session_host_name()
    if hostname == UNLOGGED:
        return redirect(url_for("login_route"))
    success, data = logged_user_menu.see_preferences(hostname)
    if success:
        return render_template("preferences.html", data=data)
    #todo return maybe some html file that will help the user to edit the prefs
    return jsonify({"success": success, "data": data})

@app.route('/set_preferences', methods=['POST'])
def set_preferences_route():
    hostname = get_session_host_name()
    if hostname == UNLOGGED:
        return redirect(url_for("login_route"))
    json_msg = request.get_json()
    success, message = logged_user_menu.set_preferences(json_msg, hostname)
    return jsonify({"success": success, "message": message})
def get_good_logs(log_data):
    try:
        log_entries = [json.loads(line) for line in log_data.split("\n") if line.strip()]
        attack_types = [entry["attack type"] for entry in log_entries]
        attack_counts = dict(Counter(attack_types))
        return render_template("log_file.html",attack_counts=attack_counts, logs=log_entries)
    except Exception as e:
        return jsonify({"success": False, "log_data": "Error during phrasing"})

@app.route('/log_file', methods=['GET'])
def see_log_file_route():
    hostname = get_session_host_name()
    if hostname == UNLOGGED:
        return redirect(url_for("login_route"))
    success, log_data = logged_user_menu.see_log_file(hostname)
    if log_data == 'Error' and success == True:
        return "<h1>Log File is Empty<h1>"
        #return jsonify({"success": success, "log_data": "Log File is Empty"})

    return get_good_logs(log_data)
    #return jsonify({"success": success, "log_data": log_data})
@app.route('/data_base', methods=['GET'])
def get_db():
    #this is only to WAF...
    key = request.headers.get("key","nothing")
    print(request.headers)
    if key != 'THIS IS WAF':
        return ""
    return waf_handler.send_pref()
@app.route('/attacker_alert', methods=['GET'])
def add_attacker():
    attacker_ip = request.args.get("ip","")
    free_date = request.args.get("free_date","")
    hostname = request.args.get("hostname","")
    if attacker_ip == "" or free_date == "":
        return "Error"
    #this is only to WAF...
    key = request.headers.get("key","nothing")
    print(request.headers)
    if key != 'THIS IS WAF':
        return ""
    print(attacker_ip)
    print(free_date)
    DB_Wrapper.insert_into_attackers(attacker_ip, free_date)
    print(hostname)
    if hostname != "":
        pref = DB_Wrapper.get_preferences_by_host_name(hostname)
        if pref.to_send_email:
            emails = DB_Wrapper.get_all_emails_of_users_from_host_name(hostname)
            print(emails)
            for email in emails:
                EmailSending.send_attack_alert_email(email,"UNKNOWN CHECK LOG",hostname)
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
    app.run(debug=True,port=SERVER_PORT,host="0.0.0.0")#todo change debug in production to false
