import json

from server import Server
from client import Client

from phe import paillier

server = Server()
client = Client()

def parse_input():
    with open('enroll_input_list.json') as file:
        data = json.load(file)
    return data

def enroll(user):
    user_roll_no = user['roll_no']
    user_pin = user['pin']
    user_fingerprint = user['fingerprint']
    user_pub_key, user_priv_key = paillier.generate_paillier_keypair()
    user_vcode = client.generate_verification_code()

    transformed_fingerprint = client.enrollment_transform(user_fingerprint, user_vcode)
    encrypted_fingerprint = client.paillier_encrypt_vector(user_pub_key, transformed_fingerprint)

    user_tid = server.store_template(encrypted_fingerprint, user_pub_key.n)

    client.store_credentials(user_roll_no, user_pin, user_tid, user_pub_key, user_priv_key, user_vcode)


if __name__ == '__main__':
    enroll_list = parse_input()
    for user in enroll_list:
        try:
            enroll(user)
            print(f"Enrolled user: {user['roll_no']}")
        except Exception as e:
            print(f"Enrollment failed: {user['roll_no']}")
            raise Exception(e)
