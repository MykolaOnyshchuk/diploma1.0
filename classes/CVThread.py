from threading import Thread
import time
import os
import subprocess
import re
from classes.Video import Video
from models.Observable import Observable, event


class CVThreadSignals(Observable):
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


class CVThread(Thread):
    __max_files = 200

    def __init__(self, camera_id):
        super().__init__()
        self.__camera_id = camera_id
        self.signals = CVThreadSignals()

    def run(self):
        camera_dir = os.path.join(Video.video_folder, str(self.__camera_id))
        orig_dir = os.path.join(camera_dir, Video.orig_folder)
        res_dir = os.path.join(camera_dir, Video.res_folder)
        if not os.path.exists(orig_dir):
            os.makedirs(orig_dir)
        if not os.path.exists(res_dir):
            os.makedirs(res_dir)
        list_files = [i for i in os.listdir(camera_dir) if i.endswith('.mp4')]
        if not list_files:
            self.signals.set_update_status('не має відео файлів')
            self.signals.set_finished()
            return
        # list_files = list_files[0:200]

        self.signals.set_update_progress_max(len(list_files) + 1)
        pattern = re.compile(r'[^\s]+.mp4')

        len_files = len(list_files)
        print(len_files)
        for i in range(0, len_files, self.__max_files):
            start = i
            end = i + self.__max_files if len_files > i + self.__max_files else len_files

            app = os.path.join(Video.video_folder, 'PrepareData.exe')
            args = [app, '-u', ','.join(list_files[start:end]), '-d', camera_dir]
            process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True, universal_newlines=True)
            self.signals.set_update_progress(1)
            for line in process.stdout:
                print(line)
                result = pattern.search(line)
                if result:
                    file = result.group(0)
                    if file in list_files:
                        number = list_files.index(file)
                        self.signals.set_update_progress(number + 2)
                        self.signals.set_update_status('Обробка файлу: {}\n'.format(file))
            return_code = process.wait()
        self.signals.set_finished()
