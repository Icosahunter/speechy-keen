import cv2
import numpy
import time
from PyQt5.QtCore import pyqtSignal, QThread, QWaitCondition

class VideoFeed(QThread):

    """
        A video feed object that captures video frames from a camera

        Inherits from QThread and thus executes on it's own thread.
        Giving a width or height of None will keep that value at it's
        default.
        Framerate can be lowered by adding a delay with the delay
        property. Delay should be given in milliseconds. Setting delay 
        to None gives maximum framerate.
    """

    new_frame_signal = pyqtSignal(numpy.ndarray)                        # create Qt signal that fires when a new frame is received
                                                                        # it must be declared outside __init__ due to the way pyqtSignal is implemented

    def __init__(self, camera_index = 0, width = None, height = None):
        super().__init__()                                              # call the parents init
        self.__camera_device = cv2.VideoCapture(camera_index)           # creates the camera device object (cv2.VideoCapture)
        if not width == None:
            self.__camera_device.set(cv2.CAP_PROP_FRAME_WIDTH, width)   # set camera frame width
        if not height == None:
            self.__camera_device.set(cv2.CAP_PROP_FRAME_HEIGHT, height) # set camera frame height
        self.delay = None                                               # set delay to None for maximum framerate
        self.__est_fps = 0                                              # framerate estimated using time.perf_counter
        self.__last_time = 0                                            # used to time frames for fps estimation
        self.__est_smth = 0.875                                         # weight given to old data in fps estimation

    @property
    def camera_fps(self):
        """ The frames per second reported by the camera device """
        return self.__camera_device.get(cv2.CAP_PROP_FPS)

    @property
    def fps(self):
        """ The frames per second estimated by this class using python timers """
        return self.__est_fps

    def stop(self):
        """ stops execution at next available time """
        self.requestInterruption()
        self.wait()

    def __del__(self):
        """ safely stops the thread if the object is deleted """
        self.stop()

    def get_frame(self):
        """ requests a single frame seperate from the main feed """
        got_frame, frame = self.__camera_device.read()          # get a frame from the camera
        return frame

    def run(self):
        """ the main thread loop """
        self.__last_time = time.perf_counter()                          # initialize t0 used for calculating est. fps

        while True:
            if self.isInterruptionRequested():                          # if received a request to stop the thread
                self.__camera_device.release()                          # release the video camera resource
                return                                                  # and stop the thread
            else:
                if self.delay != None:
                    self.msleep(self.delay)
                
                got_frame, frame = self.__camera_device.read()          # get a frame from the camera
                
                if got_frame:                                           # if successfully retrieved frame
                    self.new_frame_signal.emit(frame)                   # fire the new frame signal
                    now_time = time.perf_counter()                      # get the current time (t1)
                    new_est = 1/(now_time - self.__last_time)           # get the new fps estimate
                    self.__est_fps = self.__est_smth*self.__est_fps + (1 - self.__est_smth)*new_est # set the estimate, weighted by est_smth
                    self.__last_time = now_time                         # set the t0 to t1
