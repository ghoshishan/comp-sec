import json
import pathlib
import logging

logger = logging.getLogger('client')

def read_data(file_name):
    """
    Read a JSON file and return its content.
    If the file is not present create a new empty file.
    If the data in it is invalid create a new empty file.

    :param file_name: Name of the file
    :return: Data content of the file
    """
    file_path = pathlib.Path(__file__).parent / f'data/{file_name}'
    try:
        with open(file_path) as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        # json decode error happens when file is empty
        data = []
        with open(file_path, 'w') as file:
            json.dump(data, file)
        logger.error(f'New empty file created. Error: {e}')

    return data


def write_data(data, file_name):
    """
    Write JSON data to a file

    :param data: Data to be written to the file
    :param file_name: Name of the file
    """
    file_path = pathlib.Path(__file__).parent / f'data/{file_name}'
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)
