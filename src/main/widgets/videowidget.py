from PyQt5 import QtWidgets, QtGui, QtCore, uic
from ..utils.videofeed import VideoFeed
from .imagelabel import ImageLabel

class VideoWidget(ImageLabel):
    """
        A Qt widget that displays video feed from a camera.

        Inherits from QLabel and displays the video using the
        labels pixmap property.
    """

    def __init__(self, camera_index = 0, width = None, height = None, *args, **kwargs):
        super().__init__(*args, **kwargs)                     # call the parents init
        self.video_feed = VideoFeed(camera_index, width, height)
        self.video_feed.new_frame_signal.connect(lambda frame: self._update_label_image(frame))
        self.mirrored = False
        self.video_feed.start()

        
    def _update_label_image(self, frame):
        height, width, color_channels = frame.shape
        bytes_per_line = 3 * width
        qImg = QtGui.QImage(frame.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
        qImg = qImg.rgbSwapped()
        qImg = qImg.mirrored(self.mirrored, False)
        self.setImage(QtGui.QPixmap(qImg))

    def kill_feed(self):
        """ stops video feed thread at next available time """
        self.video_feed.stop()