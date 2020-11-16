from PyQt5.QtCore import pyqtSignal, QObject
from enum import Enum
from os import path, makedirs, listdir
import json
from datetime import datetime

class SpeechData(QObject):
    """ 
        A class for handling real time metrics coming from other widgets.
    
        This class provides interfaces for storing speech data metrics. 
        An instance of this class exists in the 'data' object so that all existing 
        metric widgets can contribute speech data in a decentralized way.
        This class also will emit signals when the speech is started, paused,
        resumed, or ended that way metric widgets can respond appropriately.
    """

    speech_finished_signal = pyqtSignal()
    speech_started_signal = pyqtSignal()
    speech_paused_signal = pyqtSignal()
    speech_resumed_signal = pyqtSignal()

    def __init__(self):
        """ The constructor """

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
        """
            Update SpeechData's internal representation of the current speech length.

            To prevent this function from needing to be called every second, the
            time representation is given as time until the pause, and the time of the
            last resume, which is the same way TimerWidget stores current time. This
            means it only needs to be called whenever the speech is started, paused,
            resumed, or ended.
        """

        self._cumul_time = cumul_time
        self._lap_time = lap_time

    def get_timestamp(self):
        """ Returns a timestamp in the form of seconds since the speech started. """

        return int((self._cumul_time + (datetime.now() - self._lap_time)).total_seconds())



    def start_speech(self):
        """ Sets state variables, emits speech started signal """
        self._paused = False
        self._finished = False
        self.speech_started_signal.emit()

    def end_speech(self):
        """ Sets state variables and emits speech finished signal. """
        self._finished = True
        self._paused = True
        self.speech_finished_signal.emit()

    def resume_speech(self):
        """ Sets state variables and emits speech resumed signal. """
        self._paused = False
        self.speech_resumed_signal.emit()

    def pause_speech(self):
        """ Sets state variables and emits speech paused signal. """
        self._paused = True
        self.speech_paused_signal.emit()

    def clear(self):
        """ Clears all speech data. """
        self._speech_data = {
            'stream_data' : {},
            'single_data' : {},
            'score_data'  : {}
        }

    def is_paused(self):
        """ Returns true if the speech is currently paused. """
        return self._paused

    def is_finished(self):
        """ Returns true if the speech has ended or has not yet started. """
        return self._finished
    
    def create_stream(self, stream_name, main_data_key, colors_dict):
        """ 
            Initialize a data stream. 
            
            Stream name is the name of the data stream and should end
            with '_stream'.
            Main data key is the name of the data that should be displayed
            in the stream plot.
            Colors dictionary is a dictionary associating data values for
            the main data to hexadecimal color values. This is used when
            plotting the stream data.
        """
        stream = {'main_data' : main_data_key, 'colors' : colors_dict, 'stream' : []}
        self._speech_data['stream_data'][stream_name] = stream

    def submit_stream_data(self, key, data_dict):
        """ 
            Submit data entry to a stream.

            Key is the stream name. Data dictionary is a dictionary with
            data names and data values.
        """
        data = {'time_stamp' : self.get_timestamp()}
        for d in data_dict:
            data[d] = data_dict[d]
        self._speech_data['stream_data'][key]['stream'].append(data)

    def undo_last_stream_data(self, key):
        """
            Removes the last submitted data entry from the given stream.

            Key is the stream name. 
        """
        self._speech_data['stream_data'][key]['stream'].pop()

    def get_stream(self, key):
        """ 
            Get's the entire stream.

            Key is the stream name.
        """
        return self._speech_data['stream_data'][key]['stream']

    def get_stream_data(self, key, index):
        """ 
            Returns a single data point from a data stream.

            Key is the stream name. Index is the index of the
            desired data point.
        """
        return self._speech_data['stream_data'][key]['stream'][index]



    def submit_single(self, key, data):
        """ 
            Submit data that is a single value.

            Key is the data name. Data is the value.
        """
        self._speech_data['single_data'][key] = data

    def get_single(self, key):
        """ 
            Get the value of a piece of single data.

            Key is the name of the data.
        """
        return self._speech_data['single_data'][key]



    def submit_score(self, key, data):
        """
            Submit a piece of data that is a percentage score for a metric.

            Key is the name of the score and should end with '_score'.
            Data is the value of the score as an integer from 1 to 100.
        """
        self._speech_data['score_data'][key] = data

    def get_score(self, key):
        """
            Get the value of a piece of score data.

            Key is the name of the score data.
        """
        return self._speech_data['score_data'][key]

    def get_all_scores(self):
        """
            Get a list of all score data values.

            Returns a list of just values for use in calculating a total score.
        """
        return self._speech_data['score_data'].values()


    def get_speech_report(self):
        """ Returns the entire speech report object. """
        return self._speech_data