#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Scoring Algorithm Functions

Originally authored by Annie Taylor (annietay@umich.edu) for Alex Bova's rat
reaching data. Modified by Krista Kernodle (kkrista@umich.edu) for mouse
reaching data.

Created on Mon Sep  9 10:47:35 2019

@author: Annie Taylor
@author: Krista Kernodle
"""
import numpy as np
import pandas as pd
import time
import os

def importLabels(filenames, rat):
    time1 = time.time()
    manualScores = pd.DataFrame()
    for i in filenames:
        print(i)
        print(rat)
        if (rat in i):
            filenameString = i
            cols = pd.read_csv(filenameString).columns
            manualScores = pd.read_csv(filenameString,header=0,usecols=cols[1:])
        else:
            manualScores = pd.DataFrame()
    #print('importLabels runtime: %f' % (time2 - time1))
    
    #Indexing in pandas:
    #manualScores.at[3,'11/4/17']
    #manualScores.iloc[r,c]
    time2 = time.time()
    return manualScores



def getSplitSize(redDimFeatures,split_sz):
    if split_sz == 1:
        print('Prime.')
        return
    elif not((len(redDimFeatures) % split_sz) == 0):
        getSplitSize(redDimFeatures,split_sz-1)
    else:
        return split_sz
    
def importDirect(directoryString):
    time1 = time.time()
    pathnames = []
    folders = []
    subfolders1 = []
    subfolders2 = []
    filenames_direct = []
    filenames_left = []
    scoresheets = []
    #count = 0
    for directories in os.listdir(directoryString):
        folder = os.fsdecode(directories)
        if folder[0:2] == 'R0':
            folders.append(folder)
        #Loop through each rat folder
        for folder in folders:
            if os.path.isdir(directoryString+'/'+folder):
                #while count < limit:
                    #count = count + 1
                    #Loop through each day of testing
                    for subfolder1 in os.listdir(directoryString+'/'+folder):
                        subfolder1 = os.fsdecode(subfolder1)
                        if ('score' in subfolder1) and (subfolder1.endswith('.csv')):
                            scorepath = directoryString+'/'+folder+'/'+subfolder1
                            if (os.path.isfile(scorepath)):
                                if len(scoresheets)>0:
                                    for i in scoresheets:
                                        if (not(i == scorepath)):
                                            scoresheets.append(scorepath)
                                else:
                                    scoresheets.append(scorepath)
                            if (os.path.isdir(directoryString+'/'+folder+'/'+subfolder1))and(not subfolder1.endswith('.fig')) and (not subfolder1.endswith('.pdf')) and (not 'temp' in subfolder1):
                                if '2017' in subfolder1 or '2018' in subfolder1:
                                    subfolders1.append(subfolder1)
                                    #print(subfolder1)
                                    for subfolder2 in os.listdir(directoryString+'/'+folder+'/'+subfolder1):
                                        subfolder2 = os.fsdecode(subfolder2)
                                        #print(subfolder2)
                                        #Loop through CSV files for direct view
                                        if ('direct' in subfolder2) and (os.path.isdir(directoryString+'/'+folder+'/'+subfolder1+'/'+subfolder2)):
                                            subfolders2.append(subfolder2)
                                            for file in os.listdir(directoryString+'/'+folder+'/'+subfolder1+'/'+subfolder2):
                                                filename_direct = os.fsdecode(file)
                                                if (folder in filename_direct) and (filename_direct.endswith('.csv')):
                                                    pathname_d = directoryString+'/'+folder+'/'+subfolder1+'/'+subfolder2+'/'+str(filename_direct)
                                                    if os.path.isfile(pathname_d):
                                                        pathnames.append(pathname_d)
                                            #filenames_direct.append(filename_direct)
                                            #print(filename_direct)                            
    time2 = time.time()
    print('importDirect runtime: %f' % (time2 - time1))
    return scoresheets, pathnames

def getInfo(pathname):
    time1 = time.time()
    rat = pathname[5:10]
    date1 = pathname[17:25]
    if (date1[4:5] == '0') and (date1[6:7] == '0'):
        date2 = date1[5:6]+'/'+date1[7:8]+'/'+date1[2:4]
    elif (not(date1[4:5] == '0')) and (date1[6:7] == '0'):
        date2 = date1[4:6]+'/'+date1[7:8]+'/'+date1[2:4]
    elif (date1[4:5] == '0') and (not(date1[6:7] == '0')):
        date2 = date1[5:6]+'/'+date1[6:8]+'/'+date1[2:4]
    else:
        date2 = date1[4:6]+'/'+date1[6:8]+'/'+date1[2:4]
    trialNum = pathname[74:77]
    trialNum = int(trialNum)
    time2 = time.time()
    #print('importLabels runtime: %f' % (time2 - time1))
    return rat, date1, date2, trialNum

def readDLC(pathname):
    time1 = time.time()
    #print("%s" % pathname)
    #pathname = bytes(pathname, "utf-8")
    #print(pathname)
    #pathname = pathname.decode("utf-8")
    #print(pathname)
    data = pd.read_csv(pathname,header=None)
    data = data.truncate(before=1,axis=1)
    data = data.truncate(before=3)
    data = data.values
    time2 = time.time()
    #print('readDLC runtime: %f' % (time2 - time1))
    return data

def normalize(featureArray):
    #Scale all coordinates by max pixel value
    maxPix = 551
    
    #Right now, this is also scaling probabilities... which is probably not great
    for a in featureArray:
        for b in a:
            sz = len(b)
            for c in range(sz-1):
                b[c] = float(b[c])/551
    return features

def distFromPellet(features):
    time1 = time.time() 
    #maxDist = np.sqrt( np.square(552/2) + np.square(552/2) )
    euclFeatures = list()
    frames = list()
    distances = list()
    a,b,c = np.shape(features)
    coord = 1
    for i in features:
        for j in i:
            if float(j[44]) > .8:
                xor = float(j[42])
                yor = float(j[43])
            else:
                xor = 0
                yor = 0
            for k in range(0,c,3):
                if coord == 1:
                    x = float(j[k])
                    y = float(j[k+1])
                    p = float(j[k+2])
                    coord = 0
                    if p > 0.8:
                        eucl = np.sqrt( np.square(x - xor) + np.square(y-yor) )
                        eucl = eucl#/maxDist
                        distances.append(eucl)
                        distances.append(p)
                    else:
                        x = 0
                        y = 0
                        eucl = np.sqrt( np.square(x - xor) + np.square(y-yor))
                        eucl = eucl#/maxDist
                        distances.append(eucl)
                        distances.append(p)
                else:
                    coord = 1
                coord = 1
            frames.append(distances)
            distances = list()
        euclFeatures.append(frames)
        frames = list()
    print(np.shape(euclFeatures))
    time2 = time.time()
    print('distFromPellet runtime is: %f' % (time2 - time1))
    return euclFeatures