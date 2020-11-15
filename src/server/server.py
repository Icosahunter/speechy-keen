from flask import Flask, request, jsonify
from PyQt5.QtCore import QThread, pyqtSignal
from os import path
import netifaces


class ServerThread(QThread):
    """ The thread the server runs in """
    disfluency_received_signal = pyqtSignal(int)

    def __init__(self, app, port):
        """ The constructor """
        super().__init__()        # call parent's init
        self.app = app
        self.port = port

    def run(self):
        """ Runs when the thread is started. Runs the server. """
        self.app.run(host='0.0.0.0', port=self.port)

flask_app = Flask(__name__)              # create flask application
flask_app.config['DEBUG'] = False        # disable debug mode
port = 5000
interface = netifaces.gateways()['default'][netifaces.AF_INET][1]
ip_address = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
full_address = ip_address + ":" + str(port)
server_thread = ServerThread(flask_app, port)
disfluency_received_signal = server_thread.disfluency_received_signal

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
        disfluency_received_signal.emit(int(request.form['clicks']))
    return "1"

def run_server():
    server_thread.start()