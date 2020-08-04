import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.functional as F
from sklearn.preprocessing import *
from sklearn.model_selection import train_test_split
import string
from keras.models import Model
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Input
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import Bidirectional
from keras.callbacks import ModelCheckpoint
import tensorflow as tf
import keras


class G2PModel:
    def __init__(self,
                 input_shape,
                 output_shape,
                 saved_weights_path='weights.hdf5'):
        """
        Main class for the prediction model. It is based on google's
        G2P, full delayed model metioned in the paper below:
        https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/43264.pdf

        Input layer is connected to a BLSTM 512units and a LSTM 512units layer,
        where they are both connected to a unidirectional LSTM with 128 unit,
        which then connected to a fully connected layer.
        """

        # The model itself based on the specifications metioned above
        self.input_layer = Input(shape=(None, input_shape))
        self.lstm_512 = LSTM(512, return_sequences=True)(input_layer)
        self.dropout_1 = Dropout(0.4)(lstm_512)
        self.blstm_512 = Bidirectional(
            LSTM(512, return_sequences=True))(input_layer)
        self.dropout_2 = Dropout(0.4)(blstm_512)
        self.lstm_128 = LSTM(128, return_sequences=True)(
            keras.layers.concatenate([dropout_1, dropout_2]))
        self.dropout_3 = Dropout(0.3)(lstm_128)
        self.output = Dense(output_shape, activation='softmax')(dropout_3)
        self.model = Model(self.input_layer, self.output)

        # There are two extra characters aside the phonems and letters,
        # which are '?' and %. '%' represents the end of the word and
        # '?' represents the delay/what's needed to be predicted.
        # So the input for the model for a word like Apple will look
        # like Apple%????, where the model should predict ?????%AEPAHL.
        # In this case '%' in Apple represents the end of the word,
        # followed by 4 '?' characters which the network needs to predict
        # what they are. And the output of the network will be ??????AEPAHL
        # and the characters after the '%' represents the phonems of the
        # word.
        # The primary reason for this is to implement the full delay as
        # described in google's paper.
        self.phonems = None
        self.letters = [[letter]
                        for letter in string.ascii_lowercase + ".'-?%"]
        self.letter_encoder = None
        self.set_letter_encoder()
        self.phonem_encoder = None
        self.checkpoint = ModelCheckpoint(
            filepath, monitor='loss', save_best_only=True, mode='min')
        self.callbacks_list = [checkpoint]
        tf.config.experimental_run_functions_eagerly(True)

    def load_phonems(self, path):
        """
        This will load all the characters used to represent the phonems.
        """
        if self.phonems is None:
            phones = pd.read_csv(path)['Phonems'].to_numpy()
            self.phonems = [[str(ph)] for ph in np.append(phones, '?')]
        self.set_phonem_encoder()

    def set_letter_encoder(self):
        """
        Creates a one-hot encoder model to encode each character.
        This will be used to encode all the words which then will be
        fed into the model
        """
        if self.letter_encoder is None:
            self.letters_encoder = OneHotEncoder()
            letters_encoder.fit(self.letters)

    def set_phonem_encoder(self):
        """
        Creates a one-hot encoder model for the phonems. This will
        be used to encode and decode data for and from the model.
        """
        if self.phonem_encoder is None and self.phonems is not None:
            self.phonem_encoder = OneHotEncoder()
            self.phonem_encoder.fit(self.phonem_encoder)

    def compile_model(self):
        """
        Compiles our model and returns for training or inference.
        """

        self.model.compile(loss='categorical_crossentropy',
                           optimizer='adam', metrics=['accuracy'])
        self.model.summary()
        return self.model

    def text_encoder(self, text):
        """
        Encodes a text into an array of one-hot vectors, which
        the will be fed into the model
        """
        if self.letter_encoder is None:
            self.set_letter_encoder()
        return np.asarray([self.letter_encoder.transform(
            [[i]for i in text]).toarray()])

    def phonem_decoder(self, array):
        """
        This can be used to decode the output of the model. It
        will decode the output of the model, which is an array
        of vectors and takes the argmax of each vector and returns
        the corresponding phonem chars. It will then join them
        to together and return the characters after the '%' char.
        """
        if self.phonem_encoder is None:
            self.set_phonem_encoder()
        return ' '.join([self.phonem_encoder.categories_[0][np.argmax(i)]
                         for i in array]).replace('? ', '')

    def load_model(self, path):
        """
        It will load the weights of a pre-trained model if there is one.
        """
        self.model.load_weights(path)

    def train(self, X, y, num_epochs=20, batch_size=16):
        """
        This code is a bit messy. The reason for it is that when I loaded the
        words, each word had a different shape, and numpy failed to properly
        show the shape of the training data properly. It would show for example
        (180000,), and when tensorflow would look at the shape it would see it
        as a one dimensional matrix, and would throw an error for mismatched
        shape. Therefore, I had to group the data with the same shape together
        and train the model based on the shape of the arrays. Then, I would
        train the next shape and so on.

        The function will train the model based on the training data `X` and
        `y`, and would the weights had there been an improvement in our
        entropy loss for each training step.
        """
        size = set()
        for i in X:
            size.add(np.asarray(i).shape)
        size = list(size)
        for j in size:
            new_X_train = []
            new_Y_train = []
            for i in range(len(X)):
                if len(X[i]) == j[0]:
                    new_X_train.append(np.asarray(X[i]))
                    new_Y_train.append(np.asarray(y_train[i]))
            model.fit(
                np.asarray(new_X_train),
                np.asarray(new_Y_train),
                epochs=num_epochs,
                batch_size=batch_size,
                callbacks=self.callbacks_list)
