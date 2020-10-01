from PyQt5 import QtWidgets, uic

class SpeechNotesPage(QtWidgets.QWidget):
    """
        The speech notes mode page widget
    """

    def __init__(self):
        super(SpeechNotesPage, self).__init__()   # call the parents init
        uic.loadUi('speechnotes.ui', self)        # load the ui file