# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 14:14:56 2021

@author: Musya
"""
import os
dir_ = os.getcwd()
import numpy as np
from utilis import importData,balanceData,loadData,preProcess,createModel,batchGen
import sys
import matplotlib.pyplot as plt
print(dir_)
data = importData()
data = balanceData(data)
os.chdir(dir_)


imgPath,steering,throttle = loadData(dir_,data)

indices  = list(range(imgPath.shape[0]))
training_instances = int(0.9*imgPath.shape[0])
np.random.shuffle(indices)
train_indices = indices[:training_instances]
test_indices = indices[training_instances:]

x_train,x_test = imgPath[train_indices],imgPath[test_indices]
y1_train,y1_test = steering[train_indices],steering[test_indices]
y2_train,y2_test = throttle[train_indices], throttle[test_indices]

print("Training Data",len(x_train))

model = createModel()
model.summary()
history = model.fit(batchGen(x_train,[y1_train,y2_train],1),
                            steps_per_epoch = 500,epochs=50,
                            validation_data = batchGen(x_test,[y1_test,y2_test],1),
                            validation_steps = 250)

os.chdir('/home/pi/Autonomous-Car/')
model.save('driver_version_1.2.h5')

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.legend(['Training','Validation'])
plt.title('Loss')
plt.xlabel('Epoch')
plt.show()