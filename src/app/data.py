from PyQt5.QtCore import QSettings, QStandardPaths, QVariant
from enum import Enum
from os import path, makedirs
import json

settings = QSettings()

SettingType = Enum('SettingType', 'setting config user_data app_data')

current_speech_data = {}

_collecting_speech_data = False

AppDataLocation = QStandardPaths.standardLocations(QStandardPaths.AppDataLocation)[0] + '/SpeechyKeen/'
AppConfigLocation = QStandardPaths.standardLocations(QStandardPaths.AppConfigLocation)[0] + '/SpeechyKeen/'
UserDataLocation = QStandardPaths.standardLocations(QStandardPaths.DocumentsLocation)[0] + '/SpeechyKeen/'
print('Config: ' + AppConfigLocation)
print('Data: ' + AppDataLocation)
print('Documents: ' + UserDataLocation)

def BeginSpeechDataCollection():
    global _collecting_speech_data
    _collecting_speech_data = True

def StopSpeechDataCollection():
    global _collecting_speech_data
    _collecting_speech_data = False

def CreateSpeechDataStream(stream_name, main_data_key, colors_dict):
    global current_speech_data
    stream = {'main_data' : main_data_key, 'colors' : colors_dict, 'stream' : []}
    current_speech_data['stream_data'][stream_name] = stream

def SubmitSpeechStreamData(key, time_stamp, data_dict):
    global current_speech_data
    if _collecting_speech_data:
        data = {'time_stamp' : time_stamp}
        for d in data_dict:
            data[d] = data_dict[d]
        current_speech_data['stream_data'][key]['stream'] += data

def SubmitSpeechSingleData(key, data):
    global current_speech_data
    if _collecting_speech_data:
        current_speech_data[key] = data

def StoreData(key, data, setting_type):

    if setting_type == SettingType.setting:
        settings.setValue(key, data)
        
    elif setting_type == SettingType.config:
        write_to_file(AppConfigLocation + key + '.json', json.dumps(data))

    elif setting_type == SettingType.user_data:
        write_to_file(UserDataLocation + key + '.json', json.dumps(data))

    elif setting_type == SettingType.app_data:
        write_to_file(AppDataLocation + key + '.json', json.dumps(data))

def GetData(key):
    if not settings.value(key) is None:
        return settings.value(key)
    else:
        try:
            with open(AppConfigLocation + key + '.json', 'r') as f:
                return json.loads(f.read())
        except:
            try:
                with open(AppDataLocation + key + '.json', 'r') as f:
                    return json.loads(f.read())
            except:
                try:
                    with open(UserDataLocation + key + '.json', 'r') as f:
                        return json.loads(f.read())
                except:
                    raise FileNotFoundError()
    
def write_to_file(file_path, str_to_write):

    directory = '/'.join(file_path.split('/')[0:-1])

    if not path.exists(directory):
        makedirs(directory)
    
    with open(file_path, 'w') as f:
        f.write(str_to_write)
