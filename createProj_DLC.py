# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 11:54:18 2019

@author: kkrista
"""

import os
import setDLCFunc
import deeplabcut

## Define User Input Variables

# Project variables
projName = 'left_groomingIso'
experimenter = 'Krista'
projDir = '/home/kkrista/Documents/Grooming/Krista/'
numRandVids = 20 # number of videos to train from
bodyParts = ['leftForepaw','rightForePaw','leftHindpaw','rightHindpaw','nose','tailBase']

# Video directory variables
subjDir = '/media/kkrista/KRISTAEHD/groomingDLC/' # Location of all animal files
foldID = 'et' # Identifier for all wanted folders (e.g., 'R' or 'et')
vidID = 'V' # Identifier for all wanted videos 


## Script defined variables
vidList=[]

## Get all video files
for path, subdirs, files in os.walk(subjDir):
    for name in files: 
        if vidID in name:
            vidList.append(path+'/'+name)
        else:
            continue

## Create cropping parameters for all video files
[x1, x2, y1, y2] = setDLCFunc.getROI(vidList)

## Get randomly selected videos for training
trainFiles = setDLCFunc.randVidSel(vidList,numRandVids)

## Create the DLC project!
configPath = deeplabcut.create_new_project(projName,experimenter,trainFiles,working_directory=projDir,copy_videos=False)



