import sys
from PyQt5 import QtWidgets, uic
from src.app.app import SpeechyKeenWindow
from src.server.server import run_server
import src.server.server as server

run_server()                        # run the server
App = QtWidgets.QApplication([])    # create the application
window = SpeechyKeenWindow()        # create the main window
sys.exit(App.exec_())               # run the application
