from models.Observable import Observable, event
from PySide6 import QtCore
from models.camera.CameraModel import CameraModel
from models.line.SingleLineModel import SingleLineModel
from models.line.LineSql import LineSql
from models.line.LineModel import LineModel
from classes.Video import Video
from classes.CVThread import CVThread
from classes.LoadVideoThread import LoadVideoThread
import os


class SingleCameraModel(Observable, QtCore.QObject):
    def __init__(self, index):
        Observable.__init__(self)
        QtCore.QObject.__init__(self)
        self.__status = ''
        self.__progress_max = 100
        self.__progress_value = 0
        self.__index = index
        self.__busy = False
        self.pixmap = index.data(QtCore.Qt.DecorationRole)
        self.title = index.data(CameraModel.TextRole)
        self.gplmod = self.__index.data(CameraModel.GplModRole)
        self.server = self.__index.data(CameraModel.ServerRole)
        self.id = self.__index.data(CameraModel.IdRole)
        self.lines = []
        self.__init_lines()

    def __init_lines(self):
        self.__line_model = LineModel(LineSql.all_from_camera(self.id))
        self.__line_model.open()
        for i in range(0, self.__line_model.rowCount()):
            self.lines.append(SingleLineModel(self.__line_model.index(i, 0)))

    def __set_busy(self, value):
        self.__busy = value

    def get_status(self):
        return self.__status

    @event
    def set_status(self, value):
        self.__status = value

    def get_progress_max(self):
        return self.__progress_max

    @event
    def set_progress_max(self, value):
        self.__progress_max = value

    def get_progress_value(self):
        return self.__progress_value

    @event
    def set_progress_value(self, value):
        self.__progress_value = value

    def load_video(self):
        if self.__busy:
            print('busy')
            return
        self.__set_busy(True)
        self.status = 'Завантаження відео'

        thread = LoadVideoThread(self.id, self.gplmod, self.server)
        thread.signals.add_observer('set_update_progress', self.set_progress_value)
        thread.signals.add_observer('set_update_progress_max', self.set_progress_max)
        thread.signals.add_observer('set_update_status', self.set_status)
        thread.signals.add_observer('set_finished', lambda: self.__set_busy(False))
        thread.start()

    def run_cv(self):
        if self.__busy:
            print('busy')
            return
        self.__set_busy(True)
        self.status = 'Обробка зображень'

        thread = CVThread(self.id)
        thread.signals.add_observer('set_update_progress', self.set_progress_value)
        thread.signals.add_observer('set_update_progress_max', self.set_progress_max)
        thread.signals.add_observer('set_update_status', self.set_status)
        thread.signals.add_observer('set_finished', lambda: self.__set_busy(False))
        thread.start()

    status = property(get_status, set_status)
    progress_max = property(get_progress_max, set_progress_max)
    progress_value = property(get_progress_value, set_progress_value)
