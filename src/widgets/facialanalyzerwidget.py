from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QThread
from ..app.data import submit_speech_stream_data, create_speech_data_stream
from fer import FER
import numpy

class FacialAnalyzerWidget(QtWidgets.QLabel):

    def __init__(self):
        super().__init__()
        self.facial_analyzer = FER()
        colors = {
            "happy"     : "#f5f242",
            "sad"       : "#4260f5",
            "surprised" : "#42f54e",
            "angry"     : "#f54542",
            "neutral"   : "#ffffff",
            "default"   : "#000000"
        }
        create_speech_data_stream("expression_stream", "expression", colors)


    @pyqtSlot(numpy.ndarray)
    def update_facial_analysis(self, frame):

        try:
            emotion, confidence = self.facial_analyzer.top_emotion(frame)
            self.setText('{:.0%} : {}'.format(confidence, emotion))
            submit_speech_stream_data('expression_stream', {'confidence': str(confidence), 'expression': emotion})
        except:
            pass

