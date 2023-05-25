from threading import Thread
import time
import os
import subprocess
import re
import urllib.parse
from classes.Video import Video
from PyQt5 import QtCore
from models.Observable import Observable, event


class LoadVideoThreadSignal(Observable):
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


class LoadVideoThread(Thread):
    __max_files = 200

    def __init__(self, camera_id, gplmod, server):
        super().__init__()
        self.__camera_id = camera_id
        self.__gplmod = gplmod
        self.__server = server
        self.signals = LoadVideoThreadSignal()

    def run(self):
        camera_dir = os.path.join(Video.video_folder, str(self.__camera_id))
        if not os.path.exists(camera_dir):
            os.makedirs(camera_dir)
        urls = Video.get_list_urls(self.__camera_id, self.__gplmod)
        # urls = sorted(filter(lambda x: os.path.isfile(os.path.join(camera_dir, x)),
        #                               os.listdir(camera_dir)))
        size = len(urls)
        self.signals.set_update_progress_max(size)
        for i in range(0, size):
            self.signals.set_update_status('Завантаження {}'.format(urls[i]))
            Video.download_video(urllib.parse.urljoin(self.__server, urls[i]), os.path.join(camera_dir, urls[i]))
            self.signals.set_update_progress(i + 1)

        self.signals.set_finished()
