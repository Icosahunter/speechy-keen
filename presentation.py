from PyQt5 import QtWidgets, uic

class PresentationPage(QtWidgets.QWidget):
    """
        The presentation mode page widget
    """

    def __init__(self):
        super(PresentationPage, self).__init__()   # call the parents init
        uic.loadUi('presentation.ui', self)         # load the ui file