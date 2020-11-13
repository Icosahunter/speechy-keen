from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QSettings, QCoreApplication, pyqtSlot, Qt
from os import path
from ..widgets.settings_widgets.alarmconfig import AlarmConfigWidget
from ..widgets.settings_widgets.scoring_settings import ScoringSettings
from ..pages.loading import LoadingPage
from ..widgets.reportviewer import ReportViewer
from time import sleep

class SpeechyKeenWindow(QtWidgets.QMainWindow):     # inherits from QMainWindow
    """
        The main window class for the Speechy Keen application
    """
    def __init__(self):
        super().__init__()                                   # call the parents init
        d = path.dirname(path.realpath(__file__))
        QCoreApplication.setOrganizationName('Nathaniel Markham')
        QCoreApplication.setApplicationName('Speechy Keen')
        uic.loadUi(path.join(d, 'app.ui'), self)             # load the ui file
        with open(path.join(d, 'app.qss'), 'r') as f:        # open the stylesheet file
            self.setStyleSheet(f.read())                     # set the main window stylesheet
        self.show()                                          # show the ui
        self.actionAlarm_Flags.triggered.connect(self.show_alarm_config)
        self.actionScoring_Settings.triggered.connect(self.show_scoring_settings)
        self.loader_id = self.startTimer(1000)
        self.tabWidget.addTab(LoadingPage(), "Loading...")
        self.alarm_config = None
        self.scoring_settings = None

    def timerEvent(self, event):
        self.load_pages()
        self.killTimer(self.loader_id)
    
    def load_pages(self):
        from ..pages.presentation import PresentationPage
        from ..pages.dashboard import DashboardPage
        from ..pages.speechnotes import SpeechNotesPage
        self.tabWidget.addTab(DashboardPage(), "dashboard")
        self.tabWidget.addTab(PresentationPage(), "presentation")
        self.tabWidget.addTab(SpeechNotesPage(), "speech notes")
        self.tabWidget.removeTab(0)
        pass

    @pyqtSlot()
    def show_alarm_config(self):
        self.alarm_config = AlarmConfigWidget()
        self.alarm_config.setStyleSheet(self.styleSheet())
        self.alarm_config.show()

    @pyqtSlot()
    def show_scoring_settings(self):
        self.scoring_settings = ScoringSettings()
        self.scoring_settings.setStyleSheet(self.styleSheet())
        self.scoring_settings.show()