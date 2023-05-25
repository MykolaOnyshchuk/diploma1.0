from models.camera.BaseCameraModel import BaseCameraModel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QPixmapCache
import requests


class CameraModel(BaseCameraModel):
    def __init__(self, sql='', *args, **kwargs):
        super(CameraModel, self).__init__(*args, **kwargs)
        self._sql = sql

    def data(self, index, role):
        if role == Qt.DecorationRole:
            image_url = self.record(index.row()).value(CameraModel.ImageRole - Qt.UserRole - 1)
            pm = QPixmap()
            # if not QPixmapCache.find(image_url, pm):
            #     pm.loadFromData(requests.get(image_url).content)
            #     pm = pm.scaledToHeight(50)
            #     QPixmapCache.insert(image_url, pm)
            return pm
        return super().data(index, role)

    def delete(self, index):
        id = index.data(CameraModel.IdRole)
        if id is not None:
            # Database.delete_selected_camera(id)
            self.refresh()
