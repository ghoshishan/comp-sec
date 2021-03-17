import json

from client.client import Client
client = Client()

from client.exceptions import AuthFailed, DuplicateUser, UnknownUser, WrongPin

def parse_input(file_name):
    with open(f'tests/{file_name}') as file:
        data = json.load(file)
    return data

print('Enrollment:')
enroll_list = parse_input('enroll-input-list.json')
for user in enroll_list:
    try:
        client.enroll(user)
    except (DuplicateUser, ):
        print("Exception occured!")
print()

print('Verification:')
verify_list = parse_input('verify-input-list.json')
for user in verify_list:
    try:
        client.verify(user)
    except (AuthFailed, WrongPin, UnknownUser):
        print("Exception occured!")
print()

print('Fetch history')
client.get_auth_history()
