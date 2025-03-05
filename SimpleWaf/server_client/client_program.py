import guiStaff
available_commands = ['Help','Add Website','Add User','Print Menu','Log In','Exit']
dict_available_commands = {index: command for index, command in enumerate(available_commands)}
#Help for specific commands
#help_dict = {'Help':'get help for spec'}
#menu = "[1]."
def get_menu():
    menu = "Available Commands:\n"
    for i in range(len(available_commands)):
        menu += f"[{i+1}]. {available_commands[i]}\n"
    return menu[:-1]#without the last \n
def add_user():
    print('---Add User Selected---')
    host_name = input("Enter Host Name of Website That Signed To WAF:\n")
    #todo check with server if host name exsist and then if yes continue
    user = input("Enter User Name:\n")
    #todo check if username already exsist
    password = input('Enter Password For User:\n')
    print('---User Added Successfully---')


def main():

    menu = get_menu()
    print(guiStaff.start_of_screen)
    while True:
        print(menu)
        current_choice = int(input())
        print(dict_available_commands)
        actual_command = dict_available_commands[current_choice]
        print(actual_command)
        if current_choice == '2':
            add_user()


if __name__ == '__main__':
    main()