from sys import argv
from rich.console import Console
from rich.text import Text

import sending_utils
import sending_utils as su

# Create a Console object for Rich
console = Console()

def main():
    if len(argv) < 3:
        console.print(f'Error: missing parameter\nUsage: "{argv[0]} <command> <flags>"\nrun "{argv[0]} help?" for more information',
                      style="bold red")
    match argv[1]:
        case "preference":
            console.print(sending_utils.send_preferences_commandes(argv))
        case "user":
            console.print(sending_utils.send_user_commandes(argv))

        case "server":
            console.print(sending_utils.send_server_commandes(argv))
        case _:
            console.print(
                Text(f'Error: invalid parameter, {argv[1]} is not a valid command\nUsage: "{argv[0]} <command> <flags>"\nrun "{argv[0]} help?" for more information',
                style="bold red"))

if __name__ == "__main__":
    main()
