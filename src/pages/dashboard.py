from PyQt5 import QtWidgets, uic
from ..app import data
from ..widgets.reportviewer import ReportViewer
from PyQt5.QtCore import pyqtSlot
import os

class DashboardPage(QtWidgets.QWidget):
    """
        The dashboard mode page widget
    """

    def __init__(self):
        super().__init__()                                 # call the parents init
        d = os.path.dirname(os.path.realpath(__file__))
        uic.loadUi(os.path.join(d, 'dashboard.ui'), self)    # load the ui file
        self.load_recent_speeches()
        self.recentSpeechesListWidget.itemClicked.connect(self.speech_report_clicked)
        self.report_viewer = None

    @pyqtSlot(QtWidgets.QListWidgetItem)
    def speech_report_clicked(self, item):
        self.report_viewer = ReportViewer()
        report = data.get_data('documents/speech_reports/' + item.text())
        self.report_viewer.open_dict(report)
        self.report_viewer.show_report()

    def load_recent_speeches(self):
        self.recentSpeechesListWidget.clear()
        recent_speeches = data.get_data_keys('documents/speech_reports/')[0:20]
        for k in recent_speeches:
            self.recentSpeechesListWidget.addItem(k)

