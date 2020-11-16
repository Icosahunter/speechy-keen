from PyQt5 import QtWidgets, QtGui, uic
from PyQt5.QtCore import Qt, pyqtSlot, QUrl
from ..app import data
from ..utils import qtimeconversion as qtc
from os import path
import json

class ReportViewer(QtWidgets.QWidget):
    """ A widget that displays a speech report """

    def __init__(self):
        """ The constructor """
        d = path.dirname(path.realpath(__file__))
        super().__init__()
        uic.loadUi(path.join(d, 'reportviewer.ui'), self)   # load the ui file
        self._plot_width = 600
        self._plot_height = 42
        self._legend_height = 22
        self._report_path = None
        self.plotScene = None
        self.closeButton.clicked.connect(self.close_button_clicked)
        self.saveButton.clicked.connect(self.save_button_clicked)
        self.openFileLocationButton.clicked.connect(self.open_file_location_button_clicked)

    @pyqtSlot()
    def open_file_location_button_clicked(self):
        """ Callback that executes when the open file location button is clicked """
        directory = '/'.join(self._report_path.split('/')[0:-1])
        url = QUrl.fromLocalFile(directory)
        QtGui.QDesktopServices.openUrl(url)

    @pyqtSlot()
    def close_button_clicked(self):
        """ Callback that executes when the close button is clicked """
        self.close()

    @pyqtSlot()
    def save_button_clicked(self):
        """ Callback that executes when the save button is clicked """
        report_file_name = self.report['single_data']['speech_name'] + ' ' + self.report['single_data']['date']
        self._report_path = data.store_data('documents/speech_reports/' + report_file_name, self.report)
        self.saveButton.setHidden(True)
        self.openFileLocationButton.setHidden(False)

    def open_file(self, report_path):
        """ Loads a report from a file """
        self.report = {}
        self._report_path = report_path
        with open(path, 'r') as f:
            self.report = json.loads(f.read())
        self.saveButton.setHidden(True)

    def open_dict(self, report_dict):
        """ Loads a report from a dictionary object """
        self.report = report_dict
        self.openFileLocationButton.setHidden(True)
    
    def show_report(self):
        """ Builds the graphical representation of the report and shows the widget """
        # Handle creating and showing data stream plots
        stream_count = len(self.report['stream_data'])
        speech_len = qtc.str_to_seconds(self.report['single_data']['speech_length'])
        time_px = (self._plot_width - 50)/speech_len

        for key in self.report['stream_data']:

            main_data_key = self.report['stream_data'][key]['main_data']
            scene = QtWidgets.QGraphicsScene(0, 0, self._plot_width, self._plot_height)

            # add ruler lines to scene
            for i in range(100):
                h = self._plot_height/30
                if i%50 == 0:
                    h = 16*h
                elif i%25 == 0:
                    h = 8*h
                elif i%5 == 0:
                    h = 4*h
                x1 = self._plot_width*i/100
                y1 = self._plot_height - self._legend_height
                x2 = self._plot_width*i/100
                y2 = self._plot_height - self._legend_height - h
                scene.addLine(x1, y1, x2, y2)

            x = 0
            y = self._plot_height - self._legend_height
            w = self._plot_width
            h = self._legend_height
            brush = QtGui.QBrush(QtGui.QColor('#AAAAAA'), Qt.SolidPattern)
            scene.addRect(x, y, w, h, QtGui.QPen(), brush)

            # add data points to scene
            for d in self.report['stream_data'][key]['stream']:

                color = '#000000'
                try:
                    color = self.report['stream_data'][key]['colors'][str(d[main_data_key])]
                except KeyError:
                    try:
                        color = self.report['stream_data'][key]['colors']['default']
                    except KeyError:
                        pass

                brush = QtGui.QBrush(QtGui.QColor(color), Qt.SolidPattern)
                time  = d['time_stamp']
                ellip_size = 0.5*(self._plot_height - self._legend_height)
                ellip_margin = 0.2*(self._plot_height - self._legend_height)
                scene.addEllipse(time*time_px, ellip_margin, ellip_size, ellip_size, QtGui.QPen(), brush)

            ellip_size = 0.5*self._legend_height
            ellip_y = self._plot_height - 1.3*ellip_size
            txt_inc = self._plot_width / len(self.report['stream_data'][key]['colors'])
            txt_x = ellip_size + 5
            txt_y = self._plot_height - self._legend_height
            # add legend entries to the report form
            for c in self.report['stream_data'][key]['colors']:

                color = self.report['stream_data'][key]['colors'][c]
                brush = QtGui.QBrush(QtGui.QColor(color), Qt.SolidPattern)
                scene.addEllipse(txt_x - ellip_size - 1, ellip_y, ellip_size, ellip_size, QtGui.QPen(), brush)

                txt = scene.addText(c)
                txt.setPos(txt_x, txt_y)
                txt_x += txt_inc


            # add everything to the report form
            k = QtWidgets.QLabel(self.pretty_name(key))
            v = QtWidgets.QGraphicsView(scene)
            v.setMaximumHeight(self._plot_height + 10)
            v.setMaximumWidth(self._plot_width + 10)
            self.reportForm.addRow(k, v)

        # handle creating and showing single datas
        for key in self.report['single_data']:
            k = QtWidgets.QLabel(self.pretty_name(key))
            v = QtWidgets.QLabel(str(self.report['single_data'][key]))
            self.reportForm.addRow(k, v)

        self.show()

    def pretty_name(self, name):
        """ Converts a lowercase underscored string to capitalized and spaced """
        return ' '.join(x.capitalize() for x in name.split('_')) + ' : '