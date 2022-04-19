# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 14:16:59 2021

@author: Musya
"""

import time
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
import matplotlib.image as mpimg
from imgaug import augmenters as iaa
import cv2
import random
from dynamic import DynamicArray

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D #Import various layers for the Neural Net
from tensorflow.keras.optimizers import Adam  #Import optimizers for the Neural Net
#from keras.layers import concatenate, Dropout

os.chdir('/home/pi/Autonomous-Car/DATA')
os.chdir('/home/pi/Autonomous-Car/DATA/CSV')
path = os.getcwd()

name = os.path.join(path, 'drivelog.csv')
def getName(filePath):
    return filePath.split("\\")[-1]
def importData():
    print("Importing Data...")
    columns = ['Image_name','PWML','PWMR']
    data = pd.read_csv(name,names = columns)
    data['Image_name'] = data['Image_name'].apply(getName)
    #print("Total Rows:", data.shape[0])
    #print("Total Columns:", data.shape[1])
    return data
def balanceData(data):

    nBins = 121
    spBin = 200

    hist,bins = np.histogram(data['PWML'],nBins)
    center = (bins[-1:]+bins[1:])*.5
    plt.bar(center,hist,width = .05)
    plt.plot((0,50),(spBin,spBin))
    plt.title('Initial Distribution')
    #plt.show()


    #hist2,bins2 = np.histogram(data['PWMR'],nBins)
    #center2 = (bins2[-1:]+bins2[1:])*.5
    #plt.bar(center2,hist2,width = .5)
    #plt.plot((0,50),(spBin,spBin))
    #plt.title('Initial Distribution')
    #plt.show()

    q = input("Do you want to balance data? y>Yes/n>No: ")
    q = q.lower()
    if q == ('y' or 'yes'):
        print("Balancing Data...")
        removedIndex = []
        for j in range(nBins):
            binData = []
            for i in range(len(data['PWML'])):
                if data['PWML'][i]>=bins[j] and data['PWML'][i] <= bins[j+1]:
                    binData.append(i)
            binData = shuffle(binData)
            binData = binData[spBin:]
            removedIndex.extend(binData)
        print("Available Images:", len(data))
        data.drop(data.index[removedIndex], inplace = True)
        print("Removed Images:", len(removedIndex))
        print("Remaining Images:", len(data))

        hist,bins = np.histogram(data['PWML'],nBins)
        plt.bar(center,hist,width = .5)
        plt.plot((0,50),(spBin,spBin))
        plt.title('Final Distribution')
        plt.show()

        print("Balancing finished")
    elif q == ('n' or 'no'):
        print("Pass")
        pass
    return data

def loadData(path,data):
    print("Loading Data...")
    imgPath = []
    steering = []
    throttle = []
    for i in range(len(data)):
        indexData = data.iloc[i]
        imgPath.append(os.path.join(path,'DATA\IMG',indexData[0]))
        steering.append(float(indexData[1]))
        throttle.append(float(indexData[2]))
        print(i, "of", len(data))
    imgPath = np.asarray(imgPath)
    steering = np.asarray(steering)
    throttle = np.asarray(throttle)
    print("Returning data")
    return imgPath, steering, throttle

def augmentImage(imgPath,PWML,PWMR):
    img = mpimg.imread(imgPath)
    if np.random.rand() < 0.5:
        zoom = iaa.Affine(scale=(1,1.2))
        img = zoo.augment_image(img)
    if np.random.rand() < 0.5:
        img = cv2.flip(img,1)
        PWML = PWMR
        PWMR = PWML
    return img,PWML,PWMR
def preProcess(img):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    img = cv2.GaussianBlur(img, (3,3),0)
    img = cv2.resize(img, (200,66))/255.0
    return img


def batchGen(imgPath,outputs, batchSize):
    steeringList = outputs[0]
    throttleList = outputs[1]
    while True:
        imgBatch = []
        steeringBatch = []
        throttleBatch = []
        for i in range(batchSize):
            index = random.randint(0, len(imgPath)-1)
            #if trainFlag:
                #img = augmentImage(imgPath[index],
                #steering = steering[index],
                #throttle = throttle[index])
            #else:
            img = mpimg.imread(imgPath[index])
            steering = steeringList[index]
            throttle = throttleList[index]

            img = preProcess(img)
            imgBatch.append(img)
            steeringBatch.append(steering)
            throttleBatch.append(throttle)
        yield(np.asarray(imgBatch),
                [np.asarray(steeringBatch),
                np.asarray(throttleBatch)]
                )

def createModel():
    print("Creating Model")
    img_Input = keras.Input(shape=(66, 200,3), name='Image')

    img = Conv2D(24, (5,5), (2, 2), activation='elu')(img_Input)
    img = Conv2D(36, (5,5), (2, 2), activation='elu')(img)
    img = Conv2D(48, (5,5), (2, 2), activation='elu')(img)
    img = Conv2D(64, (3,3), activation='elu')(img)
    img = Conv2D(64, (3,3), activation='elu')(img)

    img = Flatten()(img)

    img = Dense(100, activation='elu',name="layer1")(img)
    img = Dense(50, activation='elu',name="layer2")(img)
    img = Dense(10, activation='elu',name="layer3")(img)

    steering = Dense(1, name = 'Steering')(img)
    throttle = Dense(1, name = 'Throttle')(img)

    model = keras.Model(inputs = img_Input, outputs = [steering,throttle])
    print("Creating Model Done")
    #keras.utils.plot_model(model,"AI-CAR.jpeg")

    model.compile(loss='mean_squared_error',
              optimizer=Adam(learning_rate=0.0001),
              metrics=['Accuracy'])

    return model