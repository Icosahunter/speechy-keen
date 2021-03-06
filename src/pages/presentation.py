from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot
import os
import math
from ..widgets.videowidget import VideoWidget
from ..widgets.metric_widgets.timerwidget import TimerWidget
from ..widgets.prompterwidget import PrompterWidget
#from ..widgets.metric_widgets.facialanalyzerwidget import FacialAnalyzerWidget
from ..widgets.metric_widgets.disfluencywidget import DisfluencyWidget
from ..widgets.reportviewer import ReportViewer
from ..widgets.metric_widgets.total_score import TotalScore
from ..app import data
from ..server.server import full_address

class PresentationPage(QtWidgets.QWidget):
    """
        The presentation page widget

        This is the primary page for the application. It has 
        the video feed, allows starting and ending the speech,
        and shows feedback for the speech.
    """

    def __init__(self):
        """ The constructor """
        super().__init__()                                    # call the parents init
        d = os.path.dirname(os.path.realpath(__file__))
        uic.loadUi(os.path.join(d, 'presentation.ui'), self)    # load the ui file
        
        # remove mockup widgets
        self.timeMockup.deleteLater()
        self.videoMockup.deleteLater()
        self.moodLabelMockup.deleteLater()
        self.wordSpeedLabelMockup.deleteLater()
        self.speechNotesMockup.deleteLater()

        # add custom widgets
        self.timerWidget = TimerWidget()
        self.sideBarContainer.insertWidget(0, self.timerWidget)

        self.prompterWidget = PrompterWidget()
        self.sideBarContainer.insertWidget(5, self.prompterWidget)

        #self.facialAnalyzerWidget = FacialAnalyzerWidget()
        #self.statsContainer.insertWidget(0, self.facialAnalyzerWidget)

        self.disfluencyWidget = DisfluencyWidget()
        self.statsContainer.insertWidget(0, self.disfluencyWidget)

        self.videoWidget = VideoWidget(width=650, height=400)
        self.layout().addWidget(self.videoWidget, 1)
        self.videoWidget.mirrored = True

        self.totalScore = TotalScore()

        self.urlLabel.setText('url:  ' + full_address)

        # connect callbacks
        #self.videoWidget.frame_signal.connect(self.facialAnalyzerWidget.update_facial_analysis)
        self.startButton.clicked.connect(self.start_button_clicked)
        self.stopButton.clicked.connect(self.stop_button_clicked)
        self.report_viewer = None

    @pyqtSlot()
    def start_button_clicked(self):
        """ Callback for the start/pause/resume speech button. """
        if data.current_speech_data.is_finished():
            self.startButton.setText('pause')
            data.current_speech_data.start_speech()
        elif data.current_speech_data.is_paused():
            self.startButton.setText('pause')
            data.current_speech_data.resume_speech()
        else:
            self.startButton.setText('resume')
            data.current_speech_data.pause_speech()

    @pyqtSlot()
    def stop_button_clicked(self):
        """ Callback for the stop speech button. """
        self.startButton.setText('start')
        data.current_speech_data.end_speech()

        self.report_viewer = ReportViewer()
        report = data.current_speech_data.get_speech_report()
        self.report_viewer.open_dict(report)
        self.report_viewer.show_report()

        data.current_speech_data.clear()
        