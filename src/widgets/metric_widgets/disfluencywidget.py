from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QUrl
from pygame import mixer
import os
import json
from ...app import data
from ...server import server

class DisfluencyWidget(QtWidgets.QLabel):
    """ A metric widget for tracking disfluencies received by the server. """

    def __init__(self):
        """ The constructor """

        super().__init__()

        self.setText('🕭0')

        server.disfluency_received_signal.connect(self.update_disfluency_count)
        data.current_speech_data.speech_started_signal.connect(self.on_speech_start)
        data.current_speech_data.speech_finished_signal.connect(self.on_speech_end)

        d = os.getcwd()
        mixer.init()
        self.ding_effect = mixer.Sound(d + '/src/resources/sounds/196106__aiwha__ding.wav')

    @pyqtSlot()
    def on_speech_start(self):
        """ Callback that executes when the speech starts """
        colors = {
            "default" : "#000000"
        }
        data.current_speech_data.create_stream("disfluency_stream", "disfluency", colors)
        data.current_speech_data.submit_single('disfluency_count', 0)


    @pyqtSlot()
    def on_speech_end(self):
        """ Callback that executres when the speech ends """
        tally = data.current_speech_data.get_single('disfluency_count')
        disf_score = 100*(1-pow(tally,2)/(pow(tally,2)+100))
        data.current_speech_data.submit_score('disfluency_score', disf_score)


    @pyqtSlot(str)
    def update_disfluency_count(self, disfluency_str):
        """ Callback that executes when the server receives a disfluency """

        disfluency_dict = json.loads(disfluency_str)
        disfluencies = disfluency_dict['disfluencies']
        mute_ding = disfluency_dict['mute_ding']

        if not mute_ding:
            self.play_ding()

        if not data.current_speech_data.is_paused():
            if disfluencies > 0:
                for i in range(disfluencies):
                    data.current_speech_data.submit_stream_data('disfluency_stream', {'disfluency' : disfluencies})
            elif disfluencies < 0:
                for i in range(-disfluencies):
                    data.current_speech_data.undo_last_stream_data('disfluency_stream')
            
            tally = data.current_speech_data.get_single('disfluency_count') + disfluencies

            data.current_speech_data.submit_single('disfluency_count', tally)

            self.setText('🕭' + str(tally))

    def play_ding(self):
        self.ding_effect.play()