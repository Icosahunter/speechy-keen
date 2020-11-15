""" 
    A module-level object that allows for global data access for the entire app
    
    This data object allows any object in the application to access settings,
    application data, documents (like speech reports), or the current speech
    data (which is manipulated primarily by metric widgets)
"""

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QSettings, QStandardPaths, QVariant
from .speech_data import SpeechData
from enum import Enum
from os import path, makedirs, listdir
import json
from datetime import datetime

settings = QSettings()
current_speech_data = SpeechData()

app_data_location = QStandardPaths.standardLocations(QStandardPaths.AppDataLocation)[0] + '/SpeechyKeen/'
user_data_location = QStandardPaths.standardLocations(QStandardPaths.DocumentsLocation)[0] + '/SpeechyKeen/'
settings_location = settings.fileName()
print('Data: ' + app_data_location)
print('Documents: ' + user_data_location)


def store_data(key, data):
    """ 
        Store data under a certain key

        The key should be formatted similar to a path with '/' delimeters.
        The first part of the key determines how it is stored. This will either
        be 'settings', 'app_data', or 'documents'. Settings is stored through
        Qt's built in settings object, while app_data and documents are stored
        in the file system as JSON files.
    """

    saved_path = None
    setting_type = key.split('/')[0]
    key_path = '/'.join(key.split('/')[1:])

    if setting_type == 'settings':
        settings.setValue(key_path, data)

    elif setting_type == 'documents':
        saved_path = write_to_file(user_data_location + key_path + '.json', json.dumps(data, indent=4, sort_keys=True))

    elif setting_type == 'app_data':
        saved_path = write_to_file(app_data_location + key_path + '.json', json.dumps(data, indent=4, sort_keys=True))

    else:
        raise ValueError()

    return saved_path


def get_data(key):
    """ 
        Get data using it's key

        See "store_data" for details on key format
    """

    setting_type = key.split('/')[0]
    key_path = '/'.join(key.split('/')[1:])

    if setting_type == 'settings':
        try:
            return settings.value(key_path)
        except:
            return None

    elif setting_type == 'app_data':
        try:
            with open(app_data_location + key_path + '.json', 'r') as f:
                return json.loads(f.read())
        except FileNotFoundError:
            return None

    elif setting_type == 'documents':
        try:
            with open(user_data_location + key_path + '.json', 'r') as f:
                return json.loads(f.read())
        except FileNotFoundError:
            return None
    
    else:
        raise ValueError()


def get_data_keys(key):

    """
        Get's a list of keys that start with the given key.

        For data stored as JSON files this amounts to searching
        the path that the given key represents for any JSON files
        located there.
    """

    setting_type = key.split('/')[0]
    key_path = '/'.join(key.split('/')[1:])

    if setting_type == 'settings':
        try:
            return [x[len(key_path):] for x in settings.allKeys() if x.startswith(key_path)]
        except FileNotFoundError:
            return []

    elif setting_type == 'app_data':
        try:
            return [x.split('.')[0] for x in listdir(app_data_location + key_path) if x.split('.')[1] == 'json']
        except:
            return []

    elif setting_type == 'documents':
        try:
            return [x.split('.')[0] for x in listdir(user_data_location + key_path) if x.split('.')[1] == 'json']
        except:
            return []

    else:
        raise ValueError()


def get_data_list(key):
    """
        Get all data objects who's keys start with the given key.

        For data stored as JSON files this amounts to searching
        the path that the given key represents for any JSON files
        located there and returning the parsed JSON object for those
        files.
    """

    data_list = []

    for k in get_data_keys(key):
        data_list += get_data(key + k)
    
    return data_list


def write_to_file(file_path, str_to_write, overwrite_warning=True):
    """
        A safe file writing function used when 'store_data' is called.

        This function creates a directory if it doesn't exist, and if
        overwrite_warning is true it will show a dialog to the user
        if the file exists and hence writing to it would overwrite existing
        data.
    """

    directory = '/'.join(file_path.split('/')[0:-1])

    abort = False
    
    # If overwrite warning is enabled, and a warning window needs to be 
    # displayed then handle the warning
    if path.exists(file_path) and overwrite_warning:
        msg = QMessageBox()
        msg.setText('A file with the same name already exists!')
        overwrite = msg.addButton('Overwrite', QMessageBox.DestructiveRole)
        save_new = msg.addButton('Save as new', QMessageBox.AcceptRole)
        cancel = msg.addButton('Cancel', QMessageBox.RejectRole)
        msg.setDefaultButton(QMessageBox.AcceptRole)
        msg.exec()

        if msg.clickedButton() == save_new:

            file_name = (file_path.split('/')[-1]).split('.')[0]
            file_ext = (file_path.split('/')[-1]).split('.')[1]
            i = 0

            while path.exists(directory + '/' + file_name + ' (' + str(i) + ').' + file_ext):
                i += 1

            file_path = directory + '/' + file_name + ' (' + str(i) + ').' + file_ext

        if msg.clickedButton() == cancel:
            abort = True

    # If the user did not abort the save during overwrite
    # warning, then save the file
    if not abort:

        if not path.exists(directory):
            makedirs(directory)

        with open(file_path, 'w') as f:
            f.write(str_to_write)

        return file_path
