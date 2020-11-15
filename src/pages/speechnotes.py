from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot
from ..app import data
import os

class SpeechNotesPage(QtWidgets.QWidget):
    """
        The speech notes page widget

        Contains fields for editing speech notes and prompts as well
        as adding the speech author and speech name.
    """

    def __init__(self):
        """ The constructor """
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
        """ Callback for author line edit changing """
        data.current_speech_data.submit_single('author', self.authorEdit.text())

    @pyqtSlot()
    def update_speech_name(self):
        """ Callback for speech name line edit changing """
        data.current_speech_data.submit_single('speech_name', self.speechNameEdit.text())

    @pyqtSlot()
    def update_speech_prompts(self):
        """ Callback for speech prompts text edit changing """
        pass

    @pyqtSlot()
    def update_speech_notes(self):
        """ Callback for speech notes text edit changing """
        pass

    def parse_paragraphs(self, mystring):
        """ 
            Parse a string into a list of paragraphs

            The paragraphs will be indexed by numbers present in
            the text when they are of the form 'n)'
        """
        mystring = mystring.split('\n')
        mystring = {x.strip().split(')')[0]:')'.join(x.strip().split(')')[1:]) for x in mystring}
        return mystring
        