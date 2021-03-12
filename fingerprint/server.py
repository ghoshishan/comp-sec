from db import Database

database = Database()

class Server():
    def store_template(user_tid,template_fingerprint):
        return db.store_credentials(user_tid,template_fingerprint)

    def retrieve_template(user_tid):
        return db.retrieve_credentials(user_tid)

    def compute_euclidean(transformed_fingerprint, template_fingerprint):
        pass 

    def make_decision(euclidean_distance):
        pass 

