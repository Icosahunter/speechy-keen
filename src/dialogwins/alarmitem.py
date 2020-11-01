from PyQt5 import QtWidgets, QtGui, QtCore, uic
from os import path
from PyQt5.QtCore import pyqtSignal, pyqtSlot

class AlarmItemWidget(QtWidgets.QWidget):

    delete_clicked_signal = pyqtSignal(int)
    value_changed_signal = pyqtSignal(int)

    def __init__(self, id=0, color = 'red', time = 0):

        super().__init__()
        d = path.dirname(path.realpath(__file__))
        uic.loadUi(path.join(d, 'alarmitem.ui'), self)
        
        self.colorComboBox.setCurrentText(color)
        self.set_time(time)

        self.deleteButton.clicked.connect(self.delete_button_clicked)
        self.timeEdit.timeChanged.connect(self.time_changed)
        self.colorComboBox.currentIndexChanged.connect(self.color_changed)

        self.alarm_data = { 'id' : id, 'color' : color, 'time' : time }
    
    @pyqtSlot()
    def delete_button_clicked(self):
        self.delete_clicked_signal.emit(self.alarm_data['id'])

    @pyqtSlot()
    def time_changed(self):
        self.alarm_data['time'] = self.get_time()
        self.value_changed_signal.emit(self.alarm_data['id'])

    @pyqtSlot()
    def color_changed(self):
        self.alarm_data['color'] = self.get_color()
        self.value_changed_signal.emit(self.alarm_data['id'])

    def get_color(self):
        c = self.colorComboBox.currentText()
        if c == 'red':
            return '#c20000'
        elif c == 'orange':
            return '#d95e00'
        elif c == 'yellow':
            return '#f2d116'
        elif c == 'green':
            return '#3abd1c'
        elif c == 'teal':
            return '#109e73'
        elif c == 'blue':
            return '#1065b5'
        elif c == 'purple':
            return '#8e42bd'
        else:
            return '#000000'

    def get_time(self):
        t = self.timeEdit.dateTime().time()
        h = t.hour()
        m = t.minute()
        s = t.second()
        return 3600*h + 60*m + s

    def set_time(self, sec):
        h = sec//3600
        m = (sec - h*3600)//60
        s = (sec - h*3600 - m*60)
        self.timeEdit.setTime(QtCore.QTime(h, m, s))