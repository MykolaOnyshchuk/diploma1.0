from threading import Thread
import subprocess
import os
import numpy as np
from queue import Queue
import cv2
import urllib.parse
import time
from skimage.util import img_as_float
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
from models.line.LineSql import LineSql
from models.line.LineModel import LineModel
from models.camera.CameraSql import CameraSql
from classes.Line import Line
from classes.Video import Video
from classes.ImageNet import ImageNet


class LearnUnetThread(Thread):
    max_threads = 5

    def __init__(self, cameras, lines):
        Thread.__init__(self)
        self.__cameras = cameras
        self.__lines = lines

    def run(self):
        # cv
        with PoolExecutor(max_workers=LearnUnetThread.max_threads) as executor:
            for _ in executor.map(LearnUnetThread.__run_cv, self.__cameras):
                pass

        # create dataset
        with PoolExecutor(max_workers=LearnUnetThread.max_threads) as executor:
            for _ in executor.map(LearnUnetThread.__run_create_dataset, self.__lines):
                pass

        print('ready')

    # Потрібно викликати bioinspired, закоментовано частину, тому не працює
    @staticmethod
    def __run_cv(camera):
        camera_id, camera_gplmod, camera_server = camera

        print(camera_id, camera_gplmod, camera_server)
        return

        # dirs
        camera_dir = os.path.join(Video.video_folder, str(camera_id))
        camera_res_dir = os.path.join(camera_dir, Video.res_folder)
        camera_orig_dir = os.path.join(camera_dir, Video.orig_folder)
        os.makedirs(camera_res_dir)
        os.makedirs(camera_orig_dir)


        # # urls
        # urls = Video.get_list_urls(camera_id, camera_gplmod)
        # url_1 = urllib.parse.urljoin(camera_server, urls[-2])
        # url_2 = urllib.parse.urljoin(camera_server, urls[-1])
        # # run app cv
        # app = os.path.join(Video.video_folder, 'PrepareData.exe')
        # args = [app, '-u', url_1, '--u2', url_2, '-d', camera_dir]
        # process = subprocess.Popen(args)
        # process.wait()

    @staticmethod
    def __run_create_dataset(line):
        camera_id, line_id, coords = line

        print(camera_id, line_id, coords)
        return

        # dirs
        camera_dir = os.path.join(Video.video_folder, str(camera_id))
        orig_dir = os.path.join(camera_dir, Video.orig_folder)
        res_dir = os.path.join(camera_dir, Video.res_folder)
        ds_dir = os.path.join(camera_dir, str(line_id))
        orig_ds_dir = os.path.join(ds_dir, Video.orig_folder)
        res_ds_dir = os.path.join(ds_dir, Video.res_folder)
        os.makedirs(orig_ds_dir)
        os.makedirs(res_ds_dir)

        line = Line(coords)
        # files
        list_files = os.listdir(os.path.join(camera_dir, Video.orig_folder))
        for file in list_files:
            orig_image = cv2.imread(os.path.join(orig_dir, file))
            res_image = cv2.imread(os.path.join(res_dir, file), 0)
            final_orig, final_res = line.get_dataset_images(orig_image, res_image)
            cv2.imwrite(os.path.join(orig_ds_dir, file), final_orig)
            cv2.imwrite(os.path.join(res_ds_dir, file), final_res)

    @staticmethod
    def get_cameras_and_lines(cameras):
        list_lines = []
        list_cameras = []
        for i in range(0, cameras.rowCount()):
            camera_id = CameraSql.get_id(cameras.record(i))
            camera_glpmod = CameraSql.get_gplmod(cameras.record(i))
            camera_server = CameraSql.get_server(cameras.record(i))
            # lines
            lines = LineModel(LineSql.all_from_camera(camera_id))
            lines.open()
            lines_count = lines.rowCount()
            if lines_count == 0:
                continue
            for j in range(0, lines_count):
                list_lines.append(
                    (camera_id, LineSql.get_id(lines.record(j)), LineSql.get_list_coords(lines.record(j))))
            list_cameras.append((camera_id, camera_glpmod, camera_server))
            return list_cameras, list_lines

    @staticmethod
    def run_for_cameras(cameras):
        list_cameras, list_lines = LearnUnetThread.get_cameras_and_lines(cameras)
        # thread = LearnUnetThread(list_cameras, list_lines)
        # thread.start()

        # load images from video
        start_time = time.time()

        # line
        id_c, id_l, coords = list_lines[0]
        line = Line(coords)

        camera_id, camera_gplmod, camera_server = list_cameras[0]
        print(camera_id, camera_gplmod, camera_server)
        # urls = Video.get_list_urls(camera_id, camera_gplmod)
        # url = urllib.parse.urljoin(camera_server, urls[-1])
        cam = cv2.VideoCapture(os.path.join(Video.video_folder, camera_id))
        width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frames = []
        while True:
            ret, frame = cam.read()
            if not ret:
                break
            else:
                frames.append(line.get_image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))

        print("%s seconds" % (time.time() - start_time))
        print(len(frames))

        for i in range(0, len(frames)):
            cv2.imwrite(os.path.join(Video.video_folder, 'ppc_{}.jpg'.format(i)), frames[i])

        # # load images
        # dir = 'video/18/6'
        # orig_dir = os.path.join(dir, Video.orig_folder)
        # res_dir = os.path.join(dir, Video.res_folder)
        # list_files = os.listdir(orig_dir)
        #
        # train_x = np.zeros((len(list_files), 256, 256, 3), dtype='float32')
        # train_y = np.zeros((len(list_files), 256, 256, 1), dtype='float32')
        # i = 0
        # for file in list_files:
        #     train_x[i] = np.array(img_as_float(cv2.imread(os.path.join(orig_dir, file))))
        #     train_y[i] = np.asarray(img_as_float(cv2.imread(os.path.join(orig_dir, file), 0)))[..., None].astype(
        #         dtype='float32',
        #         copy=False)
        #     i += 1
        #
        # print('images ready')


        # # net
        # net = ImageNet()
        # net.train(train_x, train_y)
        #
        # print('all ready')


        # count_threads = 5
        # queue = Queue()
        # for i in range(500):
        #     queue.put(i)
        #
        # for i in range(count_threads):
        #     thread = DataSetThread(queue, i)
        #     thread.setDaemon(True)
        #     thread.start()
        # queue.join()
