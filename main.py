import sys
from PySide6 import QtWidgets
from PySide6.QtSql import *
from controllers.MainController import MainController
from db.Db import Db


class Application:
    mainController = None
    __app = QtWidgets.QApplication

    def __init__(self):
        self.__app = QtWidgets.QApplication(sys.argv)
        self.mainController = MainController()

    def run(self):
        self.mainController.run()
        sys.exit(self.__app.exec_())


if __name__ == "__main__":
    app = Application()
    app.run()
