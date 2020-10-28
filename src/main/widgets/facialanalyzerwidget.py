from fer import FER
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from ..app.data import SubmitSpeechStreamData
import numpy

class FacialAnalyzerWidget(QtWidgets.QLabel):

    def __init__(self):
        super().__init__()
        self.facial_analyzer = FER()

    @pyqtSlot(numpy.ndarray)
    def update_facial_analysis(self, frame):

        try:
            emotion, confidence = self.facial_analyzer.top_emotion(frame)
            self.setText('{:.0%} : {}'.format(confidence, emotion))
            SubmitSpeechStreamData('expression', {'confidence': confidence, 'emotion': emotion})
        except:
            pass

