from PyQt5.QtSql import *
from datetime import datetime
import numpy as np


class Database:
    # __db = QSqlDatabase.addDatabase("QSQLITE")
    # __db.setDatabaseName("Traffic.db")
    # __db.open()

    @staticmethod
    def commit():
        Database.__db.commit()

    @staticmethod
    def create_selected_cameras():
        sql = "CREATE TABLE selectedCameras(cameraId integer PRIMARY KEY);"
        Database.__db.exec_(sql)

    @staticmethod
    def create_stat_cameras():
        sql = "CREATE TABLE statCameras(cameraId integer, line integer, direction integer, tsp integer, value REAL);"
        Database.__db.exec_(sql)

    @staticmethod
    def get_list_cameras():
        return "SELECT * FROM camera"

    @staticmethod
    def get_list_selected_cameras():
        sql = "SELECT * FROM camera INNER JOIN selectedCameras ON camera.id = selectedCameras.cameraId"
        return sql

    @staticmethod
    def get_stat_cameras(line=1):
        sql = "SELECT * FROM statCameras WHERE datetime(tsp, 'unixepoch', 'localtime') between '2020-01-31 00:00:00' and '2020-01-31 23:59:59' and line = {}".format(line)
        return sql
    # datetime(tsp, 'unixepoch', 'localtime') between '2020-01-30 00:00:00' and '2020-01-30 23:59:59' and

    @staticmethod
    def get_stat_cameras_for_net():
        sql = """SELECT sc.tsp tsp, datetime(sc.tsp, 'unixepoch', 'localtime') dt,
                                (select ifnull(sum(value)/count(value), 1.1)
                from statCameras
                where line = sc.line and tsp between sc.tsp - 600 and sc.tsp) valfuture,
                (select ifnull(sum(value)/count(value), 1.1)
                from statCameras
                where line = sc.line and tsp between sc.tsp - (604800 + 600) and sc.tsp - 604800) valweek,
                (select ifnull(sum(value)/count(value), 1.1)
                from statCameras
                where line = sc.line and tsp between sc.tsp - (86400 + 600) and sc.tsp - 86400) valyest,
                (select ifnull(sum(value)/count(value), 1.1)
                from statCameras
                where line = sc.line and tsp between sc.tsp - (600 + 600) and sc.tsp - 600) valprev,
                (select ifnull(sum(value)/count(value), 1.1)
                from statCameras
                where line = sc.line and tsp between sc.tsp - (300 + 600) and sc.tsp -  300) val
            FROM statCameras sc
            WHERE sc.line = 5 and sc.tsp >= 1580439606 
            and (datetime(sc.tsp, 'unixepoch', 'localtime') between '2020-01-31 08:00:00' and '2020-01-31 21:00:00'
                or datetime(sc.tsp, 'unixepoch', 'localtime') between '2020-02-01 08:00:00' and '2020-02-01 21:00:00'
                or datetime(sc.tsp, 'unixepoch', 'localtime') between '2020-02-02 08:00:00' and '2020-02-02 21:00:00'
                or datetime(sc.tsp, 'unixepoch', 'localtime') between '2020-02-03 08:00:00' and '2020-02-03 21:00:00'
                or datetime(sc.tsp, 'unixepoch', 'localtime') between '2020-02-04 08:00:00' and '2020-02-04 21:00:00'
                or datetime(sc.tsp, 'unixepoch', 'localtime') between '2020-02-05 08:00:00' and '2020-02-05 21:00:00'
                )
          """
        # and datetime(sc.tsp, 'unixepoch', 'localtime') not between  '2020-02-03 00:00:00' and '2020-02-03 23:59:00'
        # time(sc2.tsp, 'unixepoch', 'localtime') between '06:00:00' and '22:00:00'
        # sc.tsp >= 1580439606 and sc.tsp < 1580649411
        query = QSqlQuery(sql)
        x, y = [], []
        x1, x2, x3, x4 = [], [], [], []
        while query.next():
            valweek = query.value("valweek")
            valyest = query.value("valyest")
            valprev = query.value("valprev")
            val = query.value("val")
            valfuture = query.value("valfuture")
            x1.append(valweek)
            x2.append(valyest)
            x3.append(valprev)
            x4.append(val)
            x.append([[valweek], [valyest], [valprev], [val]])
            y.append(valfuture)
        print(len(x), len(y))
        y = np.array(y, dtype=float)
        x = np.array(x, dtype=float)
        return x, y

    @staticmethod
    def get_stat_cameras_for_net2():
        sql = """SELECT sc.tsp tsp, datetime(sc.tsp, 'unixepoch', 'localtime') dt,
                                (select ifnull(sum(value)/count(value), 1.1)
                from statCameras
                where line = sc.line and tsp between sc.tsp - 600 and sc.tsp) valfuture,
                (select ifnull(sum(value)/count(value), 1.1)
                from statCameras
                where line = sc.line and tsp between sc.tsp - (604800 + 600) and sc.tsp - 604800) valweek,
                (select ifnull(sum(value)/count(value), 1.1)
                from statCameras
                where line = sc.line and tsp between sc.tsp - (86400 + 600) and sc.tsp - 86400) valyest,
                (select ifnull(sum(value)/count(value), 1.1)
                from statCameras
                where line = sc.line and tsp between sc.tsp - (600 + 600) and sc.tsp - 600) valprev,
                (select ifnull(sum(value)/count(value), 1.1)
                from statCameras
                where line = sc.line and tsp between sc.tsp - (300 + 600) and sc.tsp -  300) val
            FROM statCameras sc
            WHERE sc.line = 5 
           and datetime(sc.tsp, 'unixepoch', 'localtime') between '2020-02-05 08:00:00' and '2020-02-05 21:00:00'
           and valprev <> 1.1 and val <> 1.1 and valyest <> 1.1 and valweek <> 1.1
         
            """
        # and sc.tsp >= 1580439606
        # '2020-02-03 00:00:00' and '2020-02-03 23:59:00'
        # time(sc2.tsp, 'unixepoch', 'localtime') between '06:00:00' and '22:00:00'
        # sc.tsp >= 1580439606 and sc.tsp < 1580649411
        query = QSqlQuery(sql)
        x, y = [], []
        tspx = []
        test = -1
        while query.next():
            test += 1
            if test % 15 != 0:
                continue


            valweek = query.value("valweek")
            valyest = query.value("valyest")
            valprev = query.value("valprev")
            val = query.value("val")
            valfuture = query.value("valfuture")
            x.append([[valweek], [valyest], [valprev], [val]])
            y.append(valfuture)
            tspx.append(datetime.fromtimestamp(query.value("tsp")))
        print(len(x), len(y))
        y = np.array(y, dtype=float)
        x = np.array(x, dtype=float)
        return x, y, tspx

    @staticmethod
    def print_stat_cameras():
        query = Database.get_stat_cameras_data()
        while query.next():
            tlcr = query.value("value")
            tsp = query.value("tsp")
            line = query.value("line")
            print(line, datetime.fromtimestamp(tsp).time(), tlcr)

    @staticmethod
    def get_stat_cameras_data(line):
        query = QSqlQuery(Database.get_stat_cameras(line))
        return query

    @staticmethod
    def get_stat_cameras_data_compare(line):
        sql = """SELECT * FROM statCameras WHERE tsp in (1580103739, 1580104353, 1580104967, 1580105582,
        1580106197, 1580106811, 1580107425, 1580107978, 1580108530, 1580109144, 1580109759, 1580110373, 1580110987, 1580111601,
        1580112215, 1580112830, 1580113444, 1580114058, 1580114672, 1580115288, 1580115902, 1580116517, 1580117131, 1580117745,
        1580118359, 1580118973, 1580119587, 1580120201, 1580120815, 1580121429)
            and line = 5""".format(line)
        query = QSqlQuery(sql)
        return query

    @staticmethod
    def insert_stat(camera_id, line, direction, tsp, value):
        sql = QSqlQuery()
        sql.prepare("INSERT INTO statCameras(cameraId, line, direction, tsp, value) VALUES(?, ?, ?, ?, ?)")
        sql.addBindValue(camera_id)
        sql.addBindValue(line)
        sql.addBindValue(direction)
        sql.addBindValue(tsp)
        sql.addBindValue(value)
        sql.exec_()
        Database.__db.commit()

    @staticmethod
    def select_camera(cameraId):
        sql = QSqlQuery()
        sql.prepare("INSERT INTO selectedCameras(cameraId) VALUES(?)")
        sql.addBindValue(cameraId)
        sql.exec_()
        Database.__db.commit()

    @staticmethod
    def delete_selected_camera(cameraId):
        sql = QSqlQuery()
        sql.prepare("DELETE FROM selectedCameras WHERE cameraId = ?")
        sql.addBindValue(cameraId)
        sql.exec_()
        Database.__db.commit()

    @staticmethod
    def delete_stat():
        sql = QSqlQuery()
        sql.prepare("DELETE FROM statCameras")
        sql.exec_()
        Database.__db.commit()



