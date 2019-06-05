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
    
    #np.savetxt(wrkDir+"/trainFiles.csv",trainFiles,delimiter=",",fmt='%s')

    return trainFiles
    
def getROI(locVidDir,docVidDir,wrkDir,trainFcsv):
    cropParamDir=wrkDir+"/cropParameters.txt"
    train=[]
    g=[]
    h=[]
    origVids = []
    a=[]
    compName=[]
    
    cropParamFile=Path(cropParamDir)
    if cropParamFile.is_file():
        f=readfile(cropParamDir)            
        writeIt = open(cropParamDir,'w')
    else:
        writeIt = open(cropParamDir,'w+')
    
    ff=readfile(wrkDir+"/trainFiles.csv")
    
    cc=0
    while cc < len(ff):
        train.append(docVidDir+ff[cc])
        cc+=1
        
    os.chdir(locVidDir)
    fullfiles = os.listdir()
            
    ii = 0
    while ii < len(fullfiles):
        docVidPath = docVidDir + fullfiles[ii]
        locVidPath = locVidDir + fullfiles[ii]
    
        #if compName[ii] not in origVids:
        #origVids.append(compName[ii])
            
        vidcap = cv2.VideoCapture(locVidPath)
        success, image = vidcap.read()
        small = cv2.resize(image,(0,0),fx=0.5,fy=0.5)
            
        r = cv2.selectROI(small)
        r = np.array(r)
        r = 2*r

        x1 = str(r[0])
        x2 = str(r[0]+r[2])
        y1 = str(r[1])
        y2 = str(r[1]+r[3])

        writeIt.write("%s\n" % docVidPath)
        writeIt.write("%s, %s, %s, %s\n" %(x1,x2,y1,y2))
        
        #else:
            #writeIt.write("%s:\n" % docVidPath)
            #writeIt.write("crop: %s, %s, %s, %s\n" %(x1,x2,y1,y2))
        
        ii += 1

    writeIt.close()

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
