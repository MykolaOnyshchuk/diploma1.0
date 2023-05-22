from threading import Thread
import time
import os
import cv2
import numpy as np
from skimage.util import img_as_float
from classes.Video import Video
from classes.ImageNet import ImageNet
from classes.Line import Line
from PySide6 import QtCore


class RunImageNetThread(Thread):

    def __init__(self, video, coords):
        super().__init__()
        self.__video = video
        self.__coords = coords

    def run(self):
        print('ppc')
        images = []
        Video.fill_images(self.__video, images)
        line = Line(self.__coords)

        print(len(images))
        size = len(images)

        train_x = np.zeros((size, ImageNet.size_img, ImageNet.size_img, 3), dtype='float32')
        for i in range(0, len(images)):
            train_x[i] = np.array(img_as_float(line.get_image(images[i])))

        image_net = ImageNet()
        weights_dir = os.path.join(os.getcwd(), 'weights')
        weights_file_name = os.path.join(weights_dir, 'image_net_{}.weights'.format(6))

        # check net
        image_net.load_weights(weights_file_name)
        predictions = image_net.predict(train_x)

        i = 0
        for image in predictions:
            image = (image.squeeze() * 255)
            cv2.imwrite('D:/intensity/MytestNet/{}.jpg'.format(i), image)
            i += 1

        print('yeah')
