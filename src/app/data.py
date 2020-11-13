from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QSettings, QStandardPaths, QVariant
from enum import Enum
from os import path, makedirs, listdir
import json
from datetime import datetime

settings = QSettings()

SettingType = Enum('SettingType', 'setting config user_data app_data')

current_speech_data = {
    'stream_data' : {},
    'single_data' : {}
}

_collecting_speech_data = False
_cumul_time = datetime.now()
_lap_time = datetime.now()

app_data_location = QStandardPaths.standardLocations(QStandardPaths.AppDataLocation)[0] + '/SpeechyKeen/'
app_config_location = QStandardPaths.standardLocations(QStandardPaths.AppConfigLocation)[0] + '/SpeechyKeen/'
user_data_location = QStandardPaths.standardLocations(QStandardPaths.DocumentsLocation)[0] + '/SpeechyKeen/'
print('Config: ' + app_config_location)
print('Data: ' + app_data_location)
print('Documents: ' + user_data_location)

def set_time_keeping(cumul_time, lap_time):
    global _cumul_time, _lap_time
    _cumul_time = cumul_time
    _lap_time = lap_time

def get_timestamp():
    global _cumul_time, _lap_time
    return int((_cumul_time + (datetime.now() - _lap_time)).total_seconds())

def begin_speech_data_collection():
    global _collecting_speech_data
    _collecting_speech_data = True
    submit_speech_single_data('date', datetime.now().strftime('%m-%d-%YT%H%M%S'))

def stop_speech_data_collection():
    global _collecting_speech_data
    _collecting_speech_data = False

def create_speech_data_stream(stream_name, main_data_key, colors_dict):
    global current_speech_data
    stream = {'main_data' : main_data_key, 'colors' : colors_dict, 'stream' : []}
    current_speech_data['stream_data'][stream_name] = stream

def submit_speech_stream_data(key, data_dict):
    global current_speech_data, _collecting_speech_data
    if _collecting_speech_data:
        data = {'time_stamp' : get_timestamp()}
        for d in data_dict:
            data[d] = data_dict[d]
        current_speech_data['stream_data'][key]['stream'].append(data)

def undo_last_speech_stream_data(key):
    global current_speech_data, _collecting_speech_data
    if _collecting_speech_data:
        current_speech_data.popitem()

def submit_speech_single_data(key, data):
    global current_speech_data
    #if _collecting_speech_data:
    current_speech_data['single_data'][key] = data

def get_speech_single_data(key):
    global current_speech_data
    return current_speech_data['single_data'][key]

def get_speech_stream_data(key, index):
    global current_speech_data
    return current_speech_data['stream_data'][key]['stream'][index]

def get_speech_report():
    return current_speech_data

def get_speech_report_file_name():
    return get_speech_single_data('date')

def store_data(key, data, setting_type):

    saved_path = None

    if setting_type == SettingType.setting:
        settings.setValue(key, data)
        
    elif setting_type == SettingType.config:
        saved_path = write_to_file(app_config_location + key + '.json', json.dumps(data, indent=4, sort_keys=True))

    elif setting_type == SettingType.user_data:
        saved_path = write_to_file(user_data_location + key + '.json', json.dumps(data, indent=4, sort_keys=True))

    elif setting_type == SettingType.app_data:
        saved_path = write_to_file(app_data_location + key + '.json', json.dumps(data, indent=4, sort_keys=True))

    return saved_path

def get_data(key):
    if not settings.value(key) is None:
        return settings.value(key)
    else:
        try:
            with open(app_config_location + key + '.json', 'r') as f:
                return json.loads(f.read())
        except:
            try:
                with open(app_data_location + key + '.json', 'r') as f:
                    return json.loads(f.read())
            except:
                try:
                    with open(user_data_location + key + '.json', 'r') as f:
                        return json.loads(f.read())
                except:
                    raise FileNotFoundError()

def get_data_keys(key):

    keys_list = []
    try:
        keys_list.extend([x.split('.')[0] for x in listdir(app_config_location + key) if x.split('.')[1] == 'json'])
    except FileNotFoundError:
        pass

    try:
        keys_list.extend([x.split('.')[0] for x in listdir(app_data_location + key) if x.split('.')[1] == 'json'])
    except FileNotFoundError:
        pass
    
    try:
        keys_list.extend([x.split('.')[0] for x in listdir(user_data_location + key) if x.split('.')[1] == 'json'])
    except FileNotFoundError:
        pass

    return keys_list

def get_data_list(key):

    data_list = []

    for file_name in listdir(app_config_location + key):
        try:
            with open(app_config_location + key + file_name, 'r') as f:
                data_list += json.loads(f.read())
        except:
            pass
    for file_name in listdir(app_data_location + key):
        try:
            with open(app_data_location + key + file_name, 'r') as f:
                data_list += json.loads(f.read())
        except:
            pass
    for file_name in listdir(user_data_location + key):
        try:
            with open(user_data_location + key + file_name, 'r') as f:
                data_list += json.loads(f.read())
        except:
            pass
    
    return data_list


def write_to_file(file_path, str_to_write, overwrite_warning=True):

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
