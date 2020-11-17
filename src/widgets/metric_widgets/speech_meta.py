from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot
import os
from datetime import datetime
from ...app import data

class SpeechMeta(QtWidgets.QWidget):
    """ A metric widget that submits some meta data at speech start """
    
    def __init__(self):
        """ The constructor """

        super().__init__()
        d = os.path.dirname(os.path.realpath(__file__))
        uic.loadUi(os.path.join(d, 'speech_meta.ui'), self)
        
        self.presenterNameEdit.textChanged.connect(self.update_presenter_name)
        data.current_speech_data.speech_started_signal.connect(self.on_speech_start)

        data.current_speech_data.submit_single('presenter_name', self.presenterNameEdit.text())
    
    @pyqtSlot()
    def on_speech_start(self):
        """ Callback that executes when the speech starts """
        
        data.current_speech_data.submit_single('date', datetime.now().strftime('%m-%d-%YT%H%M%S'))
        data.current_speech_data.submit_single('author', data.current_speech_notes.author())
        data.current_speech_data.submit_single('speech_name', data.current_speech_notes.speech_name())
    
    def update_presenter_name(self):
        """ Callback that executes when the presenter name is changed """
        data.current_speech_data.submit_single('presenter_name', self.presenterNameEdit.text())