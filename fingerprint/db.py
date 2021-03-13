# not neccearily a database can be handled as file io as well


class DatabaseServer:    

    def store_template(self, template_fingerprint):
        pass 

    def retrieve_template(self, user_tid):
        pass 

class DatabaseClient:    

    def store_credentials(self, user_roll_no, user_pin, user_tid, user_key_pair, user_vcode):
        pass

    def retrieve_credentials(self, user_roll_no, user_pin):
        pass
