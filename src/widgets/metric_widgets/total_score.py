from PyQt5.QtCore import QObject, pyqtSlot
from ...app import data

class TotalScore(QObject):
    def __init__(self):
        super().__init__()
    
    @pyqtSlot()
    def on_speech_end():
        all_scores = data.current_speech_data.get_all_scores()
        total_score = sum(all_scores)/len(all_scores)
        data.current_speech_data.submit_score('total_score', total_score)