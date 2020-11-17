from PyQt5 import QtWidgets, QtGui, QtCore, uic
import os
from PyQt5.QtCore import pyqtSlot, QSettings
from .alarmitem import AlarmItemWidget
from ...app import data
from ...utils import qtimeconversion as qtc

class ScoringSettings(QtWidgets.QWidget):
    """ Widget for settings some settings for scoring speeches """

    def __init__(self):
        """ The constructor """
        super().__init__()
        d = os.path.dirname(os.path.realpath(__file__))
        uic.loadUi(os.path.join(d, 'scoring_settings.ui'), self)
        self.goalTimeEdit.timeChanged.connect(self.goal_time_edit_changed)
        self.goodExpressionsLineEdit.textChanged.connect(self.good_expressions_line_edit_changed)
        self.load_settings()
    
    def load_settings(self):
        """ Loads the settings from file """

        t = data.get_data('settings/scoring/goal_speech_length')
        if t is not None:
            self.goalTimeEdit.setTime(qtc.str_to_QTime(t))
        else:
            self.goalTimeEdit.setTime(qtc.str_to_QTime('00:04:00'))

        expressions = data.get_data('settings/scoring/good_expressions')
        if expressions is not None:
            self.goodExpressionsLineEdit.setText(expressions)
        else:
            self.goodExpressionsLineEdit.setText('happy, surprise, neutral')

    @pyqtSlot()
    def goal_time_edit_changed(self):
        """ Callback that executes when the goal time edit value changes """
        t = self.goalTimeEdit.dateTime().time()
        t = qtc.QTime_to_str(t)
        data.store_data('settings/scoring/goal_speech_length', t)
    
    @pyqtSlot()
    def good_expressions_line_edit_changed(self):
        """ Callback that executes when the good expressions list changes """
        expressions = self.goodExpressionsLineEdit.text()
        data.store_data('settings/scoring/good_expressions', expressions)
