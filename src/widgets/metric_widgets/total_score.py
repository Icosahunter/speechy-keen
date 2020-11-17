from PyQt5.QtCore import QObject, pyqtSlot
from ...app import data

class TotalScore(QObject):
    """ A metric widget that computes and submits the total score """
    
    def __init__(self):
        """ The constructor """
        super().__init__()
        data.current_speech_data.speech_finished_signal.connect(self.on_speech_end)
    
    @pyqtSlot()
    def on_speech_end(self):
        """ Callback that executes when the speech ends """
        all_scores = data.current_speech_data.get_all_scores()
        total_score = int(sum(all_scores)/len(all_scores))
        data.current_speech_data.submit_score('total_score', total_score)