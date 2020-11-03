from flask import Flask, request, jsonify
from PyQt5.QtCore import QThread, pyqtSignal
from os import path
import socket


class ServerThread(QThread):

    def __init__(self, app, port):
        super().__init__()        # call parent's init
        self.app = app
        self.port = port

    def run(self):
        self.app.run(host='0.0.0.0', port=self.port)

flask_app = Flask(__name__)              # create flask application
flask_app.config['DEBUG'] = False        # disable debug mode
port = 5000                              # 49152 to 65535
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
full_address = ip_address + ":" + str(port)
server_thread = ServerThread(flask_app, port)
disfluency_received_signal = pyqtSignal(int)

@flask_app.route('/', methods=['GET'])
def home():
    page = ""
    d = path.dirname(path.realpath(__file__))
    with open(path.join(d, "mobile_gui_v2.html"), 'r') as f:
        page = f.read()
    return page

@flask_app.route('/disfluencies', methods=['GET', 'POST'])
def disfluencies():
    if request.method == 'POST':
        disfluency_received_signal.emit(request.form['clicks'])
    return "1"

def run_server():
    server_thread.start()