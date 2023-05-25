from PyQt5 import QtCore, QtWidgets


class TrainImageNetView:
    __col_count = 6

    def __init__(self, table, model):
        self.__table = table
        self.__model = model

    def __create_label(self, text, pixmap=None):
        label = QtWidgets.QLabel(self.__table)
        if not pixmap:
            label.setText(text)
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setStyleSheet('margin: 5px;')
        else:
            label.setPixmap(pixmap)
        return label

    def __resize_table(self):
        self.__table.resizeColumnsToContents()
        self.__table.resizeRowsToContents()

    def __create_button(self, text, method=None):
        button = QtWidgets.QPushButton(self.__table)
        button.setText(text)
        button.setStyleSheet('margin:5px; height:15px; padding: 5px;')
        if method:
            button.clicked.connect(method)
        return button

    @staticmethod
    def __create_progress_bar():
        bar = QtWidgets.QProgressBar()
        bar.setStyleSheet('margin:5px; text-align: center;')
        return bar

    def refresh(self):
        self.__table.clear()
        self.__table.setRowCount(0)
        self.__table.setColumnCount(0)
        self.__table.horizontalHeader().setVisible(False)
        self.__table.verticalHeader().setVisible(False)
        # size
        row_count = len(self.__model)
        for camera in self.__model:
            row_count += len(camera.lines)
        self.__table.setColumnCount(self.__col_count)
        self.__table.setRowCount(row_count)

        header = self.__table.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)

        row_number = 0
        for camera in self.__model:
            self.__table.setSpan(row_number, 0, len(camera.lines) + 1, 1)
            self.__table.setCellWidget(row_number, 0, self.__create_label('', camera.pixmap))

            self.__table.setCellWidget(row_number, 1, self.__create_label(camera.title))
            self.__table.setCellWidget(row_number, 2,
                                       self.__create_button('Завантажити відео', camera.load_video))
            self.__table.setCellWidget(row_number, 3,
                                       self.__create_button('Запустити обробку зображень', camera.run_cv))
            label = self.__create_label(camera.status)
            self.__table.setCellWidget(row_number, 4, label)
            camera.add_observer('set_status', label.setText)
            camera.add_observer('set_status', lambda val: self.__resize_table())
            bar = self.__create_progress_bar()
            self.__table.setCellWidget(row_number, 5, bar)
            camera.add_observer('set_progress_value', bar.setValue)
            camera.add_observer('set_progress_max', bar.setMaximum)
            row_number += 1

            # lines
            for i in range(0, len(camera.lines)):
                line = camera.lines[i]
                self.__table.setCellWidget(row_number, 1, self.__create_label(line.title))
                self.__table.setCellWidget(row_number, 2, self.__create_button('Згенерувати датасет', line.generate_dataset))
                self.__table.setCellWidget(row_number, 3, self.__create_button('Почати навчання', line.train))
                label = self.__create_label(line.status)
                self.__table.setCellWidget(row_number, 4, label)
                line.add_observer('set_status', label.setText)
                line.add_observer('set_status', lambda val: self.__resize_table())
                bar = self.__create_progress_bar()
                line.add_observer('set_progress_value', bar.setValue)
                line.add_observer('set_progress_max', bar.setMaximum)
                self.__table.setCellWidget(row_number, 5, bar)
                row_number += 1

        # resize
        self.__table.resizeColumnsToContents()
        self.__table.resizeRowsToContents()
