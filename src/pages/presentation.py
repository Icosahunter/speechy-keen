from PyQt5 import QtWidgets, uic
from ..widgets.timerwidget import TimerWidget
from ..widgets.videowidget import VideoWidget

class PresentationPage(QtWidgets.QWidget):
    """
        The presentation mode page widget
    """

    def __init__(self):
        super(PresentationPage, self).__init__()             # call the parents init
        uic.loadUi('src/pages/presentation.ui', self)        # load the ui file
        
        # remove mockup widgets
        self.timeMockup.deleteLater()
        self.videoMockup.deleteLater()

        # add custom widgets
        self.timerWidget = TimerWidget()
        self.sideBarContainer.insertWidget(0, self.timerWidget)
        font = self.timerWidget.font()
        font.setPointSize(45)
        self.timerWidget.setFont(font)

        self.videoWidget = VideoWidget(width=650, height=400)
        self.layout().addWidget(self.videoWidget, 0, 1)
        self.videoWidget.mirrored = True

        # connect callbacks
        self.startButton.clicked.connect(\
            lambda : self.start_button_clicked())
        self.stopButton.clicked.connect(\
            lambda : self.stop_button_clicked())

    def start_button_clicked(self):
        if not self.timerWidget.timer_running:
            self.timerWidget.start_timer()
            self.startButton.setText("pause")
        else:
            self.timerWidget.pause_timer()
            self.startButton.setText("resume")

    def stop_button_clicked(self):
        self.timerWidget.clear_timer()
        self.startButton.setText("start")