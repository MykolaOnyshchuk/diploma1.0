from PySide6 import QtCore, QtSql, QtWidgets
from PySide6.QtSql import *
from PySide6.QtGui import QPixmap, QImage
from views.MainWindow import Ui_MainWindow
from views.CameraConfig import CameraConfig
from views.DefaultPlot import DefaultPlot
from views.TrainImageNetView import TrainImageNetView
from models.camera.CameraModel import CameraModel
from models.camera.CameraSql import CameraSql
from models.line.LineSql import LineSql
from classes.LearnUnetThread import LearnUnetThread
from controllers.TrainImageNetController import TrainImageNetController
import cv2
import os
from models.line.LineModel import LineModel
import numpy as np
from classes.Line import Line
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from classes.CVThread import CVThread
from classes.CalculateParams import CalculateParams
import time

from ReccurentNet import ReccurentNet
from Database import Database


class WorkThread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        for i in range(6):
            print(i)
            time.sleep(0.3)  # artificial time delay
            self.emit(QtCore.SIGNAL('update(QString)'), "from work thread " + str(i))


class MainController(QtCore.QObject):
    def __init__(self):
        super().__init__(None)

        self.__init_models()
        self.__init_main_view()
        self.__init_slots()

    def __init_models(self):
        # cameras
        self.__selected_cameras = CameraModel(CameraSql.selected())
        self.__selected_cameras.open()
        self.__all_cameras = CameraModel(CameraSql.all())
        self.__all_cameras.open()

    def __init_main_view(self):
        self.__main_ui = Ui_MainWindow()
        self.__main_window = QtWidgets.QMainWindow()
        self.__main_ui.setupUi(self.__main_window)

        self.__main_ui.list_selected_cameras.setModel(self.__selected_cameras)
        self.__main_ui.list_cameras.setModel(self.__all_cameras)

        # train u-net
        self.image_net_controller = TrainImageNetController(self.__main_ui.table_segmentation,
                                                              self.__selected_cameras)

    def __init_slots(self):
        # cameras
        self.__main_ui.add_camera.clicked.connect(
            lambda: CameraSql.select_camera(
                self.__main_ui.list_cameras.selectionModel().currentIndex().data(CameraModel.IdRole),
                self.__selected_cameras))
        self.__main_ui.delete_camera.clicked.connect(
            lambda: CameraSql.delete_selected_camera(
                self.__main_ui.list_selected_cameras.selectionModel().currentIndex().data(CameraModel.IdRole),
                self.__selected_cameras))
        self.__main_ui.config_camera.clicked.connect(
            lambda: CameraConfig.exec(self.__main_ui.list_selected_cameras.selectionModel().currentIndex()))
        self.__main_ui.run_camera.clicked.connect(
            lambda: LearnUnetThread.run_for_cameras(self.__selected_cameras))
        self.__main_ui.start_calc_params.clicked.connect(self.__calc_params)

    def run(self):
        self.__main_window.show()
        # CameraConfig.exec(6)

        # x, y = Database.get_stat_cameras_for_net()
        xtest, ytest, xtsp = Database.get_stat_cameras_for_net2()
        # print(x,y)
        net = ReccurentNet()
        net.run2(xtest, ytest, xtsp)
        # net.run(x, y, xtest, ytest, xtsp)
        # calc = CalculateParams()
        # calc.run()

    def __calc_params(self):
        self.__main_ui.start_calc_params.setEnabled(False)

        plot_layout = QtWidgets.QGridLayout()
        plot_layout.setSpacing(0)
        self.__main_ui.plots.setLayout(plot_layout)

        for i in range(0, self.__selected_cameras.rowCount()):
            camera_id = CameraSql.get_id(self.__selected_cameras.record(i))
            camera_title = CameraSql.get_title(self.__selected_cameras.record(i))
            plot_layout.addWidget(DefaultPlot(camera_id, camera_title))