from PyQt5 import QtWidgets, QtGui, QtCore, uic
import os
from PyQt5.QtCore import pyqtSlot, QSettings
from .alarmitem import AlarmItemWidget
from ...app import data

class SettingsInfo(QtWidgets.QWidget):
    """ Widget that displays some info about the application """

    def __init__(self):
        """ The constructor """
        super().__init__()
        d = os.path.dirname(os.path.realpath(__file__))
        uic.loadUi(os.path.join(d, 'settings_info.ui'), self)
        self.appLocLabel.setText(os.getcwd())
        self.settingsLocLabel.setText(data.settings_location)
        self.docLocLabel.setText(data.user_data_location)
        self.appDataLocLabel.setText(data.app_data_location)
