from models.Observable import Observable, event
from PyQt5 import QtCore
from models.line.LineModel import LineModel
from classes.ImageDataSetThread import ImageDataSetThread
from classes.LearnImageNetThread import LearnImageNetThread
from classes.RunImageNetThread import RunImageNetThread


class SingleLineModel(Observable):
    def __init__(self, index):
        super().__init__()
        self.__status = ''
        self.__progress_max = 100
        self.__progress_value = 0
        self.__index = index
        self.__busy = False
        self.title = index.data(QtCore.Qt.DisplayRole)
        self.camera_id = index.data(LineModel.CameraRole)
        self.id = index.data(LineModel.IdRole)
        self.coords = index.data(LineModel.CoordsRole)

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

    def generate_dataset(self):
        if self.__busy:
            print('busy')
            return
        self.__set_busy(True)
        self.status = 'Генерація датасету'

        thread = ImageDataSetThread(self.camera_id, self.id, self.coords)
        thread.signals.add_observer('set_update_progress', self.set_progress_value)
        thread.signals.add_observer('set_update_progress_max', self.set_progress_max)
        thread.signals.add_observer('set_update_status', self.set_status)
        thread.signals.add_observer('set_finished', lambda: self.__set_busy(False))
        thread.start()

    def train(self):
        if self.__busy:
            print('busy')
            return
        self.__set_busy(True)
        self.status = 'Навчання мережі'

        thread = LearnImageNetThread(self.camera_id, self.id)
        thread.signals.add_observer('set_update_progress', self.set_progress_value)
        thread.signals.add_observer('set_update_progress_max', self.set_progress_max)
        thread.signals.add_observer('set_update_status', self.set_status)
        thread.signals.add_observer('set_finished', lambda: self.__set_busy(False))
        thread.start()
        # thread = RunImageNetThread('D:/intensity/18/cam18stream_1579869707.mp4', self.coords)
        # thread.start()

    status = property(get_status, set_status)
    progress_max = property(get_progress_max, set_progress_max)
    progress_value = property(get_progress_value, set_progress_value)
