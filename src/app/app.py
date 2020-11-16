from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QSettings, QCoreApplication, pyqtSlot, Qt
from ..widgets.settings_widgets.alarmconfig import AlarmConfigWidget
from ..widgets.settings_widgets.scoring_settings import ScoringSettings
from ..widgets.settings_widgets.settings_info import SettingsInfo
from ..widgets.reportviewer import ReportViewer
from ..pages.loading import LoadingPage
import os
from time import sleep

class SpeechyKeenWindow(QtWidgets.QMainWindow):     # inherits from QMainWindow
    """ The main window class for the Speechy Keen application """

    def __init__(self):
        """ The constructor for SpeechyKeenWindow """

        super().__init__()                                          # call the parents init
        d = os.path.dirname(os.path.realpath(__file__))             # get the path to this file

        QCoreApplication.setOrganizationName('Nathaniel Markham')   # set organization name
        QCoreApplication.setApplicationName('Speechy Keen')         # set application name

        uic.loadUi(os.path.join(d, 'app.ui'), self)                 # load the ui file
        with open(os.path.join(d, 'app.qss'), 'r') as f:            # open the stylesheet file
            self.setStyleSheet(f.read())                            # set the main window stylesheet
        self.show()                                                 # show the ui

        # connect callbacks
        self.actionAlarm_Flags.triggered.connect(self.show_alarm_config)
        self.actionScoring_Settings.triggered.connect(self.show_scoring_settings)
        self.actionInfo.triggered.connect(self.show_info)

        # show loading screen
        self.loader_id = self.startTimer(1000)
        self.tabWidget.addTab(LoadingPage(), "Loading...")

        # initialize settings widgets
        self.alarm_config = AlarmConfigWidget()
        self.scoring_settings = ScoringSettings()
        self.settings_info = SettingsInfo()

    def timerEvent(self, event):
        """ This timer event is used to delay opening pages so that the loading screen can display """
        self.load_pages()
        self.killTimer(self.loader_id)
    
    def load_pages(self):
        """ Load the tab pages """

        from ..pages.presentation import PresentationPage
        from ..pages.dashboard import DashboardPage
        from ..pages.speechnotes import SpeechNotesPage
        self.tabWidget.addTab(DashboardPage(), "dashboard")
        self.tabWidget.addTab(SpeechNotesPage(), "speech notes")
        self.tabWidget.addTab(PresentationPage(), "presentation")
        self.tabWidget.removeTab(0)

    @pyqtSlot()
    def show_alarm_config(self):
        """ Opens alarm configuration widget """

        self.alarm_config = AlarmConfigWidget()
        self.alarm_config.setStyleSheet(self.styleSheet())
        self.alarm_config.show()

    @pyqtSlot()
    def show_scoring_settings(self):
        """ Opens speech scoring settings widget """

        self.scoring_settings = ScoringSettings()
        self.scoring_settings.setStyleSheet(self.styleSheet())
        self.scoring_settings.show()

    @pyqtSlot()
    def show_info(self):
        """ Opens application info widget """

        self.settings_info = SettingsInfo()
        self.settings_info.setStyleSheet(self.styleSheet())
        self.settings_info.show()