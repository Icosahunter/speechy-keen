from PyQt5 import QtWidgets, QtCore
from datetime import datetime, timedelta

class TimerWidget(QtWidgets.QLabel):

    def __init__(self):
        super().__init__()
        self._lap_time = datetime.now()
        self._cumul_time = timedelta(0)
        self._timer_running = False
        self._timer_id = None
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.update_text()

    def timerEvent(self, event):
        self.update_text()

    def update_text(self):
        self.setText(str(self.elapsed_time).split('.')[0])

    @property
    def timer_running(self):
        return self._timer_running

    @property
    def elapsed_time(self):
        if self.timer_running:
            return self._cumul_time + ( datetime.now() - self._lap_time )
        else:
            return self._cumul_time

    def start_timer(self):
        self._timer_running = True
        self._lap_time = datetime.now()
        self._timer_id = self.startTimer(500)
        self.update_text()

    def resume_timer(self):
        if not self._timer_running:
            self._timer_running = True
            self._lap_time = datetime.now()
            self._timer_id = self.startTimer(500)
            self.update_text()

    def pause_timer(self):
        if self._timer_running:
            self.killTimer(self._timer_id)
            self._timer_running = False
            self._cumul_time += datetime.now() - self._lap_time
            self.update_text()

    def clear_timer(self):
        if self.timer_running:
            self.killTimer(self._timer_id)
        self._timer_running = False
        self._lap_time = datetime.now()
        self._cumul_time = timedelta(0)
        self.update_text()

    def reset_timer(self):
        self.killTimer(self._timer_id)
        self._start_time = datetime.now()
        self._cumul_time = timedelta(0)
        self._timer_running = True
        self._timer_id = self.startTimer(500)
        self.update_text()