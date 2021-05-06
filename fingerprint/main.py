import json

from client.client import Client
client = Client()
import test.util as tutil

from client.exceptions import AuthFailed, DuplicateUser, UnknownUser, WrongPin, CliInvalidChoice

# TODO: take parameters from config
pin_length = 4
fingerprint_length = 12
fingerprint_range = (0, 255)
input_file = "test/input-list.json"

def parse_input(file_name):
    with open(f'test/{file_name}') as file:
        data = json.load(file)
    return data

def print_user(user, return_single_line_str=False):
    if not return_single_line_str:
        print("Roll no:\t", user["roll_no"])
        print("Pin:\t\t", user["pin"])
        print("Fingerprint:\t", " ".join([str(x) for x in user["fingerprint"]]))
    else:
        return f'{user["roll_no"]}\t{user["pin"]}\t{user["fingerprint"]}'

def select_user_from_input_file():
    with open(input_file) as file:
        data = json.load(file)
        if len(data) == 0:
            print("No users in input file")
            raise Exception
        print("Select one of these")
        for i in range(len(data)):
            print(f'{i+1}) {print_user(data[i], return_single_line_str=True)}')
        choice = int(input(f'Enter choice: '))
        if choice < 1 or choice > len(data):
            raise CliInvalidChoice
        user = data[choice-1]
    return user

def enter_user_data():
    roll_no = input("Enter roll number, leave blank for random: ")
    roll_no = roll_no if roll_no else tutil.generate_roll_number()
    pin = input(f"Enter {pin_length} digit pin, leave blank for random: ")
    pin = pin if pin else tutil.generate_pin()
    print("Fingerprint")
    print(f"Format: {fingerprint_length} space seperated integers in range {fingerprint_range}")
    fingerprint = input("Enter fingerprint, leave blank for random: ")
    fingerprint = [int(x) for x in fingerprint.split()] if fingerprint else tutil.generate_fingerprint()
    user = {
        "roll_no": roll_no,
        "pin": pin,
        "fingerprint": fingerprint
    }
    return user

def enroll_user_menu():
    print()
    print("Enroll user menu")
    print("0) Go back to main menu")
    print("1) Generate random user")
    print("2) Give user data manually")
    print("3) Select user from input file")
    option = input("Enter a number (0-2): ")

    user = None
    if option == "1":
        user = tutil.generate_random_user()
        print("Generated random user with following details")
        print_user(user)
    elif option == "2":
        user = enter_user_data()
        print("Following details were entered for user")
        print_user(user)
    elif option == "3":
        try:
            user = select_user_from_input_file()
        except CliInvalidChoice:
            print("You have entered an invalid choice.")
            return
    elif option == "0":
        return

    print("="*20)
    try:
        client.enroll(user)
        print(f'{user["roll_no"]} has been enrolled successfully')
    except (DuplicateUser, ):
        print("User already exists:", user["roll_no"])
    print("="*20)

def authenticate_user_menu():
    print()
    print("Authenticate user menu")
    print("0) Go back to main menu")
    print("1) Generate random user")
    print("2) Give user data manually")
    print("3) Select user from input file")
    option = input("Enter a number (0-2): ")

    user = None
    if option == "1":
        user = tutil.generate_random_user()
        print("Generated random user with following details")
        print_user(user)
    elif option == "2":
        user = enter_user_data()
        print("Following details were entered for user")
        print_user(user)
    elif option == "3":
        try:
            user = select_user_from_input_file()
        except CliInvalidChoice:
            print("You have entered an invalid choice.")
            return
    elif option == "0":
        return

    print("="*20)
    try:
        client.verify(user)
        print(f'{user["roll_no"]} has been authenticated successfully')
    except AuthFailed:
        print(f'Could not authenticate the fingerprint for {user["roll_no"]}')
    except WrongPin:
        print(f'Could not retrieve user data of {user["roll_no"]}, wrong pin entered.')
    except UnknownUser:
        print(f'Please enroll the user {user["roll_no"]} before authenticating')
    print("="*20)

def get_authentication_history_menu():
    print()
    print("Get authentication history menu")
    print("0) Go back to main menu")
    print("1) Generate a random roll no")
    print("2) Enter roll no manually")
    print("3) Select user from input file")
    option = input("Enter a number (0-2): ")

    roll_no = None
    if option == "1":
        roll_no = tutil.generate_roll_number()
        print(f"Generated roll no {roll_no}")
    elif option == "2":
        roll_no = input("Enter roll no: ")
        if not roll_no:
            return
    elif option == "3":
        try:
            user = select_user_from_input_file()
            roll_no = user["roll_no"]
        except CliInvalidChoice:
            print("You have entered an invalid choice.")
            return
    elif option == "0":
        return

    print("="*20)
    try:
        history = client.get_auth_history_by_roll_no(roll_no)
        print(f'User {roll_no} has authenticated {len(history)} times')
        for h in history:
            print(h["timestamp"])
    except UnknownUser:
        print(f"The user {roll_no} does not exist")
    print("="*20)

def main_menu():

    while True:
        print()
        print("-"*20)
        print("Main menu")
        print("0) Quit")
        print("1) Enroll user")
        print("2) Authenticate user")
        print("3) Get authentication history")
        print("4) Generate users to input file")
        choice = input("Enter a number (1-3): ")

        try:
            if choice == "1":
                enroll_user_menu()
            elif choice == "2":
                authenticate_user_menu()
            elif choice == "3":
                get_authentication_history_menu()
            elif choice == "4":
                n = int(input("How many?: "))
                users = []
                for i in range(n):
                    users.append(tutil.generate_random_user())
                with open(input_file, 'w') as file:
                    json.dump(users, file)
                print(f'{n} users generated to {input_file}')
            elif choice == "0":
                print("Exiting")
                return
        except Exception as e:
            print(e)
            print("Oops, something went wrong. Try again")


if __name__ == "__main__":

    main_menu()
