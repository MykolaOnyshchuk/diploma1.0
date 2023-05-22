from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6 import QtCore, QtWidgets, QtGui
import math
import numpy as np
import matplotlib.dates as md
from datetime import datetime
from PySide6.QtSql import *
from enum import Enum
from collections import namedtuple
from models.line.LineModel import LineModel
from models.line.LineSql import LineSql

_ = namedtuple('PlotTimeEnumValue', ['number', 'count_data', 'moving_step', 'date_format', 'title'])


class PlotTimeEnum(Enum):
    ten_mins = _(0, 10, 0, md.DateFormatter('%H:%M'), 'За 10 Хвилин')
    hour = _(0, 60, 10, md.DateFormatter('%H:%M'), 'За годину')
    day = _(1, 60 * 24, 60, md.DateFormatter('%H:%M'), 'За 24 години')
    week = _(1, 60 * 24 * 7, 60, md.DateFormatter('%d.%m'), 'За тиждень')


class DefaultPlot(QtWidgets.QWidget):
    __time_enum = PlotTimeEnum.hour
    __time_enum_max = PlotTimeEnum.week
    __buttons = [PlotTimeEnum.ten_mins, PlotTimeEnum.hour, PlotTimeEnum.day, PlotTimeEnum.week]
    __timer_update_time = 30000
    __colors = ['#5B9BD5', '#ED7D31', '#A5A5A5', '#FFC000']
    __table_labels = ['Останнє значення TLCR', 'Останнє значення Інтенсивності']

    def __init__(self, camera_id, title='', width=5, height=4, dpi=100, parent=None):
        super(DefaultPlot, self).__init__()
        self.__camera_id = camera_id
        self.__title = title
        self.__load_data()

        # graph
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.__inner_canvas = FigureCanvasQTAgg(fig)
        self.axes = fig.add_subplot(111)
        self.axes.grid(True)
        self.axes.set_title(self.__title)
        fig.autofmt_xdate()

        # table
        self.__model = QtGui.QStandardItemModel()
        self.__table = QtWidgets.QTableView()
        self.__table.setModel(self.__model)

        # buttons
        buttons = QtWidgets.QHBoxLayout()
        for button in self.__buttons:
            self.__add_button_from_enum(button, buttons)
        widget_buttons = QtWidgets.QWidget(self)
        widget_buttons.setLayout(buttons)

        # main layout
        self.__inner_canvas.setMinimumHeight(400)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.__table)
        layout.addWidget(widget_buttons)
        layout.addWidget(self.__inner_canvas)
        self.setLayout(layout)

        # timer
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.__update)
        timer.start(self.__timer_update_time)

        self.__draw_data()
        self.__update_data()

    def __add_button_from_enum(self, value, layout):
        button = QtWidgets.QPushButton()
        button.setText(value.value.title)
        button.clicked.connect(lambda: self.__set_time_enum(value))
        layout.addWidget(button)

    def __set_time_enum(self, value):
        self.__time_enum = value
        self.__draw_data()

    def __prepare_data(self, line):
        x, y, last_tsp = line
        step = self.__time_enum.value.moving_step
        size = len(x)
        start = size - self.__time_enum.value.count_data
        x = x[start:size]
        y = y[start:size]
        if step != 0:
            y = DefaultPlot.moving_average(y, step)
            del x[0:step - 1]
        return x, y

    def __draw_data(self):
        count_lines = len(self.__lines_data)
        if count_lines == 0:
            return

        self.axes.cla()
        self.axes.set_title(self.__title)
        self.axes.grid(True)
        self.axes.xaxis.set_major_formatter(self.__time_enum.value.date_format)

        for i in range(0, count_lines):
            line = self.__lines_data[i]
            x, y = self.__prepare_data(line)
            if len(x) == 0:
                continue
            self.axes.plot(x, y, linestyle='solid', color=self.__colors[i], label=str(i + 1))

        self.axes.legend()
        self.__inner_canvas.draw()

    @staticmethod
    def moving_average(a, n=3):
        ret = np.cumsum(a, dtype=float)
        ret[n:] = ret[n:] - ret[:-n]
        return ret[n - 1:] / n

    @staticmethod
    def __load_data_sql(sql):
        model = QSqlQueryModel()
        model.setQuery(sql)
        if model.rowCount() == 0:
            return

        while model.canFetchMore():
            model.fetchMore()

        x, y, last_tsp = [], [], 0
        for i in range(0, model.rowCount()):
            tlcr = model.record(i).field("value").value()
            tsp = model.record(i).field("tsp").value()
            tm = datetime.fromtimestamp(tsp)
            y.append(tlcr)
            x.append(tm)
            last_tsp = tsp

        return x, y, last_tsp

    def __load_data(self):
        self.__lines_data = []

        id_to_number = {
            6: 4,
            8: 5,
            9: 2
        }

        lines = LineModel(LineSql.all_from_camera(self.__camera_id))
        lines.open()
        lines_count = lines.rowCount()
        for i in range(0, lines_count):
            line_id = LineSql.get_id(lines.record(i))

            sql = 'SELECT * FROM statCameras WHERE cameraId = {} and line = {} ORDER BY tsp DESC LIMIT {}'.format(self.__camera_id,
                                                                                                id_to_number[line_id],
                                                                                                self.__time_enum_max.value.count_data)
            print(sql)
            line_data = DefaultPlot.__load_data_sql(sql)
            if line_data:
                self.__lines_data.append(line_data)

        # sql = 'SELECT * FROM statCameras WHERE cameraId = {} and line = 5'.format(self.__camera_id)
        # line = DefaultPlot.__load_data_sql(sql)
        # if line:
        #     self.__lines_data.append(line)
        #
        # sql = 'SELECT * FROM statCameras WHERE cameraId = {} and line = 4'.format(self.__camera_id)
        # line = DefaultPlot.__load_data_sql(sql)
        # if line:
        #     self.__lines_data.append(line)
        #
        # sql = 'SELECT * FROM statCameras WHERE cameraId = {} and line = 2'.format(self.__camera_id)
        # line = DefaultPlot.__load_data_sql(sql)
        # if line:
        #     self.__lines_data.append(line)
        #
        # sql = 'SELECT * FROM statCameras WHERE cameraId = {} and line = 1'.format(self.__camera_id)
        # line = DefaultPlot.__load_data_sql(sql)
        # if line:
        #     self.__lines_data.append(line)

    def __update_data(self):
        count_lines = len(self.__lines_data)
        if count_lines == 0:
            self.setVisible(False)
            return
        self.setVisible(True)

        # table
        self.__model.setColumnCount(len(self.__lines_data))
        self.__model.setVerticalHeaderLabels(self.__table_labels)
        for i in range(0, count_lines):
            x, y, last_tsp = self.__lines_data[i]
            self.__model.setData(self.__model.index(0, i), y[-1])
        # self.__table.resizeColumnsToContents()
        self.__table.resizeRowsToContents()

    def __update(self):
        print('update')
        self.__load_data()
        self.__update_data()
        self.__draw_data()
