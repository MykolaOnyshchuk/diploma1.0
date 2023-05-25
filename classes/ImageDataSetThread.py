from threading import Thread
import time
import os
import subprocess
import re
import cv2
from classes.Video import Video
from classes.Line import Line
from PyQt5 import QtCore
from models.Observable import Observable, event


class ImageDataSetThreadSignals(Observable):
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
    def set_finished(self):
        self.finished = True


class ImageDataSetThread(Thread):
    __minimum_tlcr = 60

    def __init__(self, camera_id, id, coords):
        super().__init__()
        self.__camera_id = camera_id
        self.__id = id
        self.__coords = coords
        self.signals = ImageDataSetThreadSignals()

    def run(self):
        # dirs
        camera_dir = os.path.join(Video.video_folder, str(self.__camera_id))
        orig_dir = os.path.join(camera_dir, Video.orig_folder)
        res_dir = os.path.join(camera_dir, Video.res_folder)
        ds_dir = os.path.join(camera_dir, str(self.__id))
        orig_ds_dir = os.path.join(ds_dir, Video.orig_folder)
        res_ds_dir = os.path.join(ds_dir, Video.res_folder)
        if not os.path.exists(orig_ds_dir):
            os.makedirs(orig_ds_dir)
        if not os.path.exists(res_ds_dir):
            os.makedirs(res_ds_dir)

        line = Line(self.__coords)
        # files
        list_files = os.listdir(res_dir)
        self.signals.set_update_progress_max(len(list_files))
        i = 1
        for file in list_files:
            orig_image = cv2.imread(os.path.join(orig_dir, file))
            res_image = cv2.imread(os.path.join(res_dir, file), 0)
            final_orig, final_res = line.get_dataset_images(orig_image, res_image)
            tlcr = line.get_tlcr(final_res)
            if tlcr >= self.__minimum_tlcr:
                cv2.imwrite(os.path.join(orig_ds_dir, file), final_orig)
                cv2.imwrite(os.path.join(res_ds_dir, file), final_res)
            self.signals.set_update_progress(i)
            i += 1
        self.signals.set_finished()
