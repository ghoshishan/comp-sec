from db import DatabaseClient

database = DatabaseClient()


class Client():
    def paillier_generate_keypair(self):
        # Returns a two tuple (public_key, private_key)
        pass

    def generate_verification_code(self):
        pass 
    
    def enrollment_transform(self, user_fingerprint, user_vcode):
        pass

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
        pass 



    