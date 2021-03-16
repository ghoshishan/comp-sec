import json

from client.client import Client

client = Client()

def parse_input(file_name):
    with open(f'tests/{file_name}') as file:
        data = json.load(file)
    return data

print('Enrollment:')
enroll_list = parse_input('enroll-input-list.json')
for user in enroll_list:
    client.enroll(user)
print()

print('Verification:')
verify_list = parse_input('verify-input-list.json')
for user in verify_list:
    client.verify(user)
print()

print('Fetch history')
client.get_auth_history()
