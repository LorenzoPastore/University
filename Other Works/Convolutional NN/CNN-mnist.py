# -*- coding: utf-8 -*-
"""CNN-mnist.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eKoRAXCPoDM2vYTFc0kYcIg9iDiIYvI9

# Assignment 3

**LORENZO PASTORE**

l.pastore6@campus.unimib.it

The task of the assignment #3 is the design of a CNN architecture and its training.

Input dataset: MNIST digits (input size 28x28x1, number of classes: 10).
The dataset is not distributed since can be easily downloaded directly from Keras.
Please consider the original dataset partition into trainig-valid-test (no other splits or cross-validation are needed).

The CNN has to be designed with the hard constraint of a maximum of 7.5K parameters.

The report must contain:
- a description of the designed architecture
- the parameters count for each layer
- the hyper-parameters used for training (batch size, learning rate, optimizer, number of epochs, etc)
- a plot of the training and validation loss/accuracy 
- classification performance on training, validation (if available) and test sets

## Data import and Preprocessing
"""

import keras
import pandas as pd
import numpy as np
from keras.utils import np_utils
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D, BatchNormalization
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from keras.callbacks import LearningRateScheduler
import tensorflow as tf
import matplotlib as mpl

# load dataset and split into train and validation
from keras.datasets import mnist
(trainx, trainy), (testx, testy) = mnist.load_data()

trainx.shape

testx.shape

from collections import Counter
count = Counter(trainy)
count

# viene effettuata l'operazione di normalizzazione dei pixel in scala di grigi.
trainx = trainx.astype('float32')/ 255.0
testx = testx.astype('float32')/ 255.0
# la dimensione degli array viene ridefinita in maniera da avere un unico canale di colore
trainx = trainx.reshape((trainx.shape[0],28,28,1))
testx = testx.reshape((testx.shape[0],28,28,1))
# gli array delle etichette vengono ridefiniti in forma categorica
trainy = np_utils.to_categorical(trainy)
testy = np_utils.to_categorical(testy)
# il training set viene diviso in modo da avere un validation set
x_train, x_val, y_train, y_val = train_test_split(trainx, trainy, test_size=0.2)

"""## CNN structure"""

batch_size = 1024
input_shape = (28, 28, 1)

"""Al fine di definire l'architettura più adatta, procediamo nel testare la sensibilità di alcune delle principali caratteristiche che dovrebbe avere una rete Convoluzionale.

### 1. Quanti livelli di convoluzione utilizzare?
"""

# BUILD CONVOLUTIONAL NEURAL NETWORKS
epochs = 10
nets = 3
model = [0] *nets

for j in range(3):
    model[j] = Sequential()
    model[j].add(Conv2D(16,kernel_size=5,padding='same',activation='relu',
            input_shape=input_shape))
    model[j].add(MaxPool2D())
    if j>0:
        model[j].add(Conv2D(32,kernel_size=5,padding='same',activation='relu'))
        model[j].add(MaxPool2D())
    if j>1:
        model[j].add(Conv2D(64,kernel_size=5,padding='same',activation='relu'))
        model[j].add(MaxPool2D())
    model[j].add(Flatten())
    model[j].add(Dense(128, activation='relu'))
    model[j].add(Dense(10, activation='softmax'))
    model[j].compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# TRAIN NETWORKS
history = [0] * nets
names = ["Cnn_layer1","Cnn_layer2","Cnn_layer3"]

for j in range(nets):
    history[j] = model[j].fit(x_train,y_train,
                              batch_size=batch_size,
                              epochs = epochs, 
                              validation_data = (x_val, y_val),
                              verbose=0)    
    print("CNN {0}: Epochs={1:d}, Train accuracy={2:.5f}, Validation accuracy={3:.5f}".format(
        names[j],epochs,max(history[j].history['acc']),max(history[j].history['val_acc']) ))

styles=[':','-.','--','-',':','-.','--','-',':','-.','--','-']
plt.figure(figsize=(15,5))
for i in range(nets):
    plt.plot(history[i].history['val_acc'],linestyle=styles[i])
plt.title('Model accuracy with different convolutional layers')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(names, loc='upper left')
axes = plt.gca()
axes.set_ylim([0.95,1])
plt.show()

"""### 2. Quante features mappare?"""

# BUILD CONVOLUTIONAL NEURAL NETWORKS
epochs = 10
nets_layer = 8
model = [0] *nets_layer
for j in range(8):
    model[j] = Sequential()
    model[j].add(Conv2D(j*2+1,kernel_size=5,activation='relu',input_shape=input_shape))
    model[j].add(MaxPool2D())
    model[j].add(Conv2D(j*2+2,kernel_size=5,activation='relu'))
    model[j].add(MaxPool2D())
    model[j].add(Flatten())
    model[j].add(Dense(28, activation='relu'))
    model[j].add(Dense(10, activation='softmax'))
    model[j].compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# TRAIN NETWORKS
history = [0] * nets_layer
names = ["3 maps","5 maps","7 maps","9 maps","11 maps","13 maps","15 maps","17 maps"]
for j in range(nets_layer):
    history[j] = model[j].fit(x_train,y_train,
                              batch_size=batch_size,
                              epochs = epochs, 
                              validation_data = (x_val, y_val),
                              verbose=0)    
    print("CNN {0}: Epochs={1:d}, Train accuracy={2:.5f}, Validation accuracy={3:.5f}".format(
        names[j],epochs,max(history[j].history['acc']),max(history[j].history['val_acc']) ))

plt.figure(figsize=(15,5))
for i in range(nets_layer):
    plt.plot(history[i].history['val_acc'],linestyle=styles[i])
plt.title('Model accuracy with different numbers of features')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(names, loc='upper left')
axes = plt.gca()
axes.set_ylim([0.89,0.99])
plt.show()

"""### 3. Quanto grandi devono essere i dense layer?"""

# BUILD CONVOLUTIONAL NEURAL NETWORKS
epochs = 10
nets = 6
model = [0] *nets
for j in range(6):
    model[j] = Sequential()
    model[j].add(Conv2D(11,kernel_size=5,activation='relu',input_shape=input_shape))
    model[j].add(MaxPool2D())
    model[j].add(Conv2D(12,kernel_size=5,activation='relu'))
    model[j].add(MaxPool2D())
    model[j].add(Flatten())
    if j>0:
        model[j].add(Dense((14+j), activation='relu'))
    model[j].add(Dense(10, activation='softmax'))
    model[j].compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# TRAIN NETWORKS
history = [0] * nets
names = ["15N","16N","17N","18N","19N","20N"]
for j in range(nets):
    history[j] = model[j].fit(x_train,y_train,
                              batch_size=batch_size,
                              epochs = epochs, 
                              validation_data = (x_val,y_val), 
                              verbose=0)
    print("CNN {0}: Epochs={1:d}, Train accuracy={2:.5f}, Validation accuracy={3:.5f}".format(
        names[j],epochs,max(history[j].history['acc']),max(history[j].history['val_acc']) ))

plt.figure(figsize=(15,5))
for i in range(nets):
    plt.plot(history[i].history['val_acc'],linestyle=styles[i])
plt.title('model accuracy with different dense layer units')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(names, loc='upper left')
axes = plt.gca()
axes.set_ylim([0.90,0.99])
plt.show()

"""### 4. Quanto dropout inserire nel modello?"""

# BUILD CONVOLUTIONAL NEURAL NETWORKS
epochs = 10
nets = 8
model = [0] *nets
for j in range(8):
    model[j] = Sequential()
    model[j].add(Conv2D(11,kernel_size=3,activation='relu',input_shape=input_shape))
    model[j].add(MaxPool2D())
    model[j].add(Dropout(j*0.1))
    model[j].add(Conv2D(12,kernel_size=3,activation='relu'))
    model[j].add(MaxPool2D())
    model[j].add(Dropout(j*0.1))
    model[j].add(Flatten())
    model[j].add(Dense(17, activation='relu'))
    model[j].add(Dropout(j*0.1))
    model[j].add(Dense(10, activation='softmax'))
    model[j].compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# TRAIN NETWORKS
history = [0] * nets
names = ["D=0","D=0.1","D=0.2","D=0.3","D=0.4","D=0.5","D=0.6","D=0.7"]
epochs = 10
for j in range(nets):
    history[j] = model[j].fit(x_train,y_train, 
                              batch_size=batch_size, 
                              epochs = epochs, 
                              validation_data = (x_val,y_val), 
                              verbose=0)
    print("CNN {0}: Epochs={1:d}, Train accuracy={2:.5f}, Validation accuracy={3:.5f}".format(
        names[j],epochs,max(history[j].history['acc']),max(history[j].history['val_acc']) ))

# PLOT ACCURACIES
plt.figure(figsize=(15,5))
for i in range(nets):
    plt.plot(history[i].history['val_acc'],linestyle=styles[i])
plt.title('model accuracy with different dropout %')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(names, loc='upper left')
axes = plt.gca()
axes.set_ylim([0.85,1])
plt.show()

# BUILD CONVOLUTIONAL NEURAL NETWORKS
epochs = 10
nets = 2
model = [0] *nets

j=0
model[j] = Sequential()
model[j].add(Conv2D(11,kernel_size=3,activation='relu',input_shape=(28,28,1)))
model[j].add(MaxPool2D())
model[j].add(Dropout(0.2))
model[j].add(Conv2D(12,kernel_size=3,activation='relu'))
model[j].add(MaxPool2D())
model[j].add(Dropout(0.2))
model[j].add(Flatten())
model[j].add(Dense(17, activation='relu'))
model[j].add(Dropout(0.2))
model[j].add(Dense(10, activation='softmax'))
model[j].compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

j=1
model[j] = Sequential()
model[j].add(Conv2D(11,kernel_size=5,activation='relu',input_shape=(28,28,1)))
model[j].add(MaxPool2D())
model[j].add(Dropout(0.2))
model[j].add(Conv2D(12,kernel_size=5,activation='relu'))
model[j].add(MaxPool2D())
model[j].add(Dropout(0.2))
model[j].add(Flatten())
model[j].add(Dense(17, activation='relu'))
model[j].add(Dropout(0.2))
model[j].add(Dense(10, activation='softmax'))
model[j].compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# TRAIN NETWORKS 1,2
history = [0] * nets
names = ["ksize_3","ksize_5"]
for j in range(nets):
    history[j] = model[j].fit(x_train,y_train,
                              batch_size=batch_size,
                              epochs = epochs,
                              validation_data = (x_val,y_val),
                              verbose=0)
    print("CNN {0}: Epochs={1:d}, Train accuracy={2:.5f}, Validation accuracy={3:.5f}".format(
        names[j],epochs,max(history[j].history['acc']),max(history[j].history['val_acc']) ))

# PLOT ACCURACIES
plt.figure(figsize=(15,12))
plt.subplot(2,1,nets)
for i in range(nets):
    plt.plot( history[i].history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(names, loc='upper left')
axes = plt.gca()
axes.set_ylim([0.90,1])
plt.show()
plt.figure(figsize=(14,6))
for i in range(nets):
    plt.plot(history[i].history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(names, loc='upper left')
axes = plt.gca()
axes.set_ylim([0.0,1])
plt.show()

"""### Final CNN Model"""

model_1 = Sequential()
model_1.add(Conv2D(11,kernel_size=5,activation='relu',input_shape=(28,28,1)))
model_1.add(MaxPool2D())
model_1.add(Dropout(0.2))
model_1.add(Conv2D(12,kernel_size=5,activation='relu'))
model_1.add(MaxPool2D())
model_1.add(Dropout(0.2))
model_1.add(Flatten())
model_1.add(Dense(17, activation='relu'))
model_1.add(Dropout(0.2))
model_1.add(Dense(10, activation='softmax'))
model_1.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

model_1.summary()

model_history = model_1.fit(x_train,y_train,
                          batch_size=batch_size,
                          epochs=30,
                          validation_data=(x_val,y_val))

# summarize history for accuracy
plt.plot(model_history.history['acc'])
plt.plot(model_history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='lower right')
plt.show()
# summarize history for loss
plt.plot(model_history.history['loss'])
plt.plot(model_history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper right')
plt.show()

model_1.evaluate(testx,testy)