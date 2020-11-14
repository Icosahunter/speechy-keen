from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from ...app import data
from ...server import server

class DisfluencyWidget(QtWidgets.QLabel):

    def __init__(self):
        super().__init__()
        self.setText('🕭0')
        server.disfluency_received_signal.connect(self.update_disfluency_count)
        data.current_speech_data.speech_started_signal.connect(self.on_speech_start)
        data.current_speech_data.speech_finished_signal.connect(self.on_speech_end)
        

    @pyqtSlot()
    def on_speech_start(self):
        colors = {
            "default" : "#000000"
        }
        data.current_speech_data.create_stream("disfluency_stream", "disfluency", colors)
        data.current_speech_data.submit_single('disfluency_count', 0)


    @pyqtSlot()
    def on_speech_end(self):
        tally = data.current_speech_data.get_single('disfluency_count')
        disf_score = 100*(1-pow(tally,2)/(pow(tally,2)+100))
        data.current_speech_data.submit_score('disfluency_score', disf_score)


    @pyqtSlot(int)
    def update_disfluency_count(self, disfluencies):
        if disfluencies > 0:
            for i in range(disfluencies):
                data.current_speech_data.submit_stream_data('disfluency_stream', {'disfluency' : disfluencies})
        elif disfluencies < 0:
            for i in range(-disfluencies):
                data.current_speech_data.undo_last_stream_data('disfluency_stream')
        
        tally = data.current_speech_data.get_single('disfluency_count') + disfluencies
    
        data.current_speech_data.submit_stream_data('disfluency_count', tally)

        self.setText('🕭' + str(tally))