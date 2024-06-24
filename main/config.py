#!/usr/bin/env python3

import os
import configparser
from ast import literal_eval

class ConfigReaderError(Exception): pass

class ConfigReader:
    def __init__(self, filename):
        filename = os.path.expanduser(filename)
        if not os.path.exists(filename):
            raise FileNotFoundError("File {} not found".format(filename))

        self.filename = filename
        self.config = configparser.ConfigParser()
        self.config.read(filename)

    def sections(self):
        return self.config.sections()

    def get_value(self, section, key):
        try:
            value = self.config.get(section, key)
            return literal_eval(value)
        except ValueError:
            print(f"Error: Unable to evaluate the literal for {section}.{key}. Returning the raw value.")
            return value
        except (SyntaxError, configparser.NoOptionError, configparser.NoSectionError) as e:
            print(f"Error: {e}. Returning the raw value.")
            return value

    def get_directory(self, section, key):
        directory = self.get_value(section, key)
        directory = os.path.expanduser(directory)
        return directory
    
    def get_filename(self, section, key):
        filename = self.get_value(section, key)
        filename = os.path.expanduser(filename)
        return filename
