from PyQt5 import QtWidgets, uic
from os import path

class SpeechNotesPage(QtWidgets.QWidget):
    """
        The speech notes mode page widget
    """

    def __init__(self):
        super().__init__()                                   # call the parents init
        d = path.dirname(path.realpath(__file__))
        uic.loadUi(path.join(d, 'speechnotes.ui'), self)     # load the ui file