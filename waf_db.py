import mysql.connector #pip install mysql-connector-python

ERROR_IP_ADDRESS = "0.0.0.0"
def print_table_values(table_name:str):
    """func for debug"""

    db_config = {
        "host": "localhost",
        "user": "user1",
        "password": "12345678",
        "database": "wafDataBase"
    }

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
    db_config = {
        "host": "localhost",
        "user": "user1",
        "password": "12345678",
        "database": "wafDataBase"
    }
    result = []
    conn = None
    cursor = None
    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        print("Connection established.")
        cursor = conn.cursor()
        cursor.execute(command,args_for_command)
        result = cursor.fetchall()  # get the query results
        conn.commit()
        print("execute command.")
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return []
    except Exception as e:
        print(e)
        return []
    if conn != None and cursor != None:
        cursor.close()
        conn.close()
    return result

def create_tables()->None:

    websites_table = """
    CREATE TABLE IF NOT EXISTS websites_ip (
    host_name VARCHAR(255) UNIQUE,
    ip_address TEXT    
    )
    """
    attackers_table = """
        CREATE TABLE IF NOT EXISTS attackers (
            attacker_ip VARCHAR(13) UNIQUE,
            date_to_free DATE
        )
        """
    #date_to_free= (yyyy-mm-dd) - string
    exec_command(websites_table)
    exec_command(attackers_table)
    return

#attackers:
def insert_into_attackers(attacker_ip:str,date_to_free:str)->None:

    command = """
           INSERT INTO attackers (attacker_ip, date_to_free) 
           VALUES (%s, %s)
           """
    args = (attacker_ip,date_to_free)
    exec_command(command,args)
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

    #if there is a field with that - return true
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
    pass
def get_ip_address_by_host_name(host_name:str)->str:
    command = """
        SELECT ip_address FROM websites_ip where host_name = %s
        """
    args = (host_name,)
    result = exec_command(command,args)
    if len(result) == 0:
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

def check_functunallty():


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