from PySide6.QtSql import *
from db.Db import Db


class LineSql:
    @staticmethod
    def create_table():
        Db.exec(
            'CREATE TABLE line(id integer PRIMARY KEY AUTOINCREMENT, cameraId integer, coord1x integer, coord2x integer,'
            'coord3x integer, coord4x integer, coord1y integer, coord2y integer, coord3y integer, coord4y integer);')

    @staticmethod
    def delete_table():
        Db.exec('DROP TABLE line')

    @staticmethod
    def all_from_camera(camera_id):
        return 'SELECT * FROM line WHERE cameraId = {}'.format(camera_id)

    @staticmethod
    def delete(line_id, model=None):
        print(line_id)
        if not line_id:
            return
        sql = QSqlQuery()
        sql.prepare("DELETE FROM line WHERE id = ?")
        sql.addBindValue(line_id)
        sql.exec_()
        Db.commit()
        Db.refresh_model(model)

    @staticmethod
    def check_coords(list_coords):
        for i in list_coords:
            x, y = i
            if (x == 0) or (y == 0):
                return False
        return True

    @staticmethod
    def get_list_coords(record):
        x1 = record.field('coord1x').value()
        x2 = record.field('coord2x').value()
        x3 = record.field('coord3x').value()
        x4 = record.field('coord4x').value()
        y1 = record.field('coord1y').value()
        y2 = record.field('coord2y').value()
        y3 = record.field('coord3y').value()
        y4 = record.field('coord4y').value()
        list_coords = [[x1, y1],
                       [x2, y2],
                       [x3, y3],
                       [x4, y4]]
        return list_coords

    @staticmethod
    def get_id(record):
        return record.value('id')

    @staticmethod
    def add_line(camera_id, list_coords, model=None):
        if not LineSql.check_coords(list_coords):
            return
        coord_x, coord_y = list_coords[0]
        coord2_x, coord2_y = list_coords[1]
        coord3_x, coord3_y = list_coords[2]
        coord4_x, coord4_y = list_coords[3]
        sql = QSqlQuery()
        sql.prepare("INSERT INTO line(cameraId, coord1x, coord2x, coord3x, coord4x, coord1y, coord2y, coord3y, coord4y) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)")
        sql.addBindValue(camera_id)
        sql.addBindValue(coord_x)
        sql.addBindValue(coord2_x)
        sql.addBindValue(coord3_x)
        sql.addBindValue(coord4_x)
        sql.addBindValue(coord_y)
        sql.addBindValue(coord2_y)
        sql.addBindValue(coord3_y)
        sql.addBindValue(coord4_y)
        sql.exec_()
        # print(sql.lastError())
        Db.commit()
        Db.refresh_model(model)
