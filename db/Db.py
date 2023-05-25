from PyQt5.QtSql import *


class Db:
    __db = QSqlDatabase.addDatabase("QSQLITE")
    __db.setDatabaseName("db/Traffic.db")
    __db.open()

    @staticmethod
    def commit():
        Db.__db.commit()

    @staticmethod
    def exec(sql):
        Db.__db.exec_(sql)

    @staticmethod
    def refresh_model(model):
        if not model:
            return
        model.refresh()
