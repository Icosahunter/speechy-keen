from PyQt5 import QtWidgets, uic
from ..app import data
from ..widgets.reportviewer import ReportViewer
from PyQt5.QtCore import pyqtSlot
import os

class DashboardPage(QtWidgets.QWidget):
    """
        The dashboard page widget.

        This page contains speech stats and a way to browse speech
        reports.
    """

    def __init__(self):
        """ The constructor """
        super().__init__()                                 # call the parents init
        d = os.path.dirname(os.path.realpath(__file__))    # get the path to this file
        uic.loadUi(os.path.join(d, 'dashboard.ui'), self)  # load the ui file
        self.load_recent_speeches()
        self.recentSpeechesListWidget.itemClicked.connect(self.speech_report_clicked)
        self.report_viewer = None

    @pyqtSlot(QtWidgets.QListWidgetItem)
    def speech_report_clicked(self, item):
        """ Callback for when a speech report in the list box is clicked. """
        self.report_viewer = ReportViewer()
        report = data.get_data('documents/speech_reports/' + item.text())
        self.report_viewer.open_dict(report)
        self.report_viewer.show_report()

    def load_recent_speeches(self):
        """ Loads the list of recent speech reports. """
        self.recentSpeechesListWidget.clear()
        recent_speeches = data.get_data_keys('documents/speech_reports/')[0:20]
        for k in recent_speeches:
            self.recentSpeechesListWidget.addItem(k)

