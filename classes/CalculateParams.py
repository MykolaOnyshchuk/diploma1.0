from threading import Thread, Event
import time
import numpy as np
import os
import cv2
from skimage.util import img_as_float
from classes.Video import Video
from classes.Line import Line
from classes.ImageNet import ImageNet
from models.line.LineSql import LineSql
from models.line.LineModel import LineModel


class LineThread(Thread):
    def __init__(self, index, images, event_start, event_end):
        super().__init__()
        self.__index = index
        self.__images = images
        self.__event_start = event_start
        self.__event_end = event_end
        self.__line_id = self.__index.data(LineModel.IdRole)
        self.__coords = self.__index.data(LineModel.CoordsRole)
        self.__line = Line(self.__coords)
        self.__image_net = None

    def __load_image_net(self):
        if self.__image_net:
            return
        self.__image_net = ImageNet()
        weights_dir = os.path.join(os.getcwd(), 'weights')
        weights_file_name = os.path.join(weights_dir, 'image_net_{}.weights'.format(self.__line_id))
        print(weights_file_name, self.__line_id)
        if os.path.isfile(weights_file_name) or os.path.isfile('{}.index'.format(weights_file_name)):
            self.__image_net.load_weights(weights_file_name)
            print('loaded', self.__line_id)

    def run(self):
        while True:
            self.__event_start.wait()
            self.__event_start.clear()

            # generate x data for image net
            print('get train_x data from images', self.__line_id)
            size = len(self.__images)
            train_x = np.zeros((size, ImageNet.size_img, ImageNet.size_img, 3), dtype='float32')
            for i in range(0, size):
                train_x[i] = np.array(img_as_float(self.__line.get_image(self.__images[i])))

            if self.__line_id != 6:
                continue
            # predictions
            print('image net prediction', self.__line_id)
            self.__load_image_net()
            predictions = self.__image_net.predict(train_x)

            # calculate tlcr, intensity
            print('calculate tlcr, intensity from prediction', self.__line_id)
            size_predictions = len(predictions)
            tlcr = 0
            intensity = 0
            tlcr_arr = []
            for i in range(0, size_predictions):
                tlcr += self.__line.get_tlcr(predictions[i])
                tlcr_arr.append(self.__line.get_tlcr(predictions[i]))
            tlcr = tlcr / size_predictions

            # !!!!!! Допрацювати k + time_range
            intensity = self.get_intensity(predictions, tlcr_arr, 0.155, 60)

            print(tlcr, intensity, self.__line_id)

            self.__event_end.set()

    def get_intensity(self, output_images, tlcr_arr, k, time_range):
        sum_intensity = 0
        for i in range(1, len(output_images)):
            sum_intensity += (1 if tlcr_arr[i] > k > tlcr_arr[i - 1] else 0)
        intensity = sum_intensity / time_range
        return intensity


class CameraThread(Thread):
    def __init__(self, camera_id):
        super().__init__()
        self.__camera_id = camera_id
        self.__images = []
        self.__images_ready_event = Event()

        self.__line_threads = []
        self.__line_events = []
        self.__line_model = LineModel(LineSql.all_from_camera(self.__camera_id))
        self.__line_model.open()
        for i in range(0, self.__line_model.rowCount()):
            self.__line_events.append(Event())
            self.__line_threads.append(
                LineThread(self.__line_model.index(i, 0), self.__images, self.__images_ready_event,
                           self.__line_events[i]))

    def run(self):
        for thread in self.__line_threads:
            thread.daemon = True
            thread.start()
        while True:
            start_time = time.time()
            self.__images.clear()
            Video.fill_images('E:/diploma1.0/video/18/cam18stream_1580712551.mp4', self.__images)
            self.__images_ready_event.set()

            for event in self.__line_events:
                event.wait()
                event.clear()
            print('after all threads')
            print("all %s seconds" % (time.time() - start_time))
            time.sleep(50)



class CalculateParams:
    def __init__(self):
        pass

    def run(self):
        camera_thread = CameraThread(18)
        camera_thread.daemon = True
        camera_thread.start()
