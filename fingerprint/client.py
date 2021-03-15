from db import DatabaseClient

database = DatabaseClient()


class Client():
    def paillier_generate_keypair(self):
        # Returns a two tuple (public_key, private_key)
        pass

    def generate_verification_code(self):
        user_vcode = random.sample(range(1, 255), 4)
        return user_vcode

    def enrollment_transform(self, user_fingerprint, user_vcode):
        transformed_fingerprint = user_fingerprint + user_vcode
        sumOfXiSquare = sum(x*x for x in user_fingerprint)
        sumOfViSquare = sum(v*v for v in user_vcode)
        transformed_fingerprint.extend([1,1,sumOfXiSquare, sumOfViSquare])
        return transformed_fingerprint

    def paillier_encrypt(self, pub_key, plaintxt):
        pass

    def paillier_decrypt(self, priv_key, cipher):
        pass

    def paillier_encrypt_vector(self, pub_key, transformed_fingerprint):
        # Return component wise encrypted vector
        pass

    def store_credentials(self, user_roll_no, user_pin, user_tid, user_key_pair, user_vcode):
        return database.store_credentials(user_roll_no, user_pin, user_tid, user_key_pair, user_vcode)

    def retrieve_credentials(self,user_roll_no, user_pin):
        return database.retrieve_credentials(user_roll_no, user_pin)

    def verification_transform(self,user_fingerprint, user_vcode):
        # is not this same as enrollment_transform
        transformed_fingerprint = user_fingerprint + user_vcode
        transformed_fingerprint = [ -2*n for n in transformed_fingerprint]
        sumOfYiSquare = sum(y*y for y in user_fingerprint)
        sumOfViSquare = sum(v*v for v in user_vcode)
        transformed_fingerprint.extend([sumOfYiSquare, sumOfViSquare,1, 1])
        return transformed_fingerprint

    def mark_authentication(self, user_roll_no):
        # Record the timestamp of authentication
        db.mark_authentication(user_roll_no)
        return

    def get_auth_history(self, user_roll_no):
        # Return array of timestamps at which user has authenticated
        return db.get_auth_history(user_roll_no)



