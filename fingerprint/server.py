from db import DatabaseServer

database = DatabaseServer()

class Server():
    def store_template(template_fingerprint):
        return database.store_credentials(user_tid,template_fingerprint)

    def retrieve_template(user_tid):
        return database.retrieve_credentials(user_tid)

    def compute_euclidean(user_key, template_fingerprint):
        pass 

    def make_decision(euclidean_distance):
        pass 

