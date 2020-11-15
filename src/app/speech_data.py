from PyQt5.QtCore import pyqtSignal, QObject
from enum import Enum
from os import path, makedirs, listdir
import json
from datetime import datetime

class SpeechData(QObject):

    speech_finished_signal = pyqtSignal()
    speech_started_signal = pyqtSignal()
    speech_paused_signal = pyqtSignal()
    speech_resumed_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self._speech_data = {
            'stream_data' : {},
            'single_data' : {},
            'score_data'  : {}
        }

        self._paused = True
        self._finished = True
        self._cumul_time = 0
        self._lap_time = 0

    def set_time_keeping(self, cumul_time, lap_time):
        self._cumul_time = cumul_time
        self._lap_time = lap_time

    def get_timestamp(self):
        return int((self._cumul_time + (datetime.now() - self._lap_time)).total_seconds())



    def start_speech(self):
        self._paused = False
        self._finished = False
        self.speech_started_signal.emit()
        self.submit_single('date', datetime.now().strftime('%m-%d-%YT%H%M%S'))

    def end_speech(self):
        self._finished = True
        self._paused = True
        self.speech_finished_signal.emit()

    def resume_speech(self):
        self._paused = False
        self.speech_resumed_signal.emit()

    def pause_speech(self):
        self._paused = True
        self.speech_paused_signal.emit()

    def clear(self):
        self._speech_data = {
            'stream_data' : {},
            'single_data' : {},
            'score_data'  : {}
        }

    def is_paused(self):
        return self._paused

    def is_finished(self):
        return self._finished
    
    def create_stream(self, stream_name, main_data_key, colors_dict):
        stream = {'main_data' : main_data_key, 'colors' : colors_dict, 'stream' : []}
        self._speech_data['stream_data'][stream_name] = stream

    def submit_stream_data(self, key, data_dict):
        data = {'time_stamp' : self.get_timestamp()}
        for d in data_dict:
            data[d] = data_dict[d]
        self._speech_data['stream_data'][key]['stream'].append(data)

    def undo_last_stream_data(self, key):
        self._speech_data['stream_data'][key]['stream'].pop()

    def get_stream(self, key):
        return self._speech_data['stream_data'][key]['stream']

    def get_stream_data(self, key, index):
        return self._speech_data['stream_data'][key]['stream'][index]



    def submit_single(self, key, data):
        self._speech_data['single_data'][key] = data

    def get_single(self, key):
        return self._speech_data['single_data'][key]



    def submit_score(self, key, data):
        self._speech_data['score_data'][key] = data

    def get_score(self, key):
        return self._speech_data['score_data'][key]

    def get_all_scores(self):
        return self._speech_data['score_data'].values()


    def get_speech_report(self):
        return self._speech_data