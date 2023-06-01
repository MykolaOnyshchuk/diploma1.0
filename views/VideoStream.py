import sys
import threading
from datetime import datetime
from threading import Thread
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from models.line.LineSql import LineSql
from classes.RunImageNetThread import RunImageNetThread
from classes.Video import Video


# class AnalysisThread(QThread):
#     def __init__(self, video_path, list_lines):
#         super(AnalysisThread, self).__init__()
#         self.video_path = video_path
#         self.list_lines = list_lines
#
#     def run(self):
#         thread = RunImageNetThread(self.video_path, self.list_lines)
#         thread.run()


class VideoStream(QVideoWidget):
    def __init__(self, x, y, width, height, tlcr_plot, analysis_plot):
        super(VideoStream, self).__init__()
        self.curr_dt = datetime.now()

        self.playlist = QMediaPlaylist()
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.list_of_videos = []
        self.list_of_videos.append('E:/18/cam18stream_1580707577.mp4')
        self.list_of_videos.append('E:/18/cam18stream_1580707638.mp4')
        self.list_of_videos.append('E:/18/cam18stream_1580715806.mp4')

        for video in self.list_of_videos:
            self.playlist.addMedia((QMediaContent(QUrl.fromLocalFile(video))))
        self.playlist.setPlaybackMode(QMediaPlaylist.Sequential)
        self.mediaPlayer.setPlaylist(self.playlist)

        # Set widget
        self.setGeometry(x, y, width, height)
        self.mediaPlayer.setVideoOutput(self)
        self.playlist.currentMediaChanged.connect(self.next_video_started)
        # self.mediaPlayer.play()

        self.curr_tlcr = []
        self.curr_intensity = 0
        self.curr_duration = 0
        self.curr_timer_tlcr_len = 0
        self.curr_period = 0
        self.tsp_arr = []
        self.range_size = 30
        self.first_video_currently = True


        self.next_tlcr = []
        self.next_intensity = 0
        self.next_duration = 0

        self.tlcr_plot = tlcr_plot
        self.analysis_plot = analysis_plot
        #
        # s = []
        # f = open("D:/Chrome Downloads/mock_tlcr.txt", "r")
        # s = f.readline()
        # tlcr_arr = s.split(';')
        # for i in range(len(tlcr_arr)):
        #     tlcr_arr[i] = float(tlcr_arr[i])
        #     print(tlcr_arr[i])
        #
        # self.curr_intensity = float(f.readline())
        # f.close()
        # range_size = 30
        # tlcr_ranges = [tlcr_arr[i:i + range_size] for i in range(0, len(tlcr_arr), range_size)]
        # tlcr_mean = []
        # for i in range(len(tlcr_ranges)):
        #     tlcr_mean.append(sum(tlcr_ranges[i]) / range_size)
        # self.curr_tlcr = tlcr_mean
        # self.curr_duration = Video.get_video_duration('E:/18/cam18stream_1580707577.mp4')
        # self.curr_period = self.curr_duration / len(self.curr_tlcr)
        # print(self.curr_intensity)
        #
        # f = open("D:/Chrome Downloads/mock_tlcr_2.txt", "r")
        # s_2 = f.readline()
        # self.next_intensity = float(f.readline())
        # f.close()
        # tlcr_arr_2 = s_2.split(';')
        #
        # self.update_plot_with_timer()

        # print(tlcr, intensity)

        vid = self.list_of_videos[0]
        self.run_first_current_video_analysis(vid)



        # list_lines = []
        # sql_lines = QSqlQuery('SELECT * FROM line WHERE id={}'.format(6))
        # while sql_lines.next():
        #     list_lines = LineSql.get_list_coords(sql_lines.record())
        # print(list_lines)
        #
        # self.thread = QThread()
        # self.run_image = RunImageNetThread('E:/18/cam18stream_1580709296.mp4', list_lines)
        #
        # self.run_image.moveToThread(self.thread)
        #
        # self.thread.started.connect(self.run_image.run)
        # self.run_image.finished.connect(self.thread.quit)
        # self.run_image.finished.connect(self.run_image.deleteLater)
        # self.thread.finished.connect(self.thread.deleteLater)
        # # Step 6: Start the thread
        # self.thread.start()

        # list_lines = []
        # sql_lines = QSqlQuery('SELECT * FROM line WHERE id={}'.format(6))
        # while sql_lines.next():
        #     list_lines = LineSql.get_list_coords(sql_lines.record())
        # print(list_lines)
        #
        # self.thread = QThread()
        # self.run_image = RunImageNetThread('E:/18/cam18stream_1580709296.mp4', list_lines)
        #
        # self.run_image.moveToThread(self.thread)
        #
        # self.thread.started.connect(self.run_image.run)
        # self.run_image.finished.connect(self.thread.quit)
        # self.run_image.finished.connect(self.run_image.deleteLater)
        # self.thread.finished.connect(self.thread.deleteLater)
        # # Step 6: Start the thread
        # self.thread.start()
        # self.thread.wait()
        #
        # thread_lock = threading.Lock()
        #
        # # Create thread
        # t1 = threading.Thread(target=self.mediaPlayer.play, args=(2, 1, thread_lock))
        # t2 = threading.Thread(target=thread.run, args=(2, 2, thread_lock))
        #
        # # Start task execution
        # t1.start()
        # t2.start()
        #
        # # Wait for thread to complete execution
        # t1.join()
        # t2.join()
        #
        # thread.run()



    def next_video_started(self, vid):
        if not vid.isNull():
            self.get_stat_values(vid)

    def get_stat_values(self, vid):
        self.switch_next_to_curr()

        url = vid.canonicalUrl()
        print(url.fileName())
        next_video_path = self.list_of_videos[self.playlist.nextIndex()]
        video_duration = Video.get_video_duration(next_video_path)
        self.next_duration = video_duration
        print("DURATION")
        print(video_duration)
        self.run_video_analysis(next_video_path)

    def update_plot_with_timer(self):
        self.curr_dt = datetime.now()
        self.curr_timer_tlcr_len += 1
        help_curr = self.curr_tlcr[:self.curr_timer_tlcr_len]
        tsp_full = self.curr_dt.timestamp()
        tsp = int(round(tsp_full))
        print("DATETIME DIFF")
        print(datetime.fromtimestamp(tsp_full))
        print(datetime.fromtimestamp(tsp))

        self.tsp_arr.append(tsp)
        self.tlcr_plot.update_data_tmp(help_curr, self.tsp_arr)
        # y = []
        # y.append(0.58)
        # y.append(0.64)
        # y.append(0.22)
        # y.append(0.47)
        # y.append(0.75)
        #
        # x = []
        # for i in range(0, 5):
        #     x.append(1684792800 + i * 1000)
        # self.tlcr_plot.update_data_tmp(y, x)
        print("PERIOD")
        print(self.curr_period)
        threading.Timer(self.curr_period, self.update_plot_with_timer).start()

    def run_video_analysis(self, video_path):
        list_lines = []
        sql_lines = QSqlQuery('SELECT * FROM line WHERE id={}'.format(6))
        while sql_lines.next():
            list_lines = LineSql.get_list_coords(sql_lines.record())
        print(list_lines)

        self.thread = QThread()
        self.run_image = RunImageNetThread(video_path, list_lines)

        self.run_image.moveToThread(self.thread)

        self.thread.started.connect(self.run_image.run)
        self.run_image.finished.connect(self.set_tlcr_and_intensity)
        self.run_image.finished.connect(self.thread.quit)
        self.run_image.finished.connect(self.run_image.deleteLater)
        if self.first_video_currently:
            self.run_image.finished.connect(self.mediaPlayer.play)
            self.run_image.finished.connect(self.run_first_next_video_analysis)
            self.run_image.finished.connect(self.update_plot_with_timer)
            self.first_video_currently = False
        self.thread.finished.connect(self.thread.deleteLater)
        # Step 6: Start the thread
        self.thread.start()

    def set_tlcr_and_intensity(self):
        tlcr, intensity = self.run_image.get_tlcr_and_intensity()
        tlcr_ranges = [tlcr[i:i + self.range_size] for i in range(0, len(tlcr), self.range_size)]
        tlcr_mean = []
        for i in range(len(tlcr_ranges)):
            tlcr_mean.append(sum(tlcr_ranges[i]) / self.range_size)
        print("TLCR")
        print(tlcr_mean)
        self.next_tlcr = tlcr_mean
        self.next_intensity = intensity

    def run_first_current_video_analysis(self, vid):
        video_duration = Video.get_video_duration(vid)
        self.next_duration = video_duration
        self.run_video_analysis(vid)
        print("DURATION")
        print(video_duration)

    def run_first_next_video_analysis(self):
        self.switch_next_to_curr()

        video_duration = Video.get_video_duration(self.list_of_videos[1])
        self.next_duration = video_duration
        self.run_video_analysis(self.list_of_videos[1])
        print("DURATION")
        print(video_duration)

    def switch_next_to_curr(self):
        self.curr_timer_tlcr_len = len(self.curr_tlcr)
        time_period = self.next_duration / len(self.next_tlcr)
        self.curr_period = time_period
        self.curr_tlcr = self.curr_tlcr + self.next_tlcr
        self.curr_intensity = self.next_intensity
        self.curr_duration = self.next_duration
