from rich.text import Text
from ipaddress import ip_address


def send_preferences_commandes(argv: list[str]) -> Text:
    """
    the function sends a preferences message to the server
    :param argv: the command line arguments passed to the program
    :return: returns a Text object containing a message for the user
    """
    match argv[2]:
        case "-v":
            print('---send a view message to the server---')
            preferences = 'abcd\nidvsoivosinv\nmvmsovmsovmo'
            return Text('here is the preferences you have at the time: \n" + preferences + "\n', style="bold red")
        case "-s":
            if len(argv) < 4:
                return Text('Error: missing parameter\nUsage: "{argv[0]} preferences  -s <flags>"\nrun "{argv[0]} help?" for more information',
                            style="bold red")
            if argv[3] == "-f":
                if len(argv) != 5:
                    return Text('Error: missing parameter\nUsage: "{argv[0]} preferences  -s -f <file name>"\nrun "{argv[0]} help?" for more information',
                                style = "bold red")
                with open(argv[4], 'r') as file:
                    print(f'sending: {file.read()} to the server as prefernesses')
                    return Text('successfully changed your preferences', style="bold green")
            if argv[3] == "-m":
                if len(argv) != 5:
                    return Text(f'Error: missing parameter\nUsage: "{argv[0]} preferences  -s -f <file name>"\nrun "{argv[0]} help?" for more information',
                                style="bold red")
                print(f'sent {argv[4]} to the server as preferences')
                return Text('successfully changed your preferences', style = "bold green")
            else:
                return Text(f'Error: Invalid parameter\nno such flag "{argv[4]}" for command "preferences -s -m"\nrun "{argv[0]} help?" for more information',
                            style="bold red")
        case _:
            return Text(f'Error: Invalid parameter\nno such flag "{argv[2]}" for command "preferences"\nrun "{argv[0]} help?" for more information',
                        style="bold red")


def send_user_commandes(argv: list[str]) -> Text:
    """
    the function sends a user related message to the server
    :param argv: the command line arguments passed to the program
    :return: returns a Text object containing a message to send to the user
    """
    match argv[2]:
        case "-c":
            if len(argv) < 4:
                return Text(f'Error: missing parameter\nUsage: "{argv[0]} user  -c <flags>"\nrun "{argv[0]} help?" for more information',
                            style="bold red")
            match argv[3]:
                case "-n":
                    if len(argv) != 5:
                        return Text(f'Error: missing parameter\nUsage: "{argv[0]} user  -c -n <new username>"\nrun "{argv[0]} help?" for more information',
                                    style="bold red")
                    print(f"changing your username to {argv[4]}...")
                    return Text(f'successfully changed your name to {argv[4]}', style="bold green")
                case "-p":
                    if len(argv) != 5:
                        return Text(f'Error: missing parameter\nUsage: "{argv[0]} user  -c -p <new username>"\nrun "{argv[0]} help?" for more information',
                                    style="bold red")
                    print(f"changing your password to {argv[4]}...")
                    return Text(f'successfully changed your password to {argv[4]}', style="bold green")
                case "-m":
                    if len(argv) != 5:
                        return Text(f'Error: missing parameter\nUsage: "{argv[0]} user  -c -m <new username>"\nrun "{argv[0]} help?" for more information',
                                    style="bold red")
                    print(f"changing your mail to {argv[4]}...")
                    return Text(f'successfully changed your mail to {argv[4]}', style="bold green")
                case _:
                    return Text(f'Error: Invalid parameter\nno such flag "{argv[4]}" for command "user -c"\nrun "{argv[0]} help?" for more information',
                                style="bold red")
        case "-d":
            if len(argv) != 4:
                return Text(f'Error: missing parameter\nUsage: "{argv[0]} user  -d <username>"\nrun "{argv[0]} help?" for more information',
                            style="bold red")
            print(f"deleting user {argv[3]}...")
            return Text(f'successfully deleted user {argv[3]}', style="bold green")
        case "-a":
            if len(argv) != 6:
                return Text('Error: missing parameter\nUsage: "{argv[0]} user  -a <username> <password> <mail>"\nrun "{argv[0]} help?" for more information',
                            style="bold red")
            print(f"adding user {argv[3]} with password: {argv[4]} and mail: {argv[5]}...")
            return Text(f'successfully added user {argv[3]}', style="bold green")
        case _:
            return Text(f'Error: Invalid parameter\nno such flag "{argv[2]}" for command "user"\nrun "{argv[0]} help?" for more information',
                        style="bold red")


def is_valid_ip(ip: str) -> bool:
    """
    the function checks if a string could be a valid ip
    # :param ip: a string containing an ip address(potentially)
    :return: True if is a valid ip address, otherwise False
    """
    try:
        ip_address(ip)
        return True
    except ValueError:
        # If the input is not a valid IP address
        return False

def send_server_commandes(argv: list[str]) -> Text:
    """
   the function sends a user related message to the server
   :param argv: the command line arguments passed to the program
   :return: returns a message to send to the user and a bool indicating if its an error or nor(true for error)
   """
    match argv[2]:
        case "-d":
            if len(argv) < 4:
                return Text(
                    f'Error: missing parameter\nUsage: "{argv[0]} server  -d <server domain>"\nrun "{argv[0]} help?" for more information',
                    style="bold red")
            print(f"deleting the server: {argv[3]}...")
            return Text(f"successfully deleted the server: {argv[3]}", style="bold green")
        case "-a":
            if len(argv) < 5:
                return Text(
                    f'Error: missing parameter\nUsage: "{argv[0]} server  -a <server domain> <server ip>"\nrun "{argv[0]} help?" for more information',
                    style="bold red")
            if is_valid_ip(argv[4]) is False:
                return Text(f'Error: invalid parameter\n"{argv[4]}" is not a valid ip address\nrun "{argv[0]} help?" for more information',
                            style="bold red")
            print(f"adding the server: {argv[3]}...")
            return Text(f"successfully added the server: {argv[3]}", style="bold green")
        case _:
            return Text(
                f'Error: Invalid parameter\nno such flag "{argv[2]}" for command "server"\nrun "{argv[0]} help?" for more information',
                style="bold red")



