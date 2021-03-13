from server import Server
from client import Client

server = Server()
client = Client()

class NoRecord(Exception):
    pass

def human_readable_time(timestamp):
    pass

if __name__ == "__main__":

    while(True):
        try:

            # Client side
            user_roll_no = input("Enter a roll no: ")
            
            # Server side
            timestamps = server.get_auth_history(user_roll_no)

            # Client side

            for t in timestamps:
                print(human_readable_time(t))

        except NoRecord:
            print("No record found!")
        