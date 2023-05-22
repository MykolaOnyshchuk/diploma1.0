import numpy
import matplotlib.pyplot as plt
# import pandas
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as md
from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import MinMaxScaler
# from sklearn.metrics import mean_squared_error

class ReccurentNet:
    def __init__(self):
        numpy.random.seed(7)
        return

    def moving_average(self, a, n=3):
        ret = numpy.cumsum(a, dtype=float)
        ret[n:] = ret[n:] - ret[:-n]
        return ret[n - 1:] / n

    def run2(self, xtest, ytest, xtsp):

        ppcdel = 255
        x_test = xtest / ppcdel
        y_test = ytest / ppcdel

        model = Sequential()
        model.add(LSTM(1, batch_input_shape=(None, None, 1), return_sequences=True))
        model.add(LSTM((1), return_sequences=False))
        model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['accuracy'])
        model.summary()

        model.load_weights('./ltsm.weights')

        results = model.predict(x_test)

        fig, ax = plt.subplots()
        # fig.autofmt_xdate()
        # xfmt = md.DateFormatter('%H:%M')

        # r_y_test = y_test
        # r_results = results

        r_y_test = numpy.array(y_test, dtype=float)
        r_results = numpy.array(results, dtype=float)

        # r_y_test = []
        # r_results = []
        #
        # temp_y_test = 0.0
        # temp_results = 0.0
        # for i in range(0, len(y_test)):
        #     temp_y_test += y_test[i]
        #     temp_results += results[i]
        #     if (i+1) % 10 == 0:
        #         r_y_test.append(temp_y_test/10)
        #         r_results.append(temp_results/10)
        #         temp_y_test = 0.0
        #         temp_results = 0.0
        #
        # print(len(r_y_test))

        x = numpy.arange(len(r_y_test))


        # indicies = numpy.arange(len(y_test))
        # numpy.random.shuffle(indicies)
        # r_y_test = y_test[indicies]
        # r_results = results[indicies]

        ax.plot(x, r_y_test, 'r', x, r_results, 'b')
        #, x, r_results, 'b'
        lgnd = ax.legend(['Факт', 'Прогноз'], loc='upper right', shadow=True)
        # ax.xaxis.set_major_formatter(xfmt)
        plt.style.use('fivethirtyeight')
        plt.show()

        for i in range(len(r_y_test)):
            print(r_y_test[i] , '\t', r_results[i][0])

        # for i in r_y_test:
        #     print(i)
        # print('-----------------')
        # for i in r_results:
        #     print(i[0])

        # plt.plot(results)
        # plt.show()
        #
        # plt.plot(y_test)
        # plt.show()

    def run(self, x, y, xtest, ytest, xtsp):
        # create and fit the LSTM network
        print('yeah')

        ppcdel = 255

        x_train = x / ppcdel
        y_train = y / ppcdel
        x_test = xtest / ppcdel
        y_test = ytest / ppcdel

        # x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=4)

        model = Sequential()
        model.add(LSTM(1, batch_input_shape=(None, None, 1), return_sequences=True))
        model.add(LSTM((1), return_sequences=False))
        model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['accuracy'])
        model.summary()
        history = model.fit(x_train, y_train, epochs=1500, validation_data=(x_test, y_test))

        model.save_weights('./ltsm.weights')

        results = model.predict(x_test)
        # plt.scatter(range(len(results)), results, c='r')
        # plt.scatter(range(len(y_test)), y_test, c='g')
        # plt.show()

        fig, ax = plt.subplots()
        _x1 = numpy.arange(0,80,1)
        print(history.history.keys())
        _y1 = history.history['acc']
        _y2 = history.history['val_acc']
        _y3 = history.history['loss']
        _y4 = history.history['val_loss']
        # ax.stackplot(_x1, _y1, _x1, _y2, _x1, _y3, _x1, _y4, labels=['accuracy', 'val_accuracy', 'loss', 'val_loss'])
        # ax.legend(loc='upper right')
        plt.plot(_y1)
        plt.show()
        plt.plot(_y2)
        plt.show()
        plt.plot(_y3)
        plt.show()
        plt.plot(_y4)
        plt.show()

        print(_y1)
        print("aaaa")
        print(_y4)
        print("bbbb")

        print(_y1[len(_y1)-1])
        print(_y4[len(_y4) - 1])

        fig, ax = plt.subplots()
        fig.autofmt_xdate()
        xfmt = md.DateFormatter('%H:%M')
        # %H:%M

        # k = 60
        # y1 = self.moving_average(results, k)
        # y2 = self.moving_average(y_test, k)
        # x = xtsp
        # del x[0:k - 1]

        # x = numpy.arange(len(y1))
        # ax.plot(xtsp, y_test*60, 'r', xtsp, results*60, 'b')
        ax.plot(xtsp, y_test, 'r', xtsp, results, 'b')
        lgnd = ax.legend(['Факт', 'Прогноз'], loc='upper right', shadow=True)
        ax.xaxis.set_major_formatter(xfmt)
        plt.style.use('fivethirtyeight')
        plt.show()

        # plt.plot(results*60)
        plt.plot(results)
        plt.show()

        # plt.plot(y_test*60)
        plt.plot(y_test)
        plt.show()

        # print(results)
        # print('aaaa')
        # print(y_test)

        # print(len(y_test), len(results))

        # trainX = numpy.reshape(x, (x.shape[0], 1, x.shape[1]))
        # trainY = y

        # model = Sequential()
        # model.add(LSTM(4, input_shape=(1, look_back)))
        # model.add(Dense(1))
        # model.compile(loss='mean_squared_error', optimizer='adam')
        # model.fit(x, y, epochs=1, batch_size=1, verbose=2)
        print('end')
        return