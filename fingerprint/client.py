import json
import base64
import random

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from phe import paillier, EncryptedNumber, PaillierPublicKey

SALT = b'=sNmXf\xd6\xefe\xf8\xd0\x10\xe5\xb2\xf3o\x01|\xf3\x99\xbf\xd6\x88\x0c\xb6\x9b\x08\xb3\xac\xf0\xb9g'

class Client():

    def generate_verification_code(self):
        user_vcode = random.sample(range(1, 255), 4)
        return user_vcode

    def enrollment_transform(self, user_fingerprint, user_vcode):
        transformed_fingerprint = user_fingerprint + user_vcode
        sumOfXiSquare = sum(x*x for x in user_fingerprint)
        sumOfViSquare = sum(v*v for v in user_vcode)
        transformed_fingerprint.extend([1, 1, sumOfXiSquare, sumOfViSquare])
        return transformed_fingerprint

    def string_encrypt(self, pin, plaintext):
        key = PBKDF2(pin, SALT, dkLen=32)
        data = plaintext.encode('utf-8')
        cipher_encrypt = AES.new(key, AES.MODE_CFB)
        ciphered_bytes = cipher_encrypt.encrypt(data)
        iv = cipher_encrypt.iv
        return ciphered_bytes, iv

    def string_decrypt(self, pin, iv, ciphertext):
        key = PBKDF2(pin, SALT, dkLen=32)
        cipher_decrypt = AES.new(key, AES.MODE_CFB, iv)
        deciphered_bytes = cipher_decrypt.decrypt(ciphertext)
        decrypted_data = deciphered_bytes.decode('utf-8')
        return decrypted_data

    def paillier_encrypt_vector(self, pub_key, transformed_fingerprint):
        return [pub_key.encrypt(feature) for feature in transformed_fingerprint]

    def store_credentials(self, user_roll_no, user_pin, user_tid, user_pub_key, user_priv_key, user_vcode):
        with open('client-data/userdata.json') as file:
            data = json.load(file)
        user_data = {
            'tid': user_tid,
            'vcode': user_vcode,
            'n': user_pub_key.n,
            'p': user_priv_key.p,
            'q': user_priv_key.q
        }
        user_data_string = json.dumps(user_data)
        ciphertext, iv = self.string_encrypt(user_pin, user_data_string)
        store_data = {
            'roll_no': user_roll_no,
            'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
            'iv': base64.b64encode(iv).decode('utf-8')
        }
        data.append(store_data)
        with open('client-data/userdata.json', 'w') as file:
            json.dump(data, file, indent=2)

    def retrieve_credentials(self, user_roll_no, user_pin):
        with open('client-data/userdata.json') as file:
            data = json.load(file)
        ciphertext = None
        iv = None
        for user in data:
            if user['roll_no'] == user_roll_no:
                ciphertext = base64.b64decode(user['ciphertext'].encode('utf-8'))
                iv = base64.b64decode(user['iv'].encode('utf-8'))
        user_data = self.string_decrypt(user_pin, iv, ciphertext)
        user_data = json.loads(user_data)
        return user_data

    def verification_transform(self, user_fingerprint, user_vcode):
        # is not this same as enrollment_transform
        transformed_fingerprint = user_fingerprint + user_vcode
        transformed_fingerprint = [-2*n for n in transformed_fingerprint]
        sumOfYiSquare = sum(y*y for y in user_fingerprint)
        sumOfViSquare = sum(v*v for v in user_vcode)
        transformed_fingerprint.extend([sumOfYiSquare, sumOfViSquare, 1, 1])
        return transformed_fingerprint
