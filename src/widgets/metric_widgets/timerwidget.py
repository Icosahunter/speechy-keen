from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot
from datetime import datetime, timedelta
from ...utils import qtimeconversion as qtc
from ...app import data

class TimerWidget(QtWidgets.QLabel):
    """ A metric widget for keeping time """

    def __init__(self):
        """ The constructor """
        super().__init__()
        self._lap_time = datetime.now()
        self._cumul_time = timedelta(0)
        self._timer_running = False
        self._timer_id = None
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.update_text()
        self.base_stylesheet = 'color: white; font-weight: 500;'
        data.current_speech_data.speech_started_signal.connect(self.on_speech_start)
        data.current_speech_data.speech_finished_signal.connect(self.on_speech_end)
        data.current_speech_data.speech_resumed_signal.connect(self.on_speech_resume)
        data.current_speech_data.speech_paused_signal.connect(self.on_speech_pause)

    @pyqtSlot()
    def on_speech_start(self):
        """ Callback that executes when the speech starts """
        self.start_timer()
    
    @pyqtSlot()
    def on_speech_end(self):
        """ Callback that executes when the speech ends """
        speech_len = self.elapsed_time
        
        goal_len = qtc.str_to_seconds(data.get_data('settings/scoring/goal_speech_length'))
        
        len_score = (1 - (abs(speech_len.total_seconds() - goal_len)/goal_len))
        len_score = int(100 * len_score)

        data.current_speech_data.submit_single('speech_length', qtc.timedelta_to_str(speech_len))
        data.current_speech_data.submit_score('speech_length_score', len_score)
        
        self.clear_timer()

    @pyqtSlot()
    def on_speech_pause(self):
        """ Callback that executes when the speech gets paused """
        self.pause_timer()

    @pyqtSlot()
    def on_speech_resume(self):
        """ Callback that executes when the speech resumes """
        self.resume_timer()

    def timerEvent(self, event):
        """ Callback for this widgets timer which will execute every half second """
        self.update_text()
        color = 'transparent'
        max_alarm = timedelta(seconds = 0)
        for a in data.get_data('settings/alarms'):
            t = qtc.str_to_timedelta(a['time'])
            if self.elapsed_time >= t and self.elapsed_time <= t + timedelta(seconds = 5):
                if t > max_alarm:
                    max_alarm = t
                    color = a['color']
        self.setStyleSheet(self.base_stylesheet + 'background: ' + color + ';')

    def update_text(self):
        """ Updates the text of the timer """
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
        data.current_speech_data.set_time_keeping(self._cumul_time, self._lap_time)
        self.update_text()

    def resume_timer(self):
        if not self._timer_running:
            self._timer_running = True
            self._lap_time = datetime.now()
            self._timer_id = self.startTimer(500)
            data.current_speech_data.set_time_keeping(self._cumul_time, self._lap_time)
            self.update_text()

    def pause_timer(self):
        if self._timer_running:
            self.killTimer(self._timer_id)
            self._timer_running = False
            self._cumul_time += datetime.now() - self._lap_time
            data.current_speech_data.set_time_keeping(self._cumul_time, self._lap_time)
            self.update_text()

    def clear_timer(self):
        if self.timer_running:
            self.killTimer(self._timer_id)
        self._timer_running = False
        self._lap_time = datetime.now()
        self._cumul_time = timedelta(0)
        data.current_speech_data.set_time_keeping(self._cumul_time, self._lap_time)
        self.update_text()

    def reset_timer(self):
        self.killTimer(self._timer_id)
        self._start_time = datetime.now()
        self._cumul_time = timedelta(0)
        self._timer_running = True
        self._timer_id = self.startTimer(500)
        data.current_speech_data.set_time_keeping(self._cumul_time, self._lap_time)
        self.update_text()