from PyQt5 import QtWidgets, QtGui, QtCore, uic
import os
from PyQt5.QtCore import pyqtSlot, QSettings
from .alarmitem import AlarmItemWidget
from ...app import data
from ...utils import qtimeconversion as qtc

class ScoringSettings(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        d = os.path.dirname(os.path.realpath(__file__))
        uic.loadUi(os.path.join(d, 'scoring_settings.ui'), self)
        self.goalTimeEdit.timeChanged.connect(self.goal_time_edit_changed)
        self.goodExpressionsLineEdit.textChanged.connect(self.good_expressions_line_edit_changed)
        self.load_settings()
    
    def load_settings(self):

        try:
            t = data.get_data('settings/scoring/goal_speech_length')
            self.goalTimeEdit.setTime(qtc.str_to_QTime(t))
        except:
            self.goalTimeEdit.setTime(qtc.str_to_QTime('00:04:00'))

        try:
            expressions = data.get_data('settings/scoring/good_expressions')
            self.goodExpressionsLineEdit.setText(expressions)
        except:
            self.goodExpressionsLineEdit.setText('happy, surprise, neutral')

    @pyqtSlot()
    def goal_time_edit_changed(self):
        t = self.goalTimeEdit.dateTime().time()
        t = qtc.QTime_to_str(t)
        data.store_data('settings/scoring/goal_speech_length', t)
    
    @pyqtSlot()
    def good_expressions_line_edit_changed(self):
        expressions = self.goodExpressionsLineEdit.text()
        data.store_data('settings/scoring/good_expressions', expressions)
