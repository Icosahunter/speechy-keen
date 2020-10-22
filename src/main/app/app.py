from PyQt5 import QtWidgets, uic
from os import path
from ..pages.presentation import PresentationPage
from ..pages.dashboard import DashboardPage
from ..pages.speechnotes import SpeechNotesPage
from ..dialogwins.alarmconfig import AlarmConfigWidget

class SpeechyKeenWindow(QtWidgets.QMainWindow):     # inherits from QMainWindow
    """
        The main window class for the Speechy Keen application
    """
    def __init__(self):
        super().__init__()                                   # call the parents init
        d = path.dirname(path.realpath(__file__))
        uic.loadUi(path.join(d, 'app.ui'), self)             # load the ui file
        with open(path.join(d, 'app.qss'), 'r') as f:        # open the stylesheet file
            self.setStyleSheet(f.read())                     # set the main window stylesheet
        self.show()                                          # show the ui
        self.load_pages()
        self.actionAlarm_Flags.triggered.connect(\
            lambda: self.show_alarm_config())
        self.alarm_config = AlarmConfigWidget()

    def load_pages(self):
        self.tabWidget.addTab(DashboardPage(), "dashboard")
        self.tabWidget.addTab(PresentationPage(), "presentation")
        self.tabWidget.addTab(SpeechNotesPage(), "speech notes")

    def show_alarm_config(self):
        self.alarm_config.show()