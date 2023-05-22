from PySide6.QtSql import *
from db.Db import Db


class CameraSql:
    @staticmethod
    def all():
        return 'SELECT * FROM CAMERA'

    @staticmethod
    def selected():
        return 'SELECT * FROM camera INNER JOIN selectedCameras ON camera.id = selectedCameras.cameraId'

    @staticmethod
    def select_camera(id, model=None):
        if not id:
            return
        sql = QSqlQuery()
        sql.prepare("INSERT INTO selectedCameras(cameraId) VALUES(?)")
        sql.addBindValue(id)
        sql.exec_()
        Db.commit()
        Db.refresh_model(model)

    @staticmethod
    def delete_selected_camera(id, model=None):
        if not id:
            return
        sql = QSqlQuery()
        sql.prepare("DELETE FROM selectedCameras WHERE cameraId = ?")
        sql.addBindValue(id)
        sql.exec_()
        Db.commit()
        Db.refresh_model(model)

    @staticmethod
    def get_id(record):
        return record.field("id").value()

    @staticmethod
    def get_gplmod(record):
        return record.field("gplmod").value()

    @staticmethod
    def get_server(record):
        return record.field("url").value()

    @staticmethod
    def get_title(record):
        return record.field("title").value()