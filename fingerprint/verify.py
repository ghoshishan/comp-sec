from server import Server
from client import Client

server = Server()
client = Client()

class AuthFailed(Exception):
    pass

def parse_input():
    pass

if __name__ == "__main__":

    # Take inputs
    verification_list = parse_input()

    def authenticate(item):
        
        # Note: Raise AuthFailed Exception if authentication fails in any function

        # Client side
        user_roll_no = item.roll_no
        user_pin = item.pin
        user_fingerprint = item.fingerprint

        user_tid, user_key_pair, user_vcode = client.retrieve_credentials(user_roll_no, user_pin)
        transformed_fingerprint = client.verification_transform(user_fingerprint, user_vcode)

        # Server side
        template_fingerprint = server.retrieve_template(user_tid)
        euclidean_distance_cipher = server.compute_euclidean(transformed_fingerprint, template_fingerprint)

        # Client side
        euclidean_distance = client.paillier_decrypt(user_key_pair[1], euclidean_distance_cipher)

        # Server side
        if server.make_decision(euclidean_distance):
            return
        else:
            raise AuthFailed



    for item in verification_list:
        try:
            authenticate(item)
            print("Authenticated", user.roll_no)
        except AuthFailed:
            print("Could not authenticate", user.roll_no)
        except:
            print("Error occured!")