import test.util as tutil
import unittest
import os

from client.client import Client
from client.exceptions import AuthFailed, DuplicateUser, WrongPin, UnknownUser
client = Client()

"""
Run python3 run-tests.py

Set verbose = False to print less

"""

verbose = True
def logVerbose(something):
    if (verbose):
        print(str(something))



class TestingIntegration(unittest.TestCase):

    @classmethod
    def cleardb(cls):
        toremove = [
            "client/data/authhistory.json",
            "client/data/userdata.json",
            "server/data/templates.json"
        ]
        for file in toremove:
            if os.path.exists(file):
                os.remove(file)

    @classmethod
    def setUpClass(cls):
        cls.cleardb()

    def test_excact_authentication(self):
        user = tutil.generate_random_user()
        logVerbose("\n#### Exact authentication")
        logVerbose(user)
        client.enroll(user)
        client.verify(user)

    def test_within_threshold_authentication(self):
        logVerbose("\n#### Within threshold authentication")
        user = tutil.generate_random_user()
        client.enroll(user)
        logVerbose(user)
        user["fingerprint"] = tutil.alter_fingerprint(user["fingerprint"], exceed_threshold = False)
        logVerbose(user)
        client.verify(user)

    def test_authentication_exceeding_threshold(self):
        logVerbose("\n#### Exceeding threshold authentication")
        user = tutil.generate_random_user()
        logVerbose(user)
        client.enroll(user)
        user["fingerprint"] = tutil.alter_fingerprint(user["fingerprint"], exceed_threshold = True)
        logVerbose(user)
        try:
            client.verify(user)
            # Test fails here
            raise Exception
        except AuthFailed:
            # Test passes here
            pass

    def test_duplicate_enrollment(self):
        logVerbose("\n#### Duplicate enrollment")
        user = tutil.generate_random_user()
        client.enroll(user)
        try:
            client.enroll(user)
            raise Exception
        except DuplicateUser:
            pass

    def test_wrong_pin_entry(self):
        logVerbose("\n#### Entering wrong pin")
        user = tutil.generate_random_user()
        client.enroll(user)
        user["pin"] = tutil.generate_pin()
        try:
            client.verify(user)
            raise Exception
        except WrongPin:
            pass

    def test_unknown_user(self):
        logVerbose("\n#### Trying to verify unknown user")
        user = tutil.generate_random_user()
        try:
            client.verify(user)
            raise Exception
        except UnknownUser:
            pass

    def test_auth_history(self):
        logVerbose("\n#### Checking authentication history")
        user = tutil.generate_random_user()
        client.enroll(user)
        logVerbose(user)
        attempts = 3
        for i in range(attempts):
            client.verify(user)
        history = client.get_auth_history_by_roll_no(user["roll_no"])
        logVerbose(history)
        self.assertTrue(len(history) == attempts)


    @classmethod
    def tearDownClass(cls):
        cls.cleardb()


if __name__ == "__main__":

    print("Warning: this will delete all entries in current server and client database!")
    res = input("Continue? y/n: ")
    if res == "y":
        unittest.main()
    else:
        print("Operation cancelled")
