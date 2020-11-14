from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot
from ..app import data
import os

class SpeechNotesPage(QtWidgets.QWidget):
    """
        The speech notes mode page widget
    """

    def __init__(self):
        super().__init__()                                   # call the parents init
        d = os.path.dirname(os.path.realpath(__file__))
        uic.loadUi(os.path.join(d, 'speechnotes.ui'), self)     # load the ui file
        self.authorEdit.textChanged.connect(self.update_author)
        self.speechNameEdit.textChanged.connect(self.update_speech_name)
        self.promptTextEdit.textChanged.connect(self.update_speech_prompts)
        self.speechNotesTextEdit.textChanged.connect(self.update_speech_notes)
        self.speechNameEdit.setText('MySpeech1')

    @pyqtSlot()
    def update_author(self):
        data.current_speech_data.submit_single('author', self.authorEdit.text())

    @pyqtSlot()
    def update_speech_name(self):
        data.current_speech_data.submit_single('speech_name', self.speechNameEdit.text())

    @pyqtSlot()
    def update_speech_prompts(self):
        pass

    @pyqtSlot()
    def update_speech_notes(self):
        pass

    def parse_paragraphs(self, mystring):
        mystring = mystring.split('\n')
        mystring = {x.strip().split(')')[0]:')'.join(x.strip().split(')')[1:]) for x in mystring}
        return mystring
        