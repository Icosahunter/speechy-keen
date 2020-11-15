from PyQt5 import QtWidgets, QtGui, uic
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from ..utils.videofeed import VideoFeed
from .imagelabel import ImageLabel
import numpy

class VideoWidget(ImageLabel):
    """
        A Qt widget that displays video feed from a camera.

        Inherits from QLabel and displays the video using the
        labels pixmap property.
    """

    frame_signal = pyqtSignal(numpy.ndarray)

    def __init__(self, camera_index = 0, width = None, height = None):
        """ The constructor """
        super().__init__()                     # call the parents init
        self.video_feed = VideoFeed(camera_index, width, height)
        self.video_feed.new_frame_signal.connect(self._update_label_image)
        self.mirrored = False
        self.video_feed.start()     # begin the video feed
        self._frame_count = 0       # tracks frames for intermittent signalling of frame_signal
        self._frame_proc = 10       # emit frame_signal every 10 frames

    @pyqtSlot(numpy.ndarray)
    def _update_label_image(self, frame):
        """ Callback that receives a frame and updates the label pixmap with the new frame """
        height, width, color_channels = frame.shape
        bytes_per_line = 3 * width
        qImg = QtGui.QImage(frame.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
        qImg = qImg.rgbSwapped()
        qImg = qImg.mirrored(self.mirrored, False)
        self.setImage(QtGui.QPixmap(qImg))

        if self._frame_count == self._frame_proc:
            self._frame_count = 0
            self.frame_signal.emit(frame)
        else:
            self._frame_count += 1

    def kill_feed(self):
        """ stops video feed thread at next available time """
        self.video_feed.stop()