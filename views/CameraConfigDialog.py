# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\projects\python\network\src\views\CameraConfigDialog.ui',
# licensing of 'D:\projects\python\network\src\views\CameraConfigDialog.ui' applies.
#
# Created: Fri Jul  3 08:53:00 2020
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QColor


class Ui_CameraConfigDialog(object):
    def setupUi(self, CameraConfigDialog):
        CameraConfigDialog.setObjectName("CameraConfigDialog")
        CameraConfigDialog.resize(885, 478)
        self.buttonBox = QtWidgets.QDialogButtonBox(CameraConfigDialog)
        self.buttonBox.setGeometry(QtCore.QRect(500, 420, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(CameraConfigDialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 640, 400))
        self.label.setMinimumSize(QtCore.QSize(640, 400))
        self.label.setMaximumSize(QtCore.QSize(640, 400))
        self.label.setBaseSize(QtCore.QSize(640, 400))
        self.label.setObjectName("label")
        # self.label.mousePressEvent = self.get_pixel
        self.verticalLayoutWidget = QtWidgets.QWidget(CameraConfigDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(660, 10, 211, 211))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelCoord = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelCoord.sizePolicy().hasHeightForWidth())
        self.labelCoord.setSizePolicy(sizePolicy)
        self.labelCoord.setMinimumSize(QtCore.QSize(0, 0))
        self.labelCoord.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.labelCoord.setScaledContents(False)
        self.labelCoord.setWordWrap(False)
        self.labelCoord.setObjectName("labelCoord")
        self.horizontalLayout.addWidget(self.labelCoord)
        self.coordX = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.coordX.setMinimum(0)
        self.coordX.setMaximum(1000)
        self.coordX.setProperty("value", 0)
        self.coordX.setObjectName("coordX")
        self.horizontalLayout.addWidget(self.coordX)
        self.coordY = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.coordY.setObjectName("coordY")
        self.horizontalLayout.addWidget(self.coordY)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.coordX_2 = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.coordX_2.setObjectName("coordX_2")
        self.horizontalLayout_2.addWidget(self.coordX_2)
        self.coordY_2 = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.coordY_2.setObjectName("coordY_2")
        self.horizontalLayout_2.addWidget(self.coordY_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.coordX_3 = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.coordX_3.setObjectName("coordX_3")
        self.horizontalLayout_3.addWidget(self.coordX_3)
        self.coordY_3 = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.coordY_3.setObjectName("coordY_3")
        self.horizontalLayout_3.addWidget(self.coordY_3)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_4.addWidget(self.label_5)
        self.coordX_4 = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.coordX_4.setObjectName("coordX_4")
        self.horizontalLayout_4.addWidget(self.coordX_4)
        self.coordY_4 = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.coordY_4.setObjectName("coordY_4")
        self.horizontalLayout_4.addWidget(self.coordY_4)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.lines = QtWidgets.QListView(CameraConfigDialog)
        self.lines.setGeometry(QtCore.QRect(660, 280, 211, 131))
        self.lines.setObjectName("lines")
        self.horizontalLayoutWidget_5 = QtWidgets.QWidget(CameraConfigDialog)
        self.horizontalLayoutWidget_5.setGeometry(QtCore.QRect(660, 230, 211, 41))
        self.horizontalLayoutWidget_5.setObjectName("horizontalLayoutWidget_5")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_5)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.add_line = QtWidgets.QToolButton(self.horizontalLayoutWidget_5)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/buttons/img/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_line.setIcon(icon)
        self.add_line.setIconSize(QtCore.QSize(32, 32))
        self.add_line.setObjectName("add_line")
        self.horizontalLayout_5.addWidget(self.add_line)
        self.delete_line = QtWidgets.QToolButton(self.horizontalLayoutWidget_5)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/buttons/img/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.delete_line.setIcon(icon1)
        self.delete_line.setIconSize(QtCore.QSize(32, 32))
        self.delete_line.setObjectName("delete_line")
        self.horizontalLayout_5.addWidget(self.delete_line)
        self.show_lines = QtWidgets.QCheckBox(CameraConfigDialog)
        self.show_lines.setGeometry(QtCore.QRect(10, 430, 121, 17))
        self.show_lines.setObjectName("show_lines")

        self.retranslateUi(CameraConfigDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), CameraConfigDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), CameraConfigDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CameraConfigDialog)

    def retranslateUi(self, CameraConfigDialog):
        CameraConfigDialog.setWindowTitle(QtWidgets.QApplication.translate("CameraConfigDialog", "Dialog", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("CameraConfigDialog", "TextLabel", None, -1))
        self.labelCoord.setText(QtWidgets.QApplication.translate("CameraConfigDialog", "1 точка", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("CameraConfigDialog", "2 точка", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("CameraConfigDialog", "3 точка", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("CameraConfigDialog", "4 точка", None, -1))
        self.add_line.setText(QtWidgets.QApplication.translate("CameraConfigDialog", "...", None, -1))
        self.delete_line.setText(QtWidgets.QApplication.translate("CameraConfigDialog", "...", None, -1))
        self.show_lines.setText(QtWidgets.QApplication.translate("CameraConfigDialog", "Показувати всі лінії", None, -1))

    # def get_pixel(self, event):
    #     x = event.pos().x()
    #     y = event.pos().y()
    #     c = self.qimg.pixel(x, y)  # color code (integer): 3235912
    #     # depending on what kind of value you like (arbitary examples)
    #     c_qobj = QColor(c)  # color object
    #     c_rgb = QColor(c).getRgb()  # 8bit RGBA: (255, 23, 0, 255)
    #     c_rgbf = QColor(c).getRgbf()  # RGBA float: (1.0, 0.3123, 0.0, 1.0)
    #     print(x + ' and ' + y)
    #     return x, y, c_rgb

import views.images

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CameraConfigDialog = QtWidgets.QDialog()
    ui = Ui_CameraConfigDialog()
    ui.setupUi(CameraConfigDialog)
    CameraConfigDialog.show()
    sys.exit(app.exec_())

