import json
from datetime import datetime

from server import Server
from client import Client

from phe import paillier, EncryptedNumber, PaillierPublicKey, PaillierPrivateKey

server = Server()
client = Client()


def parse_input():
    with open('verify_input_list.json') as file:
        data = json.load(file)
    return data


def authenticate(user):
    user_roll_no = user['roll_no']
    user_pin = user['pin']
    user_fingerprint = user['fingerprint']

    user_data = client.retrieve_credentials(user_roll_no, user_pin)
    if not user_data:
        print("Unknown user")
        return
    user_tid = user_data['tid']
    user_vcode = user_data['vcode']
    user_pub_key = PaillierPublicKey(user_data['n'])
    user_priv_key = PaillierPrivateKey(user_pub_key, user_data['p'], user_data['q'])
    transformed_fingerprint = client.verification_transform(
        user_fingerprint, user_vcode)

    # Server side
    euclidean_distance_cipher = server.compute_euclidean(
        transformed_fingerprint, user_tid)

    # Client side
    euclidean_distance = user_priv_key.decrypt(EncryptedNumber(user_pub_key, euclidean_distance_cipher))
    print(euclidean_distance)
    # Server side
    if server.make_decision(euclidean_distance):
        print("Authenticated")
        with open('client-data/authhistory.json') as file:
            data = json.load(file)
        data.append(
            {
                'roll_no': user_roll_no,
                'timestamp': datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            }
        )
        with open('client-data/authhistory.json', 'w') as file:
            json.dump(data, file, indent=2)
        # Stores timestamp of authentication
        # server.mark_authentication(user_roll_no)
    else:
        print("Not Authenticated")


if __name__ == "__main__":

    # Take inputs
    verification_list = parse_input()

    for user in verification_list:
        authenticate(user)
