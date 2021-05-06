import json
import pathlib
import logging

FILE_NAME = pathlib.Path(__file__).parent / 'data/templates.json'

logger = logging.getLogger('server')


def read_data():
    """
    Read a JSON file and return its content.
    If the file is not present create a new empty file.
    If the data in it is invalid create a new empty file.

    :return: JSON data
    """
    try:
        with open(FILE_NAME) as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        # json decode error happens when file is empty
        data = []
        with open(FILE_NAME, 'w') as file:
            json.dump(data, file)
        logger.error(f'New empty file created. Error: {e}')
    return data


def write_data(data):
    """
    Write JSON data to a file

    :param data: JSON data to be written
    """
    with open(FILE_NAME, 'w') as file:
        json.dump(data, file, indent=2)
