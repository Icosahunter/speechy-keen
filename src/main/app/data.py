from PyQt5.QtCore import QSettings, QStandardPaths, QVariant
from enum import Enum

settings = QSettings()

SettingType = Enum('SettingType', 'setting config user_data app_data')

current_speech_data = {}

_collecting_speech_data = False

def BeginSpeechDataCollection():
    global _collecting_speech_data
    _collecting_speech_data = True

def StopSpeechDataCollection():
    global _collecting_speech_data
    _collecting_speech_data = False

def SubmitSpeechStreamData(key, data):
    global current_speech_data
    if _collecting_speech_data:
        if key in current_speech_data:
            current_speech_data[key] += data
        else:
            current_speech_data[key] = [data]

def SubmitSpeechSingleData(key, data):
    global current_speech_data
    if _collecting_speech_data:
        current_speech_data[key] = data

def StoreData(key, data, setting_type):
    if setting_type == SettingType.setting:
        settings.setValue(key, data)
    elif setting_type == SettingType.config:
        raise NotImplementedError()
    elif setting_type == SettingType.user_data:
        raise NotImplementedError()
    elif setting_type == SettingType.app_data:
        raise NotImplementedError()

def GetData(key):
    if not settings.value(key).isNull():
        return settings.value(key)
    else:
        raise NotImplementedError()