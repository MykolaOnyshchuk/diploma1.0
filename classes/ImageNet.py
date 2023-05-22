# required to work on GPU (do not change because it only works like that)
from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
from keras.backend import set_session
from pympler import muppy, summary

import numpy as np
import os
import time

from keras import Model
from keras.optimizers import Adam
from keras.losses import binary_crossentropy
from keras.layers import Input, Conv2D, Conv2DTranspose, MaxPooling2D, concatenate, Dropout
from keras import backend as K
from keras.utils import get_custom_objects


class ImageNet:
    size_img = 256

    def __init__(self):
        # config = tf.compat.v1.ConfigProto(gpu_options=tf.GPUOptions(per_process_gpu_memory_fraction=0.7),
        #                                   allow_soft_placement=True)
        # config.gpu_options.allow_growth = True
        # # config.gpu.set_per_process_memory_fraction(0.4)
        # config.gpu_options.per_process_gpu_memory_fraction = 0.9
        # set_session(tf.compat.v1.Session(config=config))

        # config = tf.compat.v1.ConfigProto(gpu_options=tf.GPUOptions(per_process_gpu_memory_fraction=0.7),
        #                                   allow_soft_placement=True)
        # config.gpu_options.allow_growth = True
        # # config.gpu.set_per_process_memory_fraction(0.4)
        # set_session(tf.compat.v1.Session(config=config))
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
        self.init()

    def build_model(self, input_layer, start_neurons):
        conv1 = Conv2D(start_neurons * 1, (3, 3), activation="relu", padding="same")(input_layer)
        conv1 = Conv2D(start_neurons * 1, (3, 3), activation="relu", padding="same")(conv1)
        pool1 = MaxPooling2D((2, 2))(conv1)
        pool1 = Dropout(0.25)(pool1)

        conv2 = Conv2D(start_neurons * 2, (3, 3), activation="relu", padding="same")(pool1)
        conv2 = Conv2D(start_neurons * 2, (3, 3), activation="relu", padding="same")(conv2)
        pool2 = MaxPooling2D((2, 2))(conv2)
        pool2 = Dropout(0.5)(pool2)

        conv3 = Conv2D(start_neurons * 4, (3, 3), activation="relu", padding="same")(pool2)
        conv3 = Conv2D(start_neurons * 4, (3, 3), activation="relu", padding="same")(conv3)
        pool3 = MaxPooling2D((2, 2))(conv3)
        pool3 = Dropout(0.5)(pool3)

        conv4 = Conv2D(start_neurons * 8, (3, 3), activation="relu", padding="same")(pool3)
        conv4 = Conv2D(start_neurons * 8, (3, 3), activation="relu", padding="same")(conv4)
        pool4 = MaxPooling2D((2, 2))(conv4)
        pool4 = Dropout(0.5)(pool4)

        # Middle
        convm = Conv2D(start_neurons * 16, (3, 3), activation="relu", padding="same")(pool4)
        convm = Conv2D(start_neurons * 16, (3, 3), activation="relu", padding="same")(convm)

        deconv4 = Conv2DTranspose(start_neurons * 8, (3, 3), strides=(2, 2), padding="same")(convm)
        uconv4 = concatenate([deconv4, conv4])
        uconv4 = Dropout(0.5)(uconv4)
        uconv4 = Conv2D(start_neurons * 8, (3, 3), activation="relu", padding="same")(uconv4)
        uconv4 = Conv2D(start_neurons * 8, (3, 3), activation="relu", padding="same")(uconv4)

        deconv3 = Conv2DTranspose(start_neurons * 4, (3, 3), strides=(2, 2), padding="same")(uconv4)
        uconv3 = concatenate([deconv3, conv3])
        uconv3 = Dropout(0.5)(uconv3)
        uconv3 = Conv2D(start_neurons * 4, (3, 3), activation="relu", padding="same")(uconv3)
        uconv3 = Conv2D(start_neurons * 4, (3, 3), activation="relu", padding="same")(uconv3)

        deconv2 = Conv2DTranspose(start_neurons * 2, (3, 3), strides=(2, 2), padding="same")(uconv3)
        uconv2 = concatenate([deconv2, conv2])
        uconv2 = Dropout(0.5)(uconv2)
        uconv2 = Conv2D(start_neurons * 2, (3, 3), activation="relu", padding="same")(uconv2)
        uconv2 = Conv2D(start_neurons * 2, (3, 3), activation="relu", padding="same")(uconv2)

        deconv1 = Conv2DTranspose(start_neurons * 1, (3, 3), strides=(2, 2), padding="same")(uconv2)
        uconv1 = concatenate([deconv1, conv1])
        uconv1 = Dropout(0.5)(uconv1)
        uconv1 = Conv2D(start_neurons * 1, (3, 3), activation="relu", padding="same")(uconv1)
        uconv1 = Conv2D(start_neurons * 1, (3, 3), activation="relu", padding="same")(uconv1)

        uncov1 = Dropout(0.5)(uconv1)
        output_layer = Conv2D(1, (1, 1), padding="same", activation="sigmoid")(uconv1)
        return output_layer

    def dice_coeficient(self, y_true, y_pred):
        y_true_f = K.flatten(y_true)
        y_pred = K.cast(y_pred, 'float32')
        y_pred_f = K.cast(K.greater(K.flatten(y_pred), 0.5), 'float32')
        intersection = y_true_f * y_pred_f
        score = 2. * K.sum(intersection) / (K.sum(y_true_f) + K.sum(y_pred_f))
        return score

    def dice_loss(self, y_true, y_pred):
        smooth = 1.
        y_true_f = K.flatten(y_true)
        y_pred_f = K.flatten(y_pred)
        intersection = y_true_f * y_pred_f
        score = (2. * K.sum(intersection) + smooth) / (K.sum(y_true_f) + K.sum(y_pred_f) + smooth)
        return 1. - score

    def bce_dice_loss(self, y_true, y_pred):
        return binary_crossentropy(y_true, y_pred) + self.dice_loss(y_true, y_pred)

    def get_iou_vector(self, A, B):
        # Numpy version

        batch_size = A.shape[0]
        metric = 0.0
        for batch in range(batch_size):
            t, p = A[batch], B[batch]
            true = np.sum(t)
            pred = np.sum(p)

            # deal with empty mask first
            if true == 0:
                metric += (pred == 0)
                continue

            # non empty mask case.  Union is never empty
            # hence it is safe to divide by its number of pixels
            intersection = np.sum(t * p)
            union = true + pred - intersection
            iou = intersection / union

            # iou metric is a stepwise approximation of the real iou over 0.5
            iou = np.floor(max(0, (iou - 0.45) * 20)) / 10

            metric += iou

        # take the average over all images in batch
        metric /= batch_size
        return metric

    def my_iou_metric(self, label, pred):
        # Tensorflow version
        return tf.py_func(self.get_iou_vector, [label, pred > 0.5], tf.float64)

    def init(self):
        get_custom_objects().update({'bce_dice_loss': self.bce_dice_loss})
        get_custom_objects().update({'dice_loss': self.dice_loss})
        get_custom_objects().update({'dice_coef': self.dice_coeficient})
        get_custom_objects().update({'my_iou_metric': self.my_iou_metric})

        input_layer = Input((self.size_img, self.size_img, 3))
        output_layer = self.build_model(input_layer, 16)
        self.model = Model(input_layer, output_layer)
        self.model.compile(loss=self.bce_dice_loss, optimizer=Adam(lr=1e-3), metrics=[self.my_iou_metric])
        # self.model.save_weights('./keras.weights')
        # self.model.load_weights('./kerasFINAL.weights', by_name=False)

    def train(self, train_x, train_y, epochs=10):
        history = self.model.fit(train_x, train_y, batch_size=32, epochs=epochs, verbose=1, validation_split=0.1)
        # self.model.save_weights('./kerasFINAL.weights')

    def save_weights(self, file_name):
        self.model.save_weights(file_name)

    def load_weights(self, file_name):
        self.model.load_weights(file_name, by_name=False)

    def predict(self, image_array):
        return self.model.predict(image_array)
