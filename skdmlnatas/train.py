import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import sqlite3
from sqlite3 import Error


class DeepLearning:

    def __init__(self):
        pass


    @staticmethod
    def connection(db_name = "game_results.sqlite"):
        con = sqlite3.connect(db_name)
        cursor_db = con.cursor()
        cursor_db.execute('SELECT * FROM games')
        return cursor_db.fetchall()
    
    @staticmethod
    def edit():
        data = DeepLearning.connection()
        # data = np.array(data)
        dat = [[],[],[],[]]
        for i, st in enumerate(data):
            dat[0].append(st[0].split(', '))
            dat[2].append(st[2].split(', '))
            dat[1].append(st[1])
            dat[3].append(st[3])


# Data Prepare START
        global x_train, y_train, x_test, y_test

        x_train, y_train, x_test, y_test = dat


    @staticmethod
    def vgg_block(in_layer, n_conv, n_filter, filter_size=(1, 3), reduce_size=True):
        
        layer = in_layer
        for i in range(n_conv):
            layer = tf.keras.layers.Conv2D(n_filter, filter_size, padding='SAME', activation='relu')(layer)

        if reduce_size:
            layer = tf.keras.layers.MaxPool2D((1, 2))(layer)
        return layer

    @staticmethod
    def train():
        DeepLearning.edit()
        vgg_block = DeepLearning.vgg_block

        # 데이터 형태에 맞게 수정
        input_layer = tf.keras.layers.Input(shape=(10,))  # 1차원 데이터

        # 모델 구성 수정
        vgg_block01 = vgg_block(tf.expand_dims(input_layer, axis=-1), 2, 3)  # 데이터 차원 확장
        vgg_block02 = vgg_block(vgg_block01, 2, 6)
        vgg_block03 = vgg_block(vgg_block02, 3, 12)

        flatten = tf.keras.layers.Flatten()(vgg_block03)
        dense01 = tf.keras.layers.Dense(10, activation='relu')(flatten)
        output = tf.keras.layers.Dense(1, activation='sigmoid')(dense01)  # binary classification이므로 sigmoid

        model = tf.keras.models.Model(input_layer, output)

        # 훈련 시 validation_data 수정
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        model.summary()

        model.fit(x_train, y_train, batch_size=64, epochs=10,
                  validation_split=0.2)  # validation_data 대신 validation_split 사용
        
        
    
    @staticmethod
    def exreal(champs):
        return 
