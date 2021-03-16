
import json

if __name__ == "__main__":
    with open('client-data/authhistory.json') as file:
        data = json.load(file)

    roll_no = input('Enter roll no to search: ')
    history = []
    for entry in data:
        if entry['roll_no'] == roll_no:
            print(entry['timestamp'])
            history.append(entry)

    if not history:
        print('No entry found')
