from threading import Thread
import time
import os
import cv2
import numpy as np
from PyQt5.QtCore import QThread, QObject
from skimage.util import img_as_float
from classes.Video import Video
from classes.ImageNet import ImageNet
from classes.Line import Line
from PyQt5 import QtCore


class RunImageNetThread(QObject):
    finished = QtCore.pyqtSignal()

    def __init__(self, video, coords):
        super().__init__()
        self.__video = video
        self.__coords = coords
        self.__tlcr_arr = []
        self.__intensity = 0

    def run(self):
        print('ppc')
        images = []
        Video.fill_images(self.__video, images)

        line = Line(self.__coords)

        print('images', len(images))
        images = images[::5]
        size = len(images)

        train_x = np.zeros((size, ImageNet.size_img, ImageNet.size_img, 3), dtype='float32')
        for i in range(0, len(images)):
            train_x[i] = np.array(img_as_float(line.get_image(images[i])))

        image_net = ImageNet()
        weights_dir = os.path.join(os.getcwd(), 'weights')
        weights_file_name = os.path.join(weights_dir, 'image_net_{}.weights'.format(6))

        # check net
        image_net.init()
        image_net.load_weights(weights_file_name)

        print(train_x)
        print(train_x.size)
        predictions = image_net.predict(train_x)
        print('After prediction')

        for i in range(0, len(predictions)):
            image = (predictions[i].squeeze() * 255)
            cv2.imwrite('D:/MytestNet/{}.jpg'.format(i), image)
            cv2.imwrite('D:/MytestNet/{}_orig.jpg'.format(i), line.get_image(images[i]))
            print(i)

        print('calculate tlcr, intensity from prediction')
        size_predictions = len(predictions)
        tlcr = 0
        tlcr_arr = []
        for i in range(0, size_predictions):
            tlcr += line.get_tlcr(predictions[i])
            tlcr_arr.append(line.get_tlcr(predictions[i]))
        tlcr = tlcr / size_predictions

        # !!!!!! Допрацювати k + time_range
        intensity = self.get_intensity(predictions, tlcr_arr, 0.155, 1)

        # f = open("D:/Chrome Downloads/mock_tlcr_2.txt", "a")
        # for i in range(0, len(tlcr_arr)):
        #     f.write(str(tlcr_arr[i]) + ";")
        # f.write("\n" + str(intensity))
        # f.close()
        self.__tlcr_arr = tlcr_arr
        self.__intensity = intensity
        print("--------------------------------------------------")
        print(f"Analysis for {self.__video}")
        print(tlcr, intensity)
        self.finished.emit()

    def get_intensity(self, output_images, tlcr_arr, k, time_range):
        sum_intensity = 0
        for i in range(1, len(output_images)):
            sum_intensity += (1 if tlcr_arr[i] > k > tlcr_arr[i - 1] else 0)
        intensity = sum_intensity / time_range
        return intensity

    def get_tlcr_and_intensity(self):
        return self.__tlcr_arr, self.__intensity
