from server import Server
from client import Client

server = Server()
client = Client()

class EnrollFailed(Exception):
    pass

def parse_input():
    pass

# Take inputs
enroll_list = parse_input()

def enroll(item):
    
    # Note: Raise EnrollFailed Exception if any of these functions fail

    # Client side
    user_roll_no = item.roll_no
    user_pin = item.pin
    user_fingerprint = item.fingerprint

    user_key_pair = client.paillier_generate_keypair()
    user_vcode = client.generate_verification_code()

    transformed_fingerprint = client.enrollment_transform(user_fingerprint, verification_code)
    template_fingerprint = client.paillier_encrypt_vector(user_key_pair[0], transformed_fingerprint)

    # Server side
    user_tid = server.store_template(template_fingerprint)

    # Client side
    client.store_credentials(user_roll_no, user_pin, user_tid, user_key_pair, user_vcode)

# For each user
for item in enroll_list:

    try:
        enroll(item)
        print("Enrolled user", user.roll_no)
    except EnrollFailed:
        print("Could not enroll user", user.roll_no)