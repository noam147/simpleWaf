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
    #date_to_free= (yyyy-mm-dd) - string
    exec_command(websites_table)
    exec_command(website_login)
    exec_command(attackers_table)
    exec_command(attackers_score_table)
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

def check_functionality():
    create_tables()
    print_table_values("attackers")
    #websites
    example_ip = "111.123.222.121"
    example_host_name = "mySite.com2"
    insert_into_websites_ip(example_host_name,example_ip)
    print_table_values("websites_ip")
    get_ip_address_by_host_name(example_host_name)

    #attackers
    example_user_ip = "99.99.99.99"
    insert_into_attackers(example_user_ip,"2025-00-00")
    print(is_ip_blocked(example_user_ip))
    delete_attacker(example_ip)
    print_table_values("attackers")
