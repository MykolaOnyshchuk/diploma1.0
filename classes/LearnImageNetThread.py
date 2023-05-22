from threading import Thread
import time
import os
import cv2
import numpy as np
from skimage.util import img_as_float
from classes.Video import Video
from classes.ImageNet import ImageNet
from models.Observable import Observable, event


class LearnImageNetThreadSignals(Observable):
    update_progress = None
    update_status = None
    update_progress_max = None
    finished = None

    @event
    def set_update_progress(self, value):
        self.update_progress = value

    @event
    def set_update_status(self, value):
        self.update_status = value

    @event
    def set_update_progress_max(self, value):
        self.update_progress_max = value

    @event
    def set_finished(self, value):
        self.finished = value


class LearnImageNetThread(Thread):
    __max_files = 500
    __epochs = 5

    def __init__(self, camera_id, id):
        super().__init__()
        self.__camera_id = camera_id
        self.__id = id
        self.signals = LearnImageNetThreadSignals()

    def run(self):
        # dirs
        camera_dir = os.path.join(Video.video_folder, str(self.__camera_id))
        ds_dir = os.path.join(camera_dir, str(self.__id))
        orig_ds_dir = os.path.join(ds_dir, Video.orig_folder)
        res_ds_dir = os.path.join(ds_dir, Video.res_folder)

        # files
        list_files = os.listdir(res_ds_dir)
        len_files = len(list_files)
        self.signals.set_update_progress_max(len_files + len_files * self.__epochs)
        print(len_files * 2)
        train = []
        for i in range(0, len_files, self.__max_files):
            start = i
            end = i + self.__max_files if len_files > i + self.__max_files else len_files
            size = end - start
            print(start, end, size)
            train_x = np.zeros((size, ImageNet.size_img, ImageNet.size_img, 3), dtype='float32')
            train_y = np.zeros((size, ImageNet.size_img, ImageNet.size_img, 1), dtype='float32')
            j = 0
            for file in list_files[start:end]:
                orig = cv2.imread(os.path.join(orig_ds_dir, file))
                res = cv2.imread(os.path.join(res_ds_dir, file), 0)
                train_x[j] = np.array(img_as_float(orig))
                train_y[j] = np.asarray(img_as_float(res))[..., None].astype(dtype='float32', copy=False)
                j += 1
            train.append((train_x, train_y))
            self.signals.set_update_progress(end)

        # net
        image_net = ImageNet()
        len_train = len(train)
        for i in range(self.__epochs):
            for j in range(0, len_train):
                train_x, train_y = train[j]
                image_net.train(train_x, train_y, 1)
            self.signals.set_update_progress(len_files + (i + 1) * len_files)

        # save weights
        weights_dir = os.path.join(os.getcwd(), 'weights')
        weights_file_name = os.path.join(weights_dir, 'image_net_{}.weights'.format(self.__id))

        image_net.save_weights(weights_file_name)
        print('learn ready')

        # check net
        image_net.load_weights(weights_file_name)
        train_x, train_y = train[0]
        predictions = image_net.predict(train_x)

        i = 0
        for image in predictions:
            image = (image.squeeze() * 255)
            cv2.imwrite('D:/intensity/MytestNet/{}.jpg'.format(i), image)
            i += 1

        print('yeah')

        self.signals.set_finished()
