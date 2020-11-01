from PyQt5 import QtWidgets, QtGui, uic
from PyQt5.QtCore import Qt
from os import path
import json

class ReportViewer(QtWidgets.QWidget):

    def __init__(self):
        d = path.dirname(path.realpath(__file__))
        super().__init__()
        uic.loadUi(path.join(d, 'reportviewer.ui'), self)   # load the ui file
        self._plot_width = 400
        self._plot_height = 10
        self.plotScene = None
        
    def OpenReport(self, path):
        self.report = {}
        with open(path, 'r') as f:
            self.report = json.loads(f.read())
    
    def ShowReport(self):

        # Handle creating and showing data stream plots
        stream_count = len(self.report['stream_data'])
        time_px = (self._plot_width - 50)/self.report['single_data']['speech_length']

        for key in self.report['stream_data']:

            main_data_key = self.report['stream_data'][key]['main_data']
            scene = QtWidgets.QGraphicsScene(0, 0, self._plot_width, self._plot_height)

            # add ruler lines to scene
            for i in range(100):
                h = self._plot_height/20
                if i%50 == 0:
                    h = 16*h
                elif i%25 == 0:
                    h = 8*h
                elif i%5 == 0:
                    h = 4*h
                x1 = self._plot_width*i/100
                y1 = self._plot_height
                x2 = self._plot_width*i/100
                y2 = self._plot_height - h
                scene.addLine(x1, y1, x2, y2)

            # add data points to scene
            for d in self.report['stream_data'][key]['stream']:

                color = self.report['stream_data'][key]['colors'][str(d[main_data_key])]
                brush = QtGui.QBrush(QtGui.QColor(color), Qt.SolidPattern)
                time  = d['time_stamp']

                scene.addEllipse(time*time_px, 0, self._plot_height, self._plot_height, QtGui.QPen(), brush)

            # add everything to the report form
            k = QtWidgets.QLabel(self.PrettyName(key))
            v = QtWidgets.QGraphicsView(scene)
            v.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Ignored)
            self.reportForm.addRow(k, v)

            # add legend entries to the report form
            for c in self.report['stream_data'][key]['colors']:
                k = QtWidgets.QLabel(c)
                v = QtWidgets.QLabel()
                v.setStyleSheet('background: ' + self.report['stream_data'][key]['colors'][c] + ';')
                self.reportForm.addRow(k, v)

        # handle creating and showing single datas
        for key in self.report['single_data']:
            k = QtWidgets.QLabel(self.PrettyName(key))
            v = QtWidgets.QLabel(str(self.report['single_data'][key]))
            self.reportForm.addRow(k, v)

    def PrettyName(self, name):
        return ' '.join(x.capitalize() for x in name.split('_')) + ' : '