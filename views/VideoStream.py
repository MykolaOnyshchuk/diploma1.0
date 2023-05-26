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

        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(self.list_of_videos[0])))
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(self.list_of_videos[1])))
        self.playlist.setPlaybackMode(QMediaPlaylist.Sequential)
        self.mediaPlayer.setPlaylist(self.playlist)

        # Set widget
        self.setGeometry(x, y, width, height)
        self.mediaPlayer.setVideoOutput(self)
        self.playlist.currentMediaChanged.connect(self.next_video_started)
        self.mediaPlayer.play()

        # self.curr_tlcr = []
        # self.curr_intensity = 0
        # self.curr_duration = 0
        # self.curr_timer_tlcr_len = 0
        # self.curr_period = 0
        # self.tsp_arr = []
        #
        #
        # self.next_tlcr = []
        # self.next_intensity = 0
        # self.next_duration = 0
        #
        # self.tlcr_plot = tlcr_plot
        # self.analysis_plot = analysis_plot
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



        list_lines = []
        sql_lines = QSqlQuery('SELECT * FROM line WHERE id={}'.format(6))
        while sql_lines.next():
            list_lines = LineSql.get_list_coords(sql_lines.record())
        print(list_lines)

        self.thread = QThread()
        self.run_image = RunImageNetThread('E:/18/cam18stream_1580709296.mp4', list_lines)

        self.run_image.moveToThread(self.thread)

        self.thread.started.connect(self.run_image.run)
        self.run_image.finished.connect(self.thread.quit)
        self.run_image.finished.connect(self.run_image.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        # Step 6: Start the thread
        self.thread.start()

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
        # if not vid.isNull():
        #     self.get_stat_values(vid)
        b = True

    def get_stat_values(self, vid):
        self.curr_timer_tlcr_len = self.curr_tlcr
        time_period = self.next_duration / len(self.next_tlcr)
        self.curr_period = time_period
        self.curr_tlcr = self.curr_tlcr + self.next_tlcr
        self.curr_intensity = self.next_intensity
        self.curr_duration = self.next_duration

        url = vid.canonicalUrl()
        print(url.fileName())
        next_video_path = self.list_of_videos[self.playlist.nextIndex()]
        tlcr, intensity = self.runVideoAnalyze(next_video_path)
        video_duration = Video.get_video_duration(next_video_path)

        range_size = 30
        tlcr_ranges = [tlcr[i:i + range_size] for i in range(0, len(tlcr), range_size)]
        tlcr_mean = []
        for i in range(len(tlcr_ranges)):
            tlcr_mean.append(sum(tlcr_ranges[i]) / range_size)
        self.next_duration = video_duration
        self.next_tlcr = tlcr_mean
        self.next_intensity = intensity

    def update_plot_with_timer(self):
        self.curr_timer_tlcr_len += 1
        help_curr = self.curr_tlcr[:len(self.curr_tlcr) - (len(self.curr_tlcr) - self.curr_timer_tlcr_len) + 9]
        tsp = int(round(self.curr_dt.timestamp()))
        for i in range(10):
            self.tsp_arr.append(tsp)
        self.tlcr_plot.update_data_tmp(help_curr, self.tsp_arr)
        threading.Timer(self.curr_period, self.update_plot_with_timer).start()

    def runVideoAnalyze(self, video_path):
        list_lines = []
        sql_lines = QSqlQuery('SELECT * FROM line WHERE id={}'.format(6))
        while sql_lines.next():
            list_lines = LineSql.get_list_coords(sql_lines.record())
        print(list_lines)
        thread = RunImageNetThread(video_path, list_lines)
        return thread.run()

        # Write to db and share data with plot somehow
