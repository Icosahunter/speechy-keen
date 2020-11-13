from PyQt5 import QtWidgets, QtCore

class ImageLabel(QtWidgets.QLabel):
    """ 
        A class for displaying properly scaled images

        Use the setImage function to set the image.
        The image will maintain it's aspect ratio.
        By default the widget will expand to fit the
        area it is given.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)           # call the parents init
        self.setMinimumWidth(1)
        self.setMinimumHeight(1)
        self.setAlignment(QtCore.Qt.AlignCenter)

    def setImage(self, img):
        """ sets the pixmap of the label with special scale properties to maintain aspect ratio """
        self.setPixmap(img.scaled(self.width(), self.height(), QtCore.Qt.KeepAspectRatio))