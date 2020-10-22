import sys
from PyQt5 import QtWidgets, uic
from main.app.app import SpeechyKeenWindow

App = QtWidgets.QApplication([])    # create the application
window = SpeechyKeenWindow()        # create the main window
sys.exit(App.exec_())               # run the application