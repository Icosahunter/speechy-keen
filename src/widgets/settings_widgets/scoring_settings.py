from PyQt5 import QtWidgets, QtGui, QtCore, uic
from os import path
from PyQt5.QtCore import pyqtSlot, QSettings
from .alarmitem import AlarmItemWidget
from ...app.data import store_data, get_data, SettingType
from ...utils.qtimeconversion import QTime_to_seconds, seconds_to_QTime

class ScoringSettings(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        d = path.dirname(path.realpath(__file__))
        uic.loadUi(path.join(d, 'scoring_settings.ui'), self)
        self.goalTimeEdit.timeChanged.connect(self.goal_time_edit_changed)
        self.goodExpressionsLineEdit.textChanged.connect(self.good_expressions_line_edit_changed)
        self.load_settings()
    
    def load_settings(self):

        try:
            t = get_data('scoring_settings/goal_speech_length')
            self.goalTimeEdit.setTime(seconds_to_QTime(t))
        except:
            self.goalTimeEdit.setTime(seconds_to_QTime(240))

        try:
            expressions = get_data('scoring_settings/good_expressions')
            self.goodExpressionsLineEdit.setText(expressions)
        except:
            self.goodExpressionsLineEdit.setText('happy, surprise, neutral')

    @pyqtSlot()
    def goal_time_edit_changed(self):
        t = QTime_to_seconds(self.goalTimeEdit.dateTime().time())
        store_data('scoring_settings/goal_speech_length', t, SettingType.config)
    
    @pyqtSlot()
    def good_expressions_line_edit_changed(self):
        expressions = self.goodExpressionsLineEdit.text()
        store_data('scoring_settings/good_expressions', expressions, SettingType.config)
