from configparser import ConfigParser
import os

def load_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()

    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, filename)

    parser.read(file_path)

    config = {}
    if parser.has_section(section):
        for param in parser.items(section):
            config[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in {file_path}')
    return config