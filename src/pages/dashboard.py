from PyQt5 import QtWidgets, uic
from os import path

class DashboardPage(QtWidgets.QWidget):
    """
        The dashboard mode page widget
    """

    def __init__(self):
        super().__init__()                                 # call the parents init
        d = path.dirname(path.realpath(__file__))
        uic.loadUi(path.join(d, 'dashboard.ui'), self)    # load the ui file