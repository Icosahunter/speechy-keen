from PyQt5 import QtWidgets, QtGui, uic
from PyQt5.QtCore import Qt, pyqtSlot
from ..app import data
from os import path
import json

class PrompterWidget(QtWidgets.QWidget):
    """ A widget that displays and allows navigating prompts """

    def __init__(self):
        """ The constructor """
        d = path.dirname(path.realpath(__file__))
        super().__init__()
        uic.loadUi(path.join(d, 'prompterwidget.ui'), self)   # load the ui file
        self.previousButton.clicked.connect(self.previous_button_clicked)
        self.forwardButton.clicked.connect(self.forward_button_clicked)
        self.refreshButton.clicked.connect(self.refresh_button_clicked)
        self.cur_index = 0

    def previous_button_clicked(self):
        if self.cur_index > 0:
            self.cur_index -= 1
            self.update_label()

    def forward_button_clicked(self):
        if self.cur_index < data.current_speech_notes.prompt_count() - 1:
            self.cur_index += 1
            self.update_label()

    def refresh_button_clicked(self):
        self.cur_index = 0
        self.update_label()

    def update_label(self):
        text = data.current_speech_notes.prompt_at(self.cur_index)
        self.speechNotesLabel.setText(text)