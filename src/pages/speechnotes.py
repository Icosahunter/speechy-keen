from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot
import json
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
        self.openButton.clicked.connect(self.open_button_clicked)
        self.saveButton.clicked.connect(self.save_button_clicked)
        self.authorEdit.textChanged.connect(self.update_author)
        self.speechNameEdit.textChanged.connect(self.update_speech_name)
        self.promptTextEdit.textChanged.connect(self.update_speech_prompts)
        self.speechNotesTextEdit.textChanged.connect(self.update_speech_notes)
        self.speechNameEdit.setText('MySpeech1')
        self.speechNotesTextEdit.setPlainText('1) ')
        self.update_global_notes()

    @pyqtSlot()
    def open_button_clicked(self):
        path = data.user_data_location + 'speech_notes'
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Speech Notes', path, '*.json')[0]
        filename = filename.split('/')[-1]
        filename = filename.split('.')[0]

        try:
            notes = data.get_data('documents/speech_notes/' + filename)
            data.current_speech_notes.from_dictionary(notes)

            transcript = data.current_speech_notes.transcript()
            prompts = data.current_speech_notes.prompts()

            self.speechNotesTextEdit.setPlainText(transcript)
            self.promptTextEdit.setPlainText(prompts)

        except FileNotFoundError:
            pass

    @pyqtSlot()
    def save_button_clicked(self):
        data.current_speech_notes.save_to_file()

    @pyqtSlot()
    def update_author(self):
        """ Callback for author line edit changing """
        data.current_speech_notes.set_author(self.authorEdit.text())
        #data.current_speech_data.submit_single('author', self.authorEdit.text())

    @pyqtSlot()
    def update_speech_name(self):
        """ Callback for speech name line edit changing """
        data.current_speech_notes.set_speech_name(self.speechNameEdit.text())
        #data.current_speech_data.submit_single('speech_name', self.speechNameEdit.text())

    @pyqtSlot()
    def update_speech_prompts(self):
        """ Callback for speech prompts text edit changing """
        prompts = self.promptTextEdit.toPlainText()
        if prompts.endswith('\n\n'):

            n = len(prompts.split('\n\n'))
            self.promptTextEdit.setPlainText(prompts + str(n) + ') ')

            self.update_global_notes()

    @pyqtSlot()
    def update_speech_notes(self):
        """ Callback for speech notes text edit changing """

        transcript = self.speechNotesTextEdit.toPlainText()

        if transcript.endswith('\n\n'):

            n = len(transcript.split('\n\n'))
            self.speechNotesTextEdit.setPlainText(transcript + (str(n) + ') '))
            prompts = self.promptTextEdit.toPlainText()

            new_prompt = transcript.split('\n\n')[-2]
            new_prompt = ' '.join(new_prompt.split(' ')[0:8]) + '...'
            if len(prompts) != 0:
                new_prompt = '\n\n' + new_prompt
            self.promptTextEdit.setPlainText(prompts + new_prompt)

            self.update_global_notes()
        
    def update_global_notes(self):
        transcript = self.speechNotesTextEdit.toPlainText()
        prompts = self.promptTextEdit.toPlainText()
        data.current_speech_notes.from_plain_text(prompts, transcript)
        data.current_speech_notes.set_author(self.authorEdit.text())
        data.current_speech_notes.set_speech_name(self.speechNameEdit.text())