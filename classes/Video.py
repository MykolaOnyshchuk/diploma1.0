import requests
import os
import cv2
from PIL import Image

os.environ['OPENCV_FFMPEG_DEBUG'] = '0'
os.environ['OPENCV_VIDEOIO_DEBUG'] = '0'
# FFREPORT=level=quiet


class Video:
    video_folder = os.path.join(os.getcwd(), 'video')
    res_folder = 'res'
    orig_folder = 'orig'

    @staticmethod
    def get_list_urls(id, gplmod):
        url_gplmod = "http://videoprobki.ua/{}?p1=cam{}&p2={}&p3=1&p4=1".format(gplmod, id, 1)
        list_urls = requests.get(url_gplmod).text.split(", ")
        print('eba', url_gplmod, list_urls)
        list_urls.pop(0)
        # list_urls.pop()
        return list_urls

    @staticmethod
    def get_image(id, gplmod, server):
        # # list_urls = Video.get_list_urls(id, gplmod)
        # # print(list_urls)
        # # cam = cv2.VideoCapture(server + list_urls[0])
        print(id)
        camera_dir = os.path.join(Video.video_folder, str(id))
        dir_contents = os.listdir(camera_dir)
        files = [f for f in dir_contents if os.path.isfile(camera_dir + '/' + f)]
        cam = cv2.VideoCapture(os.path.join(camera_dir, files[0]))
        # cam = cv2.VideoCapture('E:/diploma1.0/video/18/cam18stream_1580707577.mp4')
        # cam = cv2.VideoCapture('D:/projects/python/network/src/video/22/cam22stream_1594272662.mp4')
        print(cam.isOpened())
        ret, frame = cam.read()
        for _ in (0, 5):
            ret, frame = cam.read()
        print(frame)
        # cv2.imshow('frame', frame)
        # # print(id, gplmod, server + list_urls[-1])
        print(os.path.join(camera_dir, files[0]))
        print(ret)
        if not ret:
            return
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame
        # cv2.imshow('trololo', frame)
        # return Image.fromarray(frame)
        # Video.download_video(server + list_urls[-1], os.path.join(Video.video_folder, list_urls[-1]))

    @staticmethod
    def download_video(url, save_url):
        if os.path.isfile(save_url):
            return
        r = requests.get(url)
        with open(save_url, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

    @staticmethod
    def fill_images(video_file, frames):
        cam = cv2.VideoCapture(video_file)
        frame_count = cam.get(cv2.CAP_PROP_FRAME_COUNT)
        num_frame = 0
        for i in range(int(frame_count)):
            ret, frame = cam.read()
            if ret:
                frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            num_frame += 1

    @staticmethod
    def get_video_duration(video_path):
        video = cv2.VideoCapture(video_path)
        duration = video.get(cv2.CAP_PROP_POS_MSEC)
        return duration
