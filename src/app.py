from PyQt5 import QtWidgets, uic
from .pages.presentation import PresentationPage
from .pages.dashboard import DashboardPage
from .pages.speechnotes import SpeechNotesPage

class SpeechyKeenWindow(QtWidgets.QMainWindow):     # inherits from QMainWindow
    """
        The main window class for the Speechy Keen application
    """
    def __init__(self):
        super(SpeechyKeenWindow, self).__init__()   # call the parents init
        uic.loadUi('src/app.ui', self)                  # load the ui file
        with open('src/app.qss', 'r') as f:             # open the stylesheet file
            self.setStyleSheet(f.read())            # set the main window stylesheet
        self.show()                                 # show the ui
        self.load_pages()

    def load_pages(self):
        self.tabWidget.addTab(DashboardPage(), "dashboard")
        self.tabWidget.addTab(PresentationPage(), "presentation")
        self.tabWidget.addTab(SpeechNotesPage(), "speech notes")