from models.camera.CameraModel import CameraModel
from models.camera.CameraSql import CameraSql
from models.line.LineSql import LineSql
from classes.Video import Video
from PIL import ImageQt
from PySide6 import QtCore, QtSql, QtWidgets
from PySide6.QtGui import QPixmap, QImage, QColor, QMouseEvent, QPainter, QPen, Qt
from PySide6.QtCore import QPoint, QLine
from views.CameraConfigDialog import Ui_CameraConfigDialog
from models.line.LineModel import LineModel
import cv2
import numpy as np

import imageio as iio


class CameraConfig(QtWidgets.QWidget):
    def __init__(self, frame, camera_id):
        super().__init__()
        self.__camera_id = camera_id
        self.__frame = frame
        self.__dialog = QtWidgets.QDialog()
        self.__ui = Ui_CameraConfigDialog()
        self.__ui.setupUi(self.__dialog)
        # model
        self.__line_model = LineModel(LineSql.all_from_camera(self.__camera_id))
        self.__line_model.open()
        self.__ui.lines.setModel(self.__line_model)
        # # self.__line_model = None
        # show picture
        self.__set_pixmap(self.__frame)
        self._new_lane_points = []

        self.qimg = None
        self.pixmap = None
        self.q_points = []
        self.q_lines = []

        # inits
        self.__init_spinbox()
        self.__init_buttons()

    def __init_buttons(self):
        # slot buttons
        self.__ui.add_line.clicked.connect(
            lambda: LineSql.add_line(self.__camera_id, self.__get_current_list_coords(), self.__line_model))
        self.__ui.delete_line.clicked.connect(
            lambda: LineSql.delete(
                self.__ui.lines.selectionModel().currentIndex().data(LineModel.IdRole), self.__line_model))
        self.__ui.lines.doubleClicked.connect(
            lambda: self.__set_current_list_coords_from_db())
        self.__ui.show_lines.stateChanged.connect(self.__draw_current_line)

    def __init_spinbox(self):
        # range spinboxes
        max_y, max_x, colors = self.__frame.shape
        self.__ui.coordX.setRange(0, max_x)
        self.__ui.coordY.setRange(0, max_y)
        self.__ui.coordX_2.setRange(0, max_x)
        self.__ui.coordY_2.setRange(0, max_y)
        self.__ui.coordX_3.setRange(0, max_x)
        self.__ui.coordY_3.setRange(0, max_y)
        self.__ui.coordX_4.setRange(0, max_x)
        self.__ui.coordY_4.setRange(0, max_y)
        # slots
        self.__ui.coordX.valueChanged.connect(self.__draw_current_line)
        self.__ui.coordY.valueChanged.connect(self.__draw_current_line)
        self.__ui.coordX_2.valueChanged.connect(self.__draw_current_line)
        self.__ui.coordY_2.valueChanged.connect(self.__draw_current_line)
        self.__ui.coordX_3.valueChanged.connect(self.__draw_current_line)
        self.__ui.coordY_3.valueChanged.connect(self.__draw_current_line)
        self.__ui.coordX_4.valueChanged.connect(self.__draw_current_line)
        self.__ui.coordY_4.valueChanged.connect(self.__draw_current_line)

        self.__ui.coordX.valueChanged.connect(self._update_coord_x)
        self.__ui.coordY.valueChanged.connect(self._update_coord_y)
        self.__ui.coordX_2.valueChanged.connect(self._update_coord_x2)
        self.__ui.coordY_2.valueChanged.connect(self._update_coord_y2)
        self.__ui.coordX_3.valueChanged.connect(self._update_coord_x3)
        self.__ui.coordY_3.valueChanged.connect(self._update_coord_y3)
        self.__ui.coordX_4.valueChanged.connect(self._update_coord_x4)
        self.__ui.coordY_4.valueChanged.connect(self._update_coord_y4)

    def __set_current_list_coords_from_db(self):
        index = self.__ui.lines.selectionModel().currentIndex()
        line_id = index.data(LineModel.IdRole)
        if not line_id:
            return
        self.__ui.coordX.setValue(index.data(LineModel.CoordXRole))
        self.__ui.coordY.setValue(index.data(LineModel.CoordYRole))
        self.__ui.coordX_2.setValue(index.data(LineModel.Coord2XRole))
        self.__ui.coordY_2.setValue(index.data(LineModel.Coord2YRole))
        self.__ui.coordX_3.setValue(index.data(LineModel.Coord3XRole))
        self.__ui.coordY_3.setValue(index.data(LineModel.Coord3YRole))
        self.__ui.coordX_4.setValue(index.data(LineModel.Coord4XRole))
        self.__ui.coordY_4.setValue(index.data(LineModel.Coord4YRole))

    def __set_spinboxes_values(self, coords):
        self.__ui.coordX.setValue(coords[0][0])
        self.__ui.coordY.setValue(coords[0][1])
        self.__ui.coordX_2.setValue(coords[1][0])
        self.__ui.coordY_2.setValue(coords[1][1])
        self.__ui.coordX_3.setValue(coords[2][0])
        self.__ui.coordY_3.setValue(coords[2][1])
        self.__ui.coordX_4.setValue(coords[3][0])
        self.__ui.coordY_4.setValue(coords[3][1])

    def __get_current_list_coords(self):
        list_coords = [[self.__ui.coordX.value(), self.__ui.coordY.value()],
                       [self.__ui.coordX_2.value(), self.__ui.coordY_2.value()],
                       [self.__ui.coordX_3.value(), self.__ui.coordY_3.value()],
                       [self.__ui.coordX_4.value(), self.__ui.coordY_4.value()]]
        return list_coords

    def __draw_current_line(self):
        frame = self.__frame.copy()
        list_coords = self.__get_current_list_coords()
        for i in range(0, len(list_coords)):
            list_coords[i][0] *= 2
            list_coords[i][1] *= 2

        CameraConfig.__show_line_on_frame(list_coords, frame)
        if self.__ui.show_lines.isChecked():
            for i in range(0, self.__line_model.rowCount()):
                CameraConfig.__show_line_on_frame(LineSql.get_list_coords(self.__line_model.record(i)), frame)
        self.__set_pixmap(frame)

    @staticmethod
    def __show_line_on_frame(list_coords, frame):
        if not LineSql.check_coords(list_coords):
            return
        pts = np.array(list_coords, np.int32).reshape((- 1, 1, 2))
        cv2.fillPoly(frame, [pts], (255, 255, 255))

    def show(self):
        if self.__dialog.exec_() == QtWidgets.QDialog.DialogCode.Accepted:
            print('yeah')

    def __set_pixmap(self, frame):
        self.qimg = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        self.pixmap = QPixmap.fromImage(self.qimg).scaledToHeight(400)
        self.__ui.label.setPixmap(self.pixmap)
        #     qimg.height() / 2

        self.__ui.label.mousePressEvent = self.get_pixel

    def get_pixel(self, e):
        print("pressed")
        x = e.pos().x()
        y = e.pos().y()
        self._add_point_to_new_lane(x * 2, y * 2)
        self.update_spinboxes()
        # qp = QPainter(self.pixmap)
        # qp.drawPixmap(self.rect(), self.pixmap)
        q_point = QPoint(e.pos().x(), e.pos().y())
        self.q_points.append(q_point)

        self._draw_dots_and_lines()

        print("pressed two", x, y, sep="; ")
        # self.update()
        # c = self.qimg.pixel(x, y)  # color code (integer): 3235912
        #print("pressed three")
        # depending on what kind of value you like (arbitary examples)
        # c_qobj = QColor(c)  # color object
        # c_rgb = QColor(c).getRgb()  # 8bit RGBA: (255, 23, 0, 255)
        # c_rgbf = QColor(c).getRgbf()  # RGBA float: (1.0, 0.3123, 0.0, 1.0)
        #print("pressed four")
        #print(x + ' and ' + y)
        return x, y#, c_rgb

    def update_spinboxes(self):
        curr_points = self.__get_current_list_coords()
        for i in range(0, self._new_lane_points.__len__()):
            curr_points[i][0] = self._new_lane_points[i][0] / 2
            curr_points[i][1] = self._new_lane_points[i][1] / 2
        self.__set_spinboxes_values(curr_points)

    def _add_point_to_new_lane(self, x, y):
        self._new_lane_points.append([x, y])

    def build_q_lines(self):
        self.q_lines.clear()
        if len(self.q_points) >= 2:
            for i in range(0, len(self.q_points) - 1):
                self.q_lines.append(QLine(self.q_points[i], self.q_points[i + 1]))
            if len(self.q_points) == 4:
                self.q_lines.append(QLine(self.q_points[0], self.q_points[3]))

    def _draw_dots_and_lines(self):
        qp = QPainter(self.pixmap)
        blue_pen = QPen(Qt.GlobalColor.cyan, 3, Qt.PenStyle.SolidLine)
        qp.setPen(blue_pen)
        # qp.drawEllipse(e.pos().x() - 5, e.pos().y() - 5, 10, 10)
        qp.drawPoints(self.q_points)
        self.build_q_lines()
        qp.drawLines(self.q_lines)
        # for i in (0, len(self.q_points)):
        #     qp.drawPoint(self.q_points[i])
        self.__ui.label.setPixmap(self.pixmap)
        self.__ui.label.show()

    def _update_coord_x(self):
        # print(self.__ui.coordX.sender())
        self._update_coord_value_from_spinbox(True, 0, self.__ui.coordX.value())

    def _update_coord_y(self):
        # print(self.__ui.coordY.sender())
        self._update_coord_value_from_spinbox(False, 0, self.__ui.coordY.value())

    def _update_coord_x2(self):
        # print(self.__ui.coordX_2.sender())
        self._update_coord_value_from_spinbox(True, 1, self.__ui.coordX_2.value())

    def _update_coord_y2(self):
        # print(self.__ui.coordY_2.sender())
        self._update_coord_value_from_spinbox(False, 1, self.__ui.coordY_2.value())

    def _update_coord_x3(self):
        # print(self.__ui.coordX_3.sender())
        self._update_coord_value_from_spinbox(True, 2, self.__ui.coordX_3.value())

    def _update_coord_y3(self):
        # print(self.__ui.coordY_3.sender())
        self._update_coord_value_from_spinbox(False, 2, self.__ui.coordY_3.value())

    def _update_coord_x4(self):
        # print(self.__ui.coordX_4.sender())
        self._update_coord_value_from_spinbox(True, 3, self.__ui.coordX_4.value())

    def _update_coord_y4(self):
        # print(self.__ui.coordY_4.sender())
        self._update_coord_value_from_spinbox(False, 3, self.__ui.coordY_4.value())

    def _update_coord_value_from_spinbox(self, is_x, index, value):
        print("ИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИ")
        if len(self.q_points) > index:
            if is_x:
                self.q_points[index].setX(value)
            else:
                self.q_points[index].setY(value)
            self.build_q_lines()
            self._draw_dots_and_lines()
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

    @staticmethod
    def exec(camera):
        # image = iio.read("E:/screen.png")
        # camera_id = camera
        camera_id = camera.data(CameraModel.IdRole)
        if not camera_id:
            return
        image = Video.get_image(camera_id, camera.data(CameraModel.GplModRole), camera.data(CameraModel.ServerRole))
        print('aaaa', image)
        camera_config = CameraConfig(image, camera_id)
        camera_config.show()
