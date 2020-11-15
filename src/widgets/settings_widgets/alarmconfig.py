from PyQt5 import QtWidgets, QtGui, QtCore, uic
import os
from PyQt5.QtCore import pyqtSlot, QSettings
from .alarmitem import AlarmItemWidget
from ...app import data

class AlarmConfigWidget(QtWidgets.QWidget):
    """ A widget for configuring alarms """

    def __init__(self):
        super().__init__()
        d = os.path.dirname(os.path.realpath(__file__))
        uic.loadUi(os.path.join(d, 'alarmconfig.ui'), self)
        self.addAlarmButton.clicked.connect(self.add_alarm_button_clicked)
        self.alarms = {}
        loaded_alarms = data.get_data('settings/alarms')
        if loaded_alarms is not None:
            for alarm in data.get_data('settings/alarms'):
                self.add_alarm(alarm['id'], alarm['color'], alarm['time'])

    @pyqtSlot()
    def add_alarm_button_clicked(self):
        """ Callback that executes when the add alarm button is clicked """
        all_ids = set(range(len(self.alarms) + 1))
        used_ids = set(self.alarms.keys())
        id = min(all_ids - used_ids)
        self.add_alarm(id)

    def add_alarm(self, id, *args):
        """ 
            Adds a new alarm with the given arguments
            
            See AlarmItemWidget class to see available arguments.
        """
        alarm = AlarmItemWidget(id, *args)
        alarm.delete_clicked_signal.connect(self.remove_alarm)
        alarm.value_changed_signal.connect(self.alarm_value_changed)
        self.alarmsListLayout.addWidget(alarm)
        self.alarms[id] = alarm

    @pyqtSlot(int)
    def remove_alarm(self, alarmId):
        """ 
            Removes the alarm with the given id from the list

            Each alarm item has a delete button that this slot is
            then connected to.
        """
        print(alarmId)
        alarm = self.alarms[alarmId]
        self.alarmsListLayout.removeWidget(alarm)

        #TODO: make sure ordering of these two doesn't matter?
        alarm.deleteLater()
        del self.alarms[alarmId]
        self.update_saved_alarms()

    @pyqtSlot(int)
    def alarm_value_changed(self, alarmId):
        """ 
            Callback that executes when the value of an alarm item changes

            Each alarm item in the list connects to this.
        """
        self.update_saved_alarms()

    def update_saved_alarms(self):
        """ Saves alarm configuration to file """
        a = []
        for id in self.alarms:
            a.append(self.alarms[id].alarm_data)
        data.store_data('settings/alarms', a)

        