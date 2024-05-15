from serializer import Serializer
from data_base import DataBase
from user import UserData
from password_generator import generate_random_password
import pyperclip
import signal
import sys
import getpass

AUTHOR = "Yablonskyi Nazarii (Nazarwadim)"

help_string = f"\n **Help menu** \n \
                h - help\n \
                e - exit\n \
                a - add new password\n \
                r - remove password from index\n \
                s - show all(passwords will be hidden)\n \
                cl - copy login\n \
                cp - copy password\n \
                ch - change existing\n \
                au - author\n \
                --------------------------------------------"

data_base = DataBase(Serializer())

def get_input_password() -> str:
    action = input("Generate random password? Y/N:").lower()
    if action == 'n':
        while True:
            password = getpass.getpass("Password: ")
            verify_password = getpass.getpass("Password second time: ")
            if(password == verify_password):
                break
            print("Invalid password verify. Both passwords must be same!")
        return password
    
    length = int(input("Print password length(can`t be larger than 1000):"))
    if length <= 0 or length > 1000: 
        print("Invalid length. Generating 12 length password.")
        return generate_random_password(12)
    return generate_random_password(length)
    

def get_input_position() -> int:
    position = input("Print index:")
    return int(position)

def signal_handler(sig, frame):
    global data_base
    data_base.close()
    print(' Ctrl+C preased. Data saved. Exit.')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

print('Enter Ctrl+C to exit.')

def show_all():
    global data_base
    user_data_list = data_base.get_data()

    counter = 0
    for user_data in user_data_list:
        counter += 1
        print(str(counter) + ')',user_data, '\n')
        
                
def on_add_password():
    global data_base
    user_data = UserData()
    user_data.title = input("Input title:")
    user_data.description = input("Input description(can be skipped by pressing 'enter'):")
    user_data.email = input("Input email(can be skipped):")
    user_data.login = input("Input login(skip?):")
    user_data.password = get_input_password()
    
    data_base.add_user_data(user_data)

def on_remove_password():
    global data_base
    position = get_input_position()
    try:
        sure = input("Sure: Y/N").lower()
        if sure == "n":
            return
        data_base.remove_user_data(position - 1)
    except Exception:
        print("Invalid position.")

def on_copy_login():
    global data_base
    position = get_input_position()
    try:
        user_data = data_base.get_user_data(position - 1)
        pyperclip.copy(user_data.login)
        input("Enter anything to remove login from clipboard.")
        pyperclip.copy(' ')
    except Exception:
        print("Invalid position.")
    
def on_copy_password():
    global data_base
    position = get_input_position()
    try:
        user_data = data_base.get_user_data(position - 1)
        pyperclip.copy(user_data.password)
        input("Enter anything to remove login from clipboard.")
        pyperclip.copy(' ')
    except Exception:
        print("Invalid position.")
    

def on_change():
    global data_base
    position = get_input_position()
    try:
        user_data = data_base.get_user_data(position - 1)
    except Exception:
        print("Invalid position.")
        return
    action = input("Input t to change title, d to description, e to email, p to password, l to login\n")
    
    if action == 't':
        user_data.title = input("Input new title:")
    elif action == 'p': 
        user_data.password = get_input_password()
    elif action == 'd':
        user_data.description = input("Input new description:")
    elif action == 'e':
        user_data.email = input("Input new email:")
    elif action == 'l':
        user_data.login = input("Input new login:")

def on_start_use():
    global data_base
    global help_string
    global AUTHOR
    c : str = " "
    while c != 'e':
        c = input("'h' for commands list:")
        if c == 'h':
            print(help_string)
        elif c == 'a':
            on_add_password()
        elif c == 'r':
            on_remove_password()
        elif c == 's':
            show_all()
        elif c == 'cl':
            on_copy_login()
        elif c == 'cp':
            on_copy_password()
        elif c == 'ch':
            on_change()
        elif c == 'au':
            print(AUTHOR)

def on_search_db():
    global data_base
    dbs = data_base.get_available_db_names()
    print("Available password bases:", dbs)
    
    if(len(dbs) == 0):
        print("You have not existing data bases.")
    
    action = input("Create new DB? Y/N ").lower()
    if(action == 'y'):
        while True:
            password = getpass.getpass("Password: ")
            verify_password = getpass.getpass("Password second time: ")
            if(password == verify_password):
                break
            print("Invalid password verify. Both passwords must be same!")
        
        filename = input("Input filename: ")
        data_base.new(password, filename)
        return
    
    db = input("Data base:")
    
    if not db in dbs:
        print("Incorrect data base. Exit.")
        exit()

    counter = 3
    while(counter != 0):
        password = getpass.getpass("Password: ")
        try:
            data_base.open(password, db)
            break
        except Exception:
            print("Incorrect password! Try again.")

        counter -= 1
    else:
        print("Too many attempts. Exit.")
        exit()
    
def main():
    global data_base
    on_search_db()
    on_start_use()
    
    data_base.close()
    
deas = False
def test():
    global deas
    assert(deas)

if __name__ == "__main__":    
    if len(sys.argv) == 2 and sys.argv[1] == "--test":
        test()
    else:
        main()