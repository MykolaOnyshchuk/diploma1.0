from PyQt5 import QtCore, QtSql, QtWidgets
from views.TrainImageNetView import TrainImageNetView
from models.camera.SingleCameraModel import SingleCameraModel


class TrainImageNetController(QtCore.QObject):
    def __init__(self, table, model):
        super().__init__(None)
        self.__model = model
        self.cameras = []

        count_cameras = self.__model.rowCount()
        for i in range(0, count_cameras):
            index = self.__model.index(i, 0)
            self.cameras.append(SingleCameraModel(index))

        self.__image_net_view = TrainImageNetView(table, self.cameras)
        self.__image_net_view.refresh()
