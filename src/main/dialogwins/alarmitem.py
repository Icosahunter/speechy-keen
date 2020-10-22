from PyQt5 import QtWidgets, QtGui, QtCore, uic
from os import path
from PyQt5.QtCore import pyqtSignal, pyqtSlot

class AlarmItemWidget(QtWidgets.QWidget):

    delete_clicked_signal = pyqtSignal(int)

    def __init__(self, id=0):
        super().__init__()
        d = path.dirname(path.realpath(__file__))
        uic.loadUi(path.join(d, 'alarmitem.ui'), self)
        self.deleteButton.clicked.connect(self.delete_button_clicked)
        self.id = id
    
    @pyqtSlot()
    def delete_button_clicked(self):
        self.delete_clicked_signal.emit(self.id)