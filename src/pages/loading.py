from PyQt5 import QtWidgets, uic
import os

class LoadingPage(QtWidgets.QWidget):
    """
        The dashboard mode page widget
    """
    def __init__(self):
        super().__init__()                              # call the parents init
        d = os.path.dirname(os.path.realpath(__file__))
        uic.loadUi(os.path.join(d, 'loading.ui'), self)    # load the ui file