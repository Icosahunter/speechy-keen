from PyQt5 import QtWidgets, uic

class DashboardPage(QtWidgets.QWidget):
    """
        The dashboard mode page widget
    """

    def __init__(self):
        super(DashboardPage, self).__init__()             # call the parents init
        uic.loadUi('src/pages/dashboard.ui', self)        # load the ui file