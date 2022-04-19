# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 11:11:09 2021

@author: Musya
"""

import csv
import os


def writeCsv(list1,list2,list3):
    if os.path.exists('/home/pi/Autonomous-Car/DATA/CSV'):
        os.chdir('/home/pi/Autonomous-Car/DATA/CSV')
    else:
        os.chdir('/home/pi/Autonomous-Car/DATA/')
        os.mkdir('CSV')
        os.chdir('/home/pi/Autonomous-Car/DATA/CSV')
    with open('drivelog.csv', 'w', newline = '') as csvfile:
        fieldnames = ['Image_name','PWML','PWMR']
        theWriter = csv.DictWriter(csvfile,
                                   fieldnames=fieldnames)
        #theWriter.writeheader()
        for i in range(len(list1)):
            theWriter.writerow({'Image_name':list1[i],
                                'PWML':list2[i],
                                'PWMR':list3[i]}
                               )

        print("Data Written:",len(list1))