from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QSettings, QStandardPaths, QVariant, pyqtSignal
from enum import Enum
from os import path, makedirs, listdir
import json
from datetime import datetime

current_speech_data = {
    'stream_data' : {},
    'single_data' : {},
    'score_data'  : {}
}

_collecting_speech_data = False

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
    current_speech_data['single_data'][key] = data


def submit_speech_score_data(key, data):
    global current_speech_data
    current_speech_data['score_data'][key] = data

def get_speech_score_data(key):
    global current_speech_data
    return current_speech_data['score_data'][key]


def get_speech_single_data(key):
    global current_speech_data
    return current_speech_data['single_data'][key]

def get_speech_stream_data(key, index):
    global current_speech_data
    return current_speech_data['stream_data'][key]['stream'][index]


def get_speech_report():
    return current_speech_data
