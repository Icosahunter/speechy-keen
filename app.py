from PyQt5 import QtWidgets, uic

class SpeechyKeenWindow(QtWidgets.QMainWindow):     # inherits from QMainWindow
    """
        The main window class for the Speechy Keen application
    """
    def __init__(self):
        super(SpeechyKeenWindow, self).__init__()   # call the parents init
        uic.loadUi('app.ui', self)                  # load the ui file
        with open('app.qss', 'r') as f:             # open the stylesheet file
            self.setStyleSheet(f.read())            # set the main window stylesheet
        self.show()                                 # show the ui
