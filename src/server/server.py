from flask import Flask, request, jsonify, send_from_directory
from PyQt5.QtCore import QThread, pyqtSignal
from ..app import data
from os import path
import netifaces


class ServerThread(QThread):
    """ The thread the server runs in """
    disfluency_received_signal = pyqtSignal(str)

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
        disfluencies = request.form['disfluencies']
        mute_ding = request.form['mute_ding']
        json_data = f'{{"disfluencies":{disfluencies}, "mute_ding":{mute_ding}}}'
        disfluency_received_signal.emit(json_data)
        return "1"
    if request.method == 'GET':
        if not data.current_speech_data.is_paused():
            return str(data.current_speech_data.get_single('disfluency_count'))
        else:
            return "0"

@flask_app.route('/images/bell.png', methods=['GET'])
def bell_image():
    d = path.dirname(path.realpath(__file__))
    return send_from_directory(path.join(d, '../resources/images/'), 'bell_icon.png')

@flask_app.route('/images/arrow.png', methods=['GET'])
def arrow_image():
    d = path.dirname(path.realpath(__file__))
    return send_from_directory(path.join(d, '../resources/images/'), 'corner_angle.png')

def run_server():
    server_thread.start()