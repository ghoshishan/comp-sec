class AuthFailed(Exception):
    pass

class DuplicateUser(Exception):
    pass

class WrongPin(Exception):
    pass

class UnknownUser(Exception):
    pass