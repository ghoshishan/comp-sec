import json
import logging

from phe import paillier, EncryptedNumber, PaillierPublicKey


class Server():
    """
    Implements functionality related to cloud biometric storage and processing.

    Return values to the client:
        store_template():
            <int> tid (template id)
                if template succesfully stored in the database file
            <None>
                if error during store occurs

        calculate_eucledian():
            <int> encrypted_eucledian_distance
                Ciphertext which contains the encrypted eucledian distance
            <None>
                if error during calculation occurs

        make_decision():
            <True> given unencrypted eucledian distance
                returns if the value is within threshold
            <False>
                if the value is not withing threshold

    """

    def __init__(self):
        """
        Constructor executed during object creation
        """
        self.logger = self.get_logger()  # for server logs

        try:
            with open('server-data/templates.json') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            # json decode error happens when file is empty
            data = []
            with open('server-data/templates.json', 'w') as file:
                json.dump(data, file)
            self.logger.error(e)

        if not data:
            self.tid = 0
        else:
            last_entry = data[-1]  # fetch the last appended tid
            self.tid = last_entry['tid']

    def store_template(self, encrypted_fingerprint, pub_key_n):
        """
        Receives a encrypted transformed fingerprint from the client.
        Fingerprint is homomorphically encrypted using the paillier
        scheme which allows the server to perform certain operations on
        encrypted data.
        This data is stored in a database.

        :param template_fingerprint: encrypted fingerprint template
        :param pub_key_n:
        :return: template id of the template stored, None if error
        """
        with open('server-data/templates.json') as file:
            data = json.load(file)

        self.tid = self.tid + 1

        try:
            serializable_encrypted_fingerprint = [
                feature._EncryptedNumber__ciphertext for feature in encrypted_fingerprint]
            new_template = {'tid': self.tid,
                            'fingerprint': serializable_encrypted_fingerprint,
                            'public_key': pub_key_n}
            data.append(new_template)
            with open('server-data/templates.json', 'w') as file:
                json.dump(data, file, indent=2)
        except Exception as e:
            self.logger.exception(e)
            raise Exception(e)
            return None

        self.logger.info('New template stored')
        self.logger.debug(json.dumps(new_template, indent=2))

        return self.tid

    def retrieve_template(self, user_tid):
        """
        Retrieves encrypted fingerprint vector given a particular
        template id.

        :param user_tid: template id of the user from client
        :return: fingerprint template if it exists else None
        """
        with open('server-data/templates.json') as file:
            data = json.load(file)
        for entry in data:
            if entry['tid'] == user_tid:
                return entry
        # This technically should never happen
        self.logger.error(f'Unknown template id: {user_tid}')
        return None

    def compute_euclidean(self, verification_fingerprint, user_tid):
        """
        Computes the eucledian distance between the verification fingerprint
        and the original fingerprint.

        :param verification_fingerprint: fingerprint transformed vector
            for the user that is to be verified by the client
        :param user_tid: template id of the user being verified
            sent by the client
        :return: encrypted eucledian distance
        """
        template_json = self.retrieve_template(user_tid)
        if not template_json:
            return None
        pub_key = PaillierPublicKey(template_json['public_key'])
        original_fingerprint = [EncryptedNumber(
            pub_key, cipher) for cipher in template_json['fingerprint']]
        if len(verification_fingerprint) != len(original_fingerprint):
            self.logger.error(f'Fingerprint templates size do not match')
            self.logger.debug(
                f'Verification fingerprint {verification_fingerprint}')
            return None
        for idx, feature in enumerate(verification_fingerprint):
            original_fingerprint[idx] = original_fingerprint[idx]*feature
        encrypted_eucledian_distance = 0
        for c in original_fingerprint:
            encrypted_eucledian_distance += c
        return encrypted_eucledian_distance._EncryptedNumber__ciphertext

    def make_decision(self, euclidean_distance):
        """
        Given unencrypted eucledian distance between the original and to be verified fingerprint
        it returns whether the value is withing threshold
        https://www.intechopen.com/books/advanced-biometric-technologies/fingerprint-recognition
        threshold value taken from this website (gm1 = 27)

        :param euclidean_distance: eucledian distance as integer
        :return: True or False
        """
        if euclidean_distance < 27:
            return True
        else:
            return False

    def get_logger(self):
        """
        Create a logging object for server logs

        :return: logger object
        """
        logger = logging.getLogger('server')
        logger.setLevel(level=logging.DEBUG)

        formatter = logging.Formatter(
            '%(asctime)s: %(module)s: [%(levelname)s]: %(message)s')

        file_handler = logging.FileHandler('server-data/server.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return logger


if __name__ == '__main__':
    server = Server()

    pub_key, priv_key = paillier.generate_paillier_keypair()
    X = [22, 53, 61, 62, 74]
    V = [11, 40, 45]
    X_transformed = [22, 53, 61, 62, 74, 11, 40, 45, 1, 1, 16334, 3746]
    encrypted_X = [pub_key.encrypt(i) for i in X_transformed]
    server.store_template(encrypted_X, pub_key.n)

    Y = [21, 52, 61, 62, 74]
    V = [11, 40, 45]
    Y_transformed = [-42, -104, -122, -124, -148, -22, -80, -90, 16186, 3746, 1, 1]
    eucledian_distance = server.compute_euclidean(Y_transformed, server.tid)
    eucledian_distance = priv_key.decrypt(EncryptedNumber(pub_key, eucledian_distance))
    print(eucledian_distance)
    res = server.make_decision(eucledian_distance)
    if res == True:
        print("Authenticated")
    else:
        print("Not Authenticated")
