import sys
from PyQt5 import QtWidgets, uic
from threading import Thread
from datetime import datetime

def timer_thread_update(simpleTimer):
    while simpleTimer.run_timer:
        current_time = datetime.now()
        elapsed_time = current_time - simpleTimer.start_time
        simpleTimer.textWidget.text = str(elapsed_time)

class SimpleTimer():

    def __init__(self, textWidget):
        self.textWidget = textWidget
        self.thread = Thread(target=timer_thread_update, args=(self,))
        self.start_time = None
        self.thread.start()
        self.run_timer = False

    def start(self):
        self.run_timer = True
        self.thread.run()

    def stop(self):
        self.run_timer = False
        self.start_time = datetime.now()

    def pause(self):
        self.run_timer = False

    def restart(self):
        self.start_time = datetime.now()
