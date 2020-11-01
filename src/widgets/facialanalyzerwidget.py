from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QThread
from ..app.data import SubmitSpeechStreamData
from fer import FER
import importlib
import numpy
import asyncio

class FacialAnalyzerWidget(QtWidgets.QLabel):

    def __init__(self):
        super().__init__()
        self.facial_analyzer = FER()

    @pyqtSlot(numpy.ndarray)
    def update_facial_analysis(self, frame):

        try:
            emotion, confidence = self.facial_analyzer.top_emotion(frame)
            self.setText('{:.0%} : {}'.format(confidence, emotion))
            #SubmitSpeechStreamData('expression', {'confidence': confidence, 'emotion': emotion})
        except:
            pass

