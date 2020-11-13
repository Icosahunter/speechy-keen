from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from ...app.speech_data import create_speech_data_stream, submit_speech_stream_data, undo_last_speech_stream_data, submit_speech_single_data, get_speech_single_data
from ...server.server import disfluency_received_signal

class DisfluencyWidget(QtWidgets.QLabel):

    def __init__(self):
        super().__init__()
        self.setText('🕭0')
        disfluency_received_signal.connect(self.update_disfluency_count)
        colors = {
            "default" : "#000000"
        }
        create_speech_data_stream("disfluency_stream", "disfluency", colors)
        submit_speech_single_data('disfluency_count', 0)


    @pyqtSlot(int)
    def update_disfluency_count(self, disfluencies):
        if disfluencies > 0:
            for i in range(disfluencies):
                submit_speech_stream_data('disfluency_stream', {'disfluency' : disfluencies})
        elif disfluencies < 0:
            for i in range(-disfluencies):
                undo_last_speech_stream_data('disfluency_stream')
        
        submit_speech_single_data('disfluency_count', get_speech_single_data('disfluency_count') + disfluencies)

        self.setText('🕭' + str(get_speech_single_data('disfluency_count')))