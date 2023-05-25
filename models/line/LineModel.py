from PyQt5.QtSql import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt


class LineModel(QSqlQueryModel):
    _sql = ""
    IdRole = Qt.UserRole + 1
    CameraRole = Qt.UserRole + 2
    CoordXRole = Qt.UserRole + 3
    Coord2XRole = Qt.UserRole + 4
    Coord3XRole = Qt.UserRole + 5
    Coord4XRole = Qt.UserRole + 6
    CoordYRole = Qt.UserRole + 7
    Coord2YRole = Qt.UserRole + 8
    Coord3YRole = Qt.UserRole + 9
    Coord4YRole = Qt.UserRole + 10
    CoordsRole = Qt.UserRole + 11

    def __init__(self, sql='', *args, **kwargs):
        super(LineModel, self).__init__(*args, **kwargs)
        self.__sql = sql

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return '({}x{}),({}x{}), ({}x{}), ({}x{})'.format(self.data(index, LineModel.CoordXRole),
                                                              self.data(index, LineModel.CoordYRole),
                                                              self.data(index, LineModel.Coord2XRole),
                                                              self.data(index, LineModel.Coord2YRole),
                                                              self.data(index, LineModel.Coord3XRole),
                                                              self.data(index, LineModel.Coord3YRole),
                                                              self.data(index, LineModel.Coord4XRole),
                                                              self.data(index, LineModel.Coord4YRole))
            # return self.record(index.row()).value(LineModel.TextRole - Qt.UserRole - 1)
        if role == LineModel.CoordsRole:
            return [[self.data(index, LineModel.CoordXRole), self.data(index, LineModel.CoordYRole)],
                       [self.data(index, LineModel.Coord2XRole), self.data(index, LineModel.Coord2YRole)],
                       [self.data(index, LineModel.Coord3XRole), self.data(index, LineModel.Coord3YRole)],
                       [self.data(index, LineModel.Coord4XRole), self.data(index, LineModel.Coord4YRole)]]

        if role > Qt.UserRole:
            return self.record(index.row()).value(role - Qt.UserRole - 1)
        return super().data(index, role)

    def refresh(self):
        self.setQuery(self.__sql)
        self.layoutChanged.emit()

    def open(self):
        self.refresh()
