import json
import base64
import random
import logging

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from phe import paillier, EncryptedNumber, PaillierPublicKey
import client.dbhandler as dbhandler

from client.exceptions import WrongPin, UnknownUser

logger = logging.getLogger('client')

# for salting pins of users
SALT = b'=sNmXf\xd6\xefe\xf8\xd0\x10\xe5\xb2\xf3o\x01|\xf3\x99\xbf\xd6\x88\x0c\xb6\x9b\x08\xb3\xac\xf0\xb9g'


def generate_verification_code():
    """
    Generates a list of random numbers which is used to transform
    the fingerprint vector to protect against malicious users
    who have access to the fingerprint data of the user they want to impersonate.

    :return: user verification code
    """
    user_vcode = random.sample(range(1, 255), 4)
    return user_vcode

def generate_shuffle_code():
    """
    Returns a random shuffle code.

    :return: shuffle code
    """
    user_shuffle_code = random.randint(1000, 9999)
    return user_shuffle_code

def enrollment_transform(user_fingerprint, user_vcode, user_shuffle_code):
    """
    Performs fingerprint transform during enrollment

    :param user_fingerprint: fingerprint feature vector
    :param user_vcode: verification code of the user
    :return: transformed fingerprint vector
    """
    transformed_fingerprint = user_fingerprint + user_vcode
    sumOfXiSquare = sum(x*x for x in user_fingerprint)
    sumOfViSquare = sum(v*v for v in user_vcode)
    transformed_fingerprint.extend([1, 1, sumOfXiSquare, sumOfViSquare])
    random.Random(user_shuffle_code).shuffle(transformed_fingerprint)
    return transformed_fingerprint


def string_encrypt(pin, plaintext):
    """
    Performs AES encryption based on a pin.
    Used for storing paillier key pair and verification code of a user.

    :param pin: 4 digit integer string
    :param plaintext: JSON dumps of reaquired data to be encrypted
    :return: ciphertext and initialization vector
    """
    key = PBKDF2(pin, SALT, dkLen=32)
    data = plaintext.encode('utf-8')
    # CFB basically doesn't require padding to maintain block size
    cipher_encrypt = AES.new(key, AES.MODE_CFB)
    ciphered_bytes = cipher_encrypt.encrypt(data)
    iv = cipher_encrypt.iv
    return ciphered_bytes, iv


def string_decrypt(pin, iv, ciphertext):
    """
    Performs AES decryption on a ciphertext given a pin and iv.

    :param pin: 4 digit integer string
    :param iv: Initialization vector returned during encryption
    :param ciphertext: encrypted cipher text
    :return: decrypted string data
    """
    key = PBKDF2(pin, SALT, dkLen=32)
    cipher_decrypt = AES.new(key, AES.MODE_CFB, iv)
    deciphered_bytes = cipher_decrypt.decrypt(ciphertext)
    try:
        decrypted_data = deciphered_bytes.decode('utf-8')
    except UnicodeDecodeError as e:
        logger.info(f'Incorrect pin')
        return None
    return decrypted_data


def paillier_encrypt_vector(pub_key, transformed_fingerprint):
    """
    Performs encryption on the transformmed fingerprint
    using the paillier cryptosystem.

    :param pub_key: public key of the user
    :param transformed_fingerprint: a fingerprint feature vector
    :return: encrypted feature vector
    """
    encrypted_fingerprint = [pub_key.encrypt(
        feature) for feature in transformed_fingerprint]
    serialized_fingerprint = []  # readable form of the ciphertext
    for entry in encrypted_fingerprint:
        serialized_fingerprint.append(entry._EncryptedNumber__ciphertext)
    logger.debug(json.dumps(serialized_fingerprint, indent=2))
    return encrypted_fingerprint


def store_credentials(user_roll_no, user_pin, user_tid, user_pub_key, user_priv_key, user_vcode, user_shuffle_code):
    """
    Store credentials of the user in an encrypted format.

    :param user_roll_no: user roll no
    :param user_pin: user 4 digit integer pin
    :param user_tid: user fingerprint id stored on the server
    :param user_pub_key: user paillier public key
    :param user_priv_key: user paillier private key
    :param user_vcode: user verification code
    """
    data = dbhandler.read_data('userdata.json')
    user_data = {
        'tid': user_tid,
        'vcode': user_vcode,
        'scode': user_shuffle_code,
        'n': user_pub_key.n,
        'p': user_priv_key.p,
        'q': user_priv_key.q
    }
    user_data_string = json.dumps(user_data)
    ciphertext, iv = string_encrypt(user_pin, user_data_string)
    store_data = {
        'roll_no': user_roll_no,
        'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
        'iv': base64.b64encode(iv).decode('utf-8')
    }
    data.append(store_data)
    dbhandler.write_data(data, 'userdata.json')
    logger.info(f'User data stored: {user_roll_no}')


def retrieve_credentials(user_roll_no, user_pin):
    """
    Fetch and decrypt encrypted user data stored in the database

    :param user_roll_no: user roll number
    :param user_pin: user pin
    :return: decrypted data
    """
    data = dbhandler.read_data('userdata.json')
    ciphertext = None
    iv = None
    flag = 0
    for user in data:
        if user['roll_no'] == user_roll_no:
            ciphertext = base64.b64decode(user['ciphertext'].encode('utf-8'))
            iv = base64.b64decode(user['iv'].encode('utf-8'))
            flag = 1
            break
    if flag == 0:
        print(f'Unknown user: {user_roll_no}')
        raise UnknownUser
        return None
    user_data = string_decrypt(user_pin, iv, ciphertext)
    if not user_data:
        print(f'Incorrect pin: {user_roll_no}')
        raise WrongPin
        return None
    user_data = json.loads(user_data)
    return user_data


def verification_transform(user_fingerprint, user_vcode, user_shuffle_code):
    """
    Performs transformation on the fingerprint feature vector
    required during verification.

    :param user_fingerprint: fingerprint feature vector
    :param user_vcode: verification code of the user
    :return: transformed fingerprint
    """
    # is not this same as enrollment_transform
    transformed_fingerprint = user_fingerprint + user_vcode
    transformed_fingerprint = [-2*n for n in transformed_fingerprint]
    sumOfYiSquare = sum(y*y for y in user_fingerprint)
    sumOfViSquare = sum(v*v for v in user_vcode)
    transformed_fingerprint.extend([sumOfYiSquare, sumOfViSquare, 1, 1])
    random.Random(user_shuffle_code).shuffle(transformed_fingerprint)
    return transformed_fingerprint
