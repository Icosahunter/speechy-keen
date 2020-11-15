from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QThread
from ...app import data
from fer import FER
import numpy

class FacialAnalyzerWidget(QtWidgets.QLabel):
    """ A metric widget for tracking facial expressions """

    def __init__(self):
        """  """
        super().__init__()
        self.facial_analyzer = FER()
        data.current_speech_data.speech_started_signal.connect(self.on_speech_start)
        data.current_speech_data.speech_finished_signal.connect(self.on_speech_end)


    @pyqtSlot()
    def on_speech_start(self):
        """ Callback that executes when the speech starts """
        colors = {
            "happy"     : "#f5f242",
            "sad"       : "#4260f5",
            "surprise"  : "#42f54e",
            "fear"      : "#8f8f8f",
            "angry"     : "#f54542",
            "neutral"   : "#ffffff",
            "default"   : "#000000"
        }
        data.current_speech_data.create_stream("expression_stream", "expression", colors)

    @pyqtSlot()
    def on_speech_end(self):
        """ Callback that executes when the speech ends """
        good_expressions = data.get_data('settings/scoring/good_expressions').split(', ')
    
        expressions = data.current_speech_data.get_stream('expression_stream')
        expressions = [x['expression'] for x in expressions]

        expr_score = sum(x in expressions for x in good_expressions) / len(expressions)
        data.current_speech_data.submit_single('expression_score', expr_score)

    @pyqtSlot(numpy.ndarray)
    def update_facial_analysis(self, frame):
        """ Callback that executes when a new frame for analysis is received """

        if not data.current_speech_data.is_paused():
            try:
                emotion, confidence = self.facial_analyzer.top_emotion(frame)
                self.setText('{:.0%} : {}'.format(confidence, emotion))
                data.current_speech_data.submit_stream_data('expression_stream', {'confidence': str(confidence), 'expression': emotion})
            except:
                pass
