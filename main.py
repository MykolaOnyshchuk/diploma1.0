import sys
from PyQt5 import QtWidgets
from PyQt5.QtSql import *
# import qdarktheme
# import qt_material
from controllers.MainController import MainController
from db.Db import Db


class Application:
    mainController = None
    __app = QtWidgets.QApplication

    def __init__(self):
        self.__app = QtWidgets.QApplication(sys.argv)
        # qdarktheme.setup_theme()
        # qt_material.apply_stylesheet(self.__app, theme='dark_cyan.xml')

        self.mainController = MainController()

    def run(self):
        self.mainController.run()
        sys.exit(self.__app.exec_())


if __name__ == "__main__":
    app = Application()
    app.run()
