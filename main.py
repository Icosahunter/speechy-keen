import sys
from PyQt5 import QtWidgets, uic

main_stylesheet = 'main.qss'        # a global stylesheet for the whole application

App = QtWidgets.QApplication([])    # create the application

with open('main.qss', 'r') as f:    # open the stylesheet file
    App.setStyleSheet(f.read())     # set the application stylesheet

UI = uic.loadUi('main.ui')          # open the ui file
UI.show()                           # display the ui
sys.exit(App.exec_())               # run the application