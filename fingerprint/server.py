import json
import logging

from phe import paillier


class Server():
    """
    Implements functionality related to cloud biometric storage and processing.
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

    def store_template(self, encrypted_fingerprint):
        """
        Receives a encrypted transformed fingerprint from the client.
        Fingerprint is homomorphically encrypted using the paillier
        scheme which allows the server to perform certain operations on
        encrypted data.
        This data is stored in a database.

        :param template_fingerprint: encrypted fingerprint template
        :return: template id of the template
        """
        with open('server-data/templates.json') as file:
            data = json.load(file)

        self.tid = self.tid + 1
        serializable_encrypted_fingerprint = [
            feature._EncryptedNumber__ciphertext for feature in encrypted_fingerprint]
        new_template = {'tid': self.tid,
                        'fingerprint': serializable_encrypted_fingerprint}
        data.append(new_template)
        with open('server-data/templates.json', 'w') as file:
            json.dump(data, file, indent=2)

        self.logger.info('New template stored')
        self.logger.debug(json.dumps(new_template, indent=2))

        return self.tid

    def retrieve_template(self, user_tid):
        return database.retrieve_template(user_tid)

    def compute_euclidean(self, transformed_fingerprint, template_fingerprint):
        pass

    def make_decision(self, euclidean_distance):
        pass

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
    server.store_template(encrypted_X)
