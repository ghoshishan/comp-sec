from db import DatabaseServer

database = DatabaseServer()

class Server():
    def store_template(self, template_fingerprint):
        return database.store_template(template_fingerprint)

    def retrieve_template(self, user_tid):
        return database.retrieve_template(user_tid)

    def compute_euclidean(self, transformed_fingerprint, template_fingerprint):
        pass 

    def make_decision(self, euclidean_distance):
        pass 

    def mark_authentication(self, user_roll_no):
        # Record the timestamp of authentication
        pass

    def get_auth_history(self, user_roll_no):
        # Return array of timestamps at which user has authenticated
        pass

