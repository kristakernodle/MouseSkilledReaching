#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 15:57:44 2019

@author: kkrista
"""
import os
import random
import numpy as np
import cv2
# from pathlib import Path

def readfile(F):
    with open(F) as f:
        return f.read().splitlines()
    
def randVidSel(vidList,numVids):
    trainFiles = []
    maxNum = len(vidList)
    if maxNum >= numVids:
        vidInd = random.sample(range(0,maxNum),numVids)
    else:
        raise ValueError("numVids should be less than "+str(maxNum))
    
    for num in vidInd:
        trainFiles.append(vidList[num])

    return trainFiles
    
def getROI(vidList):
    
    # Initialize output variables
    x1_all = []
    x2_all = []
    y1_all = []
    y2_all = []
    
    for vid in vidList:
        vidcap = cv2.VideoCapture(vid)
        success, image = vidcap.read()
        small = cv2.resize(image,(0,0),fx=0.5,fy=0.5)
            
        r = cv2.selectROI(small)
        r = np.array(r)
        r = 2*r

        x1_all.append(str(r[0]))
        x2_all.append(str(r[0]+r[2]))
        y1_all.append(str(r[1]))
        y2_all.append(str(r[1]+r[3]))
        

    return [x1_all, x2_all, y1_all, y2_all]

def multiNet(projName,locVidDir,docVidDir):
    file=readfile('/home/kkrista/Documents/Script/dlcVar.txt')
    projNameInd=file.index("# Variables")+2
    locVidDirInd=projNameInd+3
    docVidDirInd=locVidDirInd+1
    
    writeFile=open('/home/kkrista/Documents/Script/dlcVar.txt','w')
    
    for line in file[0:projNameInd]:
        writeFile.write('%s\n' %line)
    writeFile.write('projName="%s"\n' %projName)
    for line in file[projNameInd+1:locVidDirInd]:
        writeFile.write('%s\n' %line)
    writeFile.write('locVidDir="%s"\n' %locVidDir)
    writeFile.write('docVidDir="%s"\n' %docVidDir)
    for line in file[docVidDirInd+1:]:
        writeFile.write('%s\n' %line)
        
    writeFile.close()
