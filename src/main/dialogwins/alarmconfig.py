from PyQt5 import QtWidgets, QtGui, QtCore, uic
from os import path
from PyQt5.QtCore import pyqtSlot
from .alarmitem import AlarmItemWidget

class AlarmConfigWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        d = path.dirname(path.realpath(__file__))
        uic.loadUi(path.join(d, 'alarmconfig.ui'), self)
        with open(path.join(d, '../app/app.qss'), 'r') as f:        # open the stylesheet file
            self.setStyleSheet(f.read())                     # set the main window stylesheet
        self.addAlarmButton.clicked.connect(self.add_alarm_button_clicked)
        self.alarms = {}

    @pyqtSlot()
    def add_alarm_button_clicked(self):
        alarm = AlarmItemWidget()
        alarm.delete_clicked_signal.connect(self.remove_alarm)
        self.alarmsListLayout.addWidget(alarm)
        all_ids = set(range(len(self.alarms) + 1))
        used_ids = set(self.alarms.keys())
        alarm.id = min(all_ids - used_ids)
        self.alarms[alarm.id] = alarm

    @pyqtSlot(int)
    def remove_alarm(self, alarmId):
        print(alarmId)
        alarm = self.alarms[alarmId]
        self.alarmsListLayout.removeWidget(alarm)

        #TODO: make sure ordering of these two doesn't matter?
        alarm.deleteLater()
        del self.alarms[alarmId]

        