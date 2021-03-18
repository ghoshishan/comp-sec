import json

from client.client import Client
client = Client()
import test.util as tutil

from client.exceptions import AuthFailed, DuplicateUser, UnknownUser, WrongPin

# TODO: take parameters from config
pin_length = 4
fingerprint_length = 12
fingerprint_range = (0, 255)

def parse_input(file_name):
    with open(f'test/{file_name}') as file:
        data = json.load(file)
    return data

def print_user(user):
    print("Roll no:\t", user["roll_no"])
    print("Pin:\t\t", user["pin"])
    print("Fingerprint:\t", " ".join([str(x) for x in user["fingerprint"]]))

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
    option = input("Enter a number (0-2): ")

    user = None
    if option == "1":
        user = tutil.generate_random_user()
        print("Generated random user with following details")
        print_user(user)
        pass
    elif option == "2":
        user = enter_user_data()
        pass
    elif option == "0":
        return

    print("="*20)
    try:
        client.enroll(user)
        print(f'{user["roll_no"]} has been enrolled successfully')
    except (DuplicateUser, ):
        print("User already exists:", user["roll_no"])
    except Exception:
        print("Oops, something went wrong.")
    print("="*20)

def authenticate_user_menu():
    print()
    print("Authenticate user menu")
    print("0) Go back to main menu")
    print("1) Generate random user")
    print("2) Give user data manually")
    option = input("Enter a number (0-2): ")

    user = None
    if option == "1":
        user = tutil.generate_random_user()
        print("Generated random user with following details")
        print_user(user)
        pass
    elif option == "2":
        user = enter_user_data()
        pass
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
    except Exception:
        print("Oops, something went wrong.")
    print("="*20)

def get_authentication_history_menu():
    print()
    print("Get authentication history menu")
    print("0) Go back to main menu")
    print("1) Generate a random roll no")
    print("2) Enter roll no manually")
    option = input("Enter a number (0-2): ")

    roll_no = None
    if option == "1":
        roll_no = tutil.generate_roll_number()
        print(f"Generated roll no {roll_no}")
    elif option == "2":
        roll_no = input("Enter roll no: ")
        if not roll_no:
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
    except Exception:
        print("Oops, something went wrong.")
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
        choice = input("Enter a number (1-3): ")

        if choice == "1":
            enroll_user_menu()
        elif choice == "2":
            authenticate_user_menu()
        elif choice == "3":
            get_authentication_history_menu()
        elif choice == "0":
            print("Exiting")
            return


if __name__ == "__main__":

    main_menu()
