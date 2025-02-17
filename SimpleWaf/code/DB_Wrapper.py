import mysql.connector #pip install mysql-connector-python
import hashlib
ERROR_IP_ADDRESS = "0.0.0.0"
ERROR_WITH_DB_EXEC_COMMAND_CODE = [-1]
DEFAULT_STARTING_SCORE = 1
db_config = {
        "host": "localhost",
        "user": "user1",
        "password": "12345678",
        "database": "wafDataBase"
    }

### for attacker finding and blocking ###
from datetime import datetime, timedelta
def calc_n_days_from_now(n:int) -> str:

    current_date = datetime.now()
    future_date = current_date + timedelta(days=n)
    formatted_date = future_date.strftime('%Y-%m-%d')
    return formatted_date
def calc_days_until_free_for_attack(attacker_ip: str) -> int:
    ### get the current score ###
    NUM_OF_DAYS = 30
    current_score = get_score_of_attacker(attacker_ip)
    DAYS_UNTIL_FREE: int = int(NUM_OF_DAYS * current_score)
    return DAYS_UNTIL_FREE
def calc_attacker_free_date(attacker_ip: str) -> str:
    ### update the score ###
    special_insert_or_update_attackers_score(attacker_ip)

    days_until_free = calc_days_until_free_for_attack(attacker_ip)

    return calc_n_days_from_now(days_until_free)

def when_find_attacker(attacker_ip: str):
    free_date = calc_attacker_free_date(attacker_ip)
    special_insert_or_update_attackers_table(attacker_ip, free_date)



#general tables:
def drop_table(table_name:str):
    query = "DROP TABLE IF EXISTS " + table_name
    exec_command(query)

def print_table_values(table_name:str):
    """func for debug"""

    query = "SELECT * FROM "+table_name

    conn = None
    cursor = None
    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        # Print the rows
        print(f"Attackers Table ({len(rows)} rows):")
        for row in rows:
            print(row)

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        print("Connection closed.")

def exec_command(command:str,args_for_command:tuple=()) -> list:

    """
    func will ececute mysql command
    input: the query- command
    the additional arguments for each command (in %s or %d)

    output: if the command is an update/insert command - an empty list
    if the command is select command - list of the output
    """
    result = []
    conn = None
    cursor = None
    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        #print("Connection established.")
        cursor = conn.cursor()
        cursor.execute(command,args_for_command)
        result = cursor.fetchall()  # get the query results
        conn.commit()
        #print("execute command.")
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return ERROR_WITH_DB_EXEC_COMMAND_CODE#maybe add an error code that the func will know that error accured
    except Exception as e:
        print(e)
        return []
    if conn != None and cursor != None:
        cursor.close()
        conn.close()
    return result

def create_tables()->None:

#ip_len = len(ipv6) = 39
    websites_table = """
    CREATE TABLE IF NOT EXISTS websites_ip (
    host_name VARCHAR(255) UNIQUE,
    ip_address VARCHAR(39)    
    )
    """
    website_login = """
    CREATE TABLE IF NOT EXISTS website_login (
    host_name VARCHAR(255) UNIQUE,
    user_name VARCHAR(64) UNIQUE,
    hashed_password VARCHAR(64),
    email VARCHAR(128)    
    )
    """
    attackers_table = """
        CREATE TABLE IF NOT EXISTS attackers (
            attacker_ip VARCHAR(39) UNIQUE,
            date_to_free DATE
        )
        """
    #decimal(3,1) = up to 999 with 1 number of the dot
    #example: 543.2, 13.6
    attackers_score_table = """
        CREATE TABLE IF NOT EXISTS attackers_score (
            attacker_ip VARCHAR(39) UNIQUE,
            current_score DECIMAL(3,1)
        )
        """

### see documitation in Mismah Efion ###
    preferences_table = """
    CREATE TABLE IF NOT EXISTS preferences (
        host_name VARCHAR(255) UNIQUE,
        sql_strictness INTEGER,
        xss_defence  BOOL,
        hpp_defence BOOL,
        file_attacks_level INTEGER,
        send_email_when_attacked BOOL,
        os_level INTEGER,
        port INTEGER,
        isHttps BOOL
        )
        """

    #date_to_free= (yyyy-mm-dd) - string
    exec_command(websites_table)
    exec_command(website_login)
    exec_command(attackers_table)
    exec_command(attackers_score_table)
    exec_command(preferences_table)
    return

#attackers score:
def special_insert_or_update_attackers_score(attacker_ip_add:str,amount_to_add:float = 0.2)->None:
    """inserts new attacker or updates the score if the attacker already exists."""
    command = f"""
        INSERT INTO attackers_score (attacker_ip, current_score)
        VALUES (%s,{DEFAULT_STARTING_SCORE})
        ON DUPLICATE KEY UPDATE current_score = current_score + {amount_to_add}"""
    args = (attacker_ip_add,)
    exec_command(command,args)

def reset_score_of_attacker(attacker_ip_add:str,initial_score:float=1.0):
    command = """
            UPDATE attackers_score SET current_score = %s where attacker_ip = %s
            """
    args = (initial_score,attacker_ip_add)
    exec_command(command, args)

def get_score_of_attacker(attacker_ip_add:str) -> float:
    """get current score of attacker
        NOTE: need to insert the attacker to the db and only after
            to check his score"""
    command = """
        SELECT * FROM attackers_score where attacker_ip = %s
        """
    args = (attacker_ip_add,)
    result:list = exec_command(command, args)
    if len(result) == 1 and result != ERROR_WITH_DB_EXEC_COMMAND_CODE:
        attacker_details = result[0]
        current_score = attacker_details[1]
        return float(current_score)#we want type float, not dechimal
    else:
        print(f"there isn't a score for attack: {attacker_ip_add} ,please fix this.")
        return 3#if there isn't a score witch does not suppose to happend, we will generate a high score intentially
#attackers:
def insert_into_attackers(attacker_ip:str,date_to_free:str)->None:

    command = """
           INSERT INTO attackers (attacker_ip, date_to_free) 
           VALUES (%s, %s)
           """
    args = (attacker_ip,date_to_free)
    exec_command(command,args)

def special_insert_or_update_attackers_table(attacker_ip:str,date_to_free:str)->None:
    command = """
               INSERT INTO attackers (attacker_ip, date_to_free) 
               VALUES (%s, %s)
               ON DUPLICATE KEY UPDATE date_to_free = %s
               """
    args = (attacker_ip, date_to_free, date_to_free)
    exec_command(command, args)

def get_date_to_free_of_attacker(attacker_ip:str) -> str:
    command = """
           SELECT * FROM attackers where attacker_ip = %s
           """
    args = (attacker_ip,)
    result: list = exec_command(command, args)
    if len(result) == 1 and result != ERROR_WITH_DB_EXEC_COMMAND_CODE:
        attacker_details = result[0]
        date_to_free = attacker_details[1]
        return date_to_free
    return ""

def delete_attacker(attacker_ip:str)->None:

    command = """
               DELETE FROM attackers WHERE attacker_ip = %s
               """
    args = (attacker_ip,)
    exec_command(command, args)

def is_ip_blocked(user_ip:str)->bool:

    command = """
    SELECT * FROM attackers where attacker_ip = %s
    """
    args = (user_ip,)
    result:list = exec_command(command,args)
    #print(result)
    if len(result) == 0:#if there is not an instance of the userip in the attckers table
        return False
    return True

#websites_ip:
def insert_into_websites_ip(host_name:str,ip_add:str)->None:
    command = """
               INSERT INTO websites_ip (host_name, ip_address) 
               VALUES (%s, %s)
               """
    args = (host_name,ip_add)
    exec_command(command,args)

def update_website_ip(host_name:str,ip_add:str)->None:
    command = """
                  UPDATE websites_ip SET ip_address = %s where host_name = %s
                  """
    args = (ip_add, host_name)
    exec_command(command, args)

def special_insert_or_update_website_ip(host_name:str,ip_add:str)->None:
    """inserts new website or updates the ip address if the website already exists."""
    command = """
        INSERT INTO websites_ip (host_name, ip_address)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE ip_address = VALUES(ip_address)"""
    args = (host_name, ip_add)
    exec_command(command,args)

def get_ip_address_by_host_name(host_name:str)->str:
    command = """
        SELECT ip_address FROM websites_ip where host_name = %s
        """
    # for debug
    if host_name == "mysite.com":  # for debug
        return "127.0.0.1"  # for debug
    args = (host_name,)
    result = exec_command(command,args)
    if len(result) == 0 or result == ERROR_WITH_DB_EXEC_COMMAND_CODE:
        return ERROR_IP_ADDRESS
    if len(result) > 1:#need to treat this case?
        pass
    print(result[0][0])
    try:
        ip_add = result[0][0]#take the first query-> take the first(and only) argument
        return ip_add
    except Exception as e:
        print(e)
        return ERROR_IP_ADDRESS
def get_all_host_names():
    command = """
            SELECT host_name FROM websites_ip
            """
    result = exec_command(command)
    return result
#website_login:
def _hash_password(password:str):
    """func will encode the password before putting in db"""
    # maybe will be changes later into stronger hashing
    return hashlib.sha256(password)

def verify_login_into_website_login(user_name:str,password:str) -> bool:
    """func will check if the user_name match the password in the db"""
    hashed_password = _hash_password(password)
    command = """
        SELECT ip_address FROM websites_login where user_name = %s AND hashed_password = %s
        """
    args = (user_name,hashed_password)
    result = exec_command(command,args)
    if len(result) == 1 and result != ERROR_WITH_DB_EXEC_COMMAND_CODE:
        return True
    return False

def insert_into_website_login(host_name:str, user_name:str, password:str, email:str) -> bool:
    """func will perform sign up for new user
    :return true if insertion went without problems
    false - if there is an exsisting user name or other problem"""
    hashed_password = _hash_password(password)
    command = """
            INSERT INTO websites_ip (host_name, user_name,hashed_password, email)
            VALUES (%s, %s, %s, %s)"""
    args = (host_name,user_name,hashed_password,email)
    result = exec_command(command,args)
    if result == ERROR_WITH_DB_EXEC_COMMAND_CODE:
        return False
    return True

###  preferences table ###

from Preferences_Items import  Preferences_Items
def special_insert_or_update_preferences_table_preferences_table(prefs:Preferences_Items) ->None:
    """get the strings and send to the actual func"""
    command = """
                    INSERT INTO preferences (host_name, sql_strictness, xss_defence, hpp_defence,
                                              file_attacks_level, send_email_when_attacked, os_level,port,isHttps)
                    VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s)
                    ON DUPLICATE KEY UPDATE
                        sql_strictness = VALUES(sql_strictness),
                        xss_defence = VALUES(xss_defence),
                        hpp_defence = VALUES(hpp_defence),
                        file_attacks_level = VALUES(file_attacks_level),
                        send_email_when_attacked = VALUES(send_email_when_attacked),
                        os_level = VALUES(os_level),
                        port = VALUES(port),
                        isHttps = VALUES(isHttps)
                    """
    args = (prefs.host_name,prefs.sql_level,prefs.xss_defence,prefs.hpp_defence,prefs.file_attack_level,prefs.to_send_email,prefs.os_level,prefs.port,prefs.isHttps)
    exec_command(command, args)

def get_preferences_by_host_name(host_name:str) -> Preferences_Items:
    """func will get the pref of a host name
    if the host name does not exsit the func will output a default prefrences"""

    ### todo checnage this from hard coded to SQL.STRICTfor example
    defualt_prefs = [(host_name,3,True,True,3,True,1,443,True)]
    def_prefs_in_class = Preferences_Items(defualt_prefs)
    command = """
            SELECT * FROM preferences where host_name = %s
            """
    args = (host_name,)
    result = exec_command(command,args)
    if result == None or result == []:
        return def_prefs_in_class
    pref_in_class:Preferences_Items = Preferences_Items(result)
    return pref_in_class



def at_start():
    ###activate this func and after that delete it or something...###
    drop_table("preferences")
    create_tables()
    a:Preferences_Items = Preferences_Items([("phisherWeb.com",2,True,True,3,True,1,80,False)])
    #print(a.to_string())
    special_insert_or_update_preferences_table_preferences_table(a)
    print(get_preferences_by_host_name("phisherWeb.com").to_string())