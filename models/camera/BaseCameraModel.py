from PyQt5.QtSql import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt


class BaseCameraModel(QSqlQueryModel):
    _sql = ""
    IdRole = Qt.UserRole + 1
    TextRole = Qt.UserRole + 2
    GplModRole = Qt.UserRole + 3
    ServerRole = Qt.UserRole + 4
    ImageRole = Qt.UserRole + 5

    def __init__(self, *args, **kwargs):
        super(BaseCameraModel, self).__init__(*args, **kwargs)

    def flags(self, index:QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self.record(index.row()).value(BaseCameraModel.TextRole - Qt.UserRole - 1)

        if role > Qt.UserRole:
            return self.record(index.row()).value(role - Qt.UserRole - 1)
        return super().data(index, role)

    def refresh(self):
        self.setQuery(self._sql)
        self.layoutChanged.emit()

    def open(self):
        self.refresh()

    def test(self):
        for i in range(self.rowCount()):
            print(self.record(i).value("id"))
