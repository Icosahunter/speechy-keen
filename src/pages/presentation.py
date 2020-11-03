from PyQt5 import QtWidgets, uic
from os import path
from ..widgets.timerwidget import TimerWidget
from ..widgets.videowidget import VideoWidget
from ..widgets.facialanalyzerwidget import FacialAnalyzerWidget
from ..widgets.disfluencywidget import DisfluencyWidget
from ..app.data import begin_speech_data_collection, stop_speech_data_collection
from PyQt5.QtCore import pyqtSlot

class PresentationPage(QtWidgets.QWidget):
    """
        The presentation mode page widget
    """

    def __init__(self):
        super().__init__()                                    # call the parents init
        d = path.dirname(path.realpath(__file__))
        uic.loadUi(path.join(d, 'presentation.ui'), self)    # load the ui file
        
        # remove mockup widgets
        self.timeMockup.deleteLater()
        self.videoMockup.deleteLater()
        self.moodLabelMockup.deleteLater()
        self.wordSpeedLabelMockup.deleteLater()

        # add custom widgets
        self.timerWidget = TimerWidget()
        self.sideBarContainer.insertWidget(0, self.timerWidget)
        font = self.timerWidget.font()
        font.setPointSize(45)
        self.timerWidget.setFont(font)

        self.facialAnalyzerWidget = FacialAnalyzerWidget()
        self.statsContainer.insertWidget(0, self.facialAnalyzerWidget)

        self.disfluencyWidget = DisfluencyWidget()
        self.statsContainer.insertWidget(0, self.facialAnalyzerWidget)

        self.videoWidget = VideoWidget(width=650, height=400)
        self.layout().addWidget(self.videoWidget, 0, 1)
        self.videoWidget.mirrored = True

        # connect callbacks
        self.videoWidget.frame_signal.connect(self.facialAnalyzerWidget.update_facial_analysis)
        self.startButton.clicked.connect(self.start_button_clicked)
        self.stopButton.clicked.connect(self.stop_button_clicked)

    @pyqtSlot()
    def start_button_clicked(self):
        if not self.timerWidget.timer_running:
            self.timerWidget.start_timer()
            self.startButton.setText("pause")
            stop_speech_data_collection()
        else:
            self.timerWidget.pause_timer()
            self.startButton.setText("resume")
            begin_speech_data_collection()

    @pyqtSlot()
    def stop_button_clicked(self):
        self.timerWidget.clear_timer()
        self.startButton.setText("start")
        stop_speech_data_collection()