from PyQt5.QtCore import QObject, pyqtSlot
from datetime import datetime
from ...app import data

class SpeechMeta(QObject):
    """ A metric widget that submits some meta data at speech start """
    
    def __init__(self):
        """ The constructor """

        super().__init__()
        data.current_speech_data.speech_started_signal.connect(self.on_speech_start)
    
    @pyqtSlot()
    def on_speech_start(self):
        """ Callback that executes when the speech starts """
        
        data.current_speech_data.submit_single('date', datetime.now().strftime('%m-%d-%YT%H%M%S'))
        data.current_speech_data.submit_single('author', data.current_speech_notes.author())
        data.current_speech_data.submit_single('speech_name', data.current_speech_notes.speech_name())