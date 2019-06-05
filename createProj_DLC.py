# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 11:54:18 2019

@author: kkrista
"""
import os
import setDLCFunc
import deeplabcut
from PIL import Image

## Define User Input Variables

# Project variables
projName = 'left_grooming'
experimenter = 'Krista'
projDir = '/home/kkrista/Documents/Grooming/Krista/'
numRandVids = 15 # number of videos to train from
bodyParts = ['leftForepaw','rightForePaw','leftHindpaw','rightHindpaw','nose','tailBase']
vidDims = (1920, 1080)

# Video directory variables
subjDir = '/media/kkrista/KRISTAEHD/groomingDLC/' # Location of all animal files
foldID = 'et' # Identifier for all wanted folders (e.g., 'R' or 'et')
vidID = 'V' # Identifier for all wanted videos 

## Get all video files
vidList = setDLCFunc.fileFinder(subjDir,vidID)

## Create cropping parameters for all video files
[x1_all, x2_all, y1_all, y2_all] = setDLCFunc.getROI(vidList)

## Get randomly selected videos for training
trainFiles = setDLCFunc.randVidSel(vidList,numRandVids)

## Create the DLC project!
configPath = deeplabcut.create_new_project(projName,experimenter,trainFiles,working_directory=projDir,copy_videos=False)

## Edit configuration file with bodyParts and training video crop parameters
config = deeplabcut.utils.auxiliaryfunctions.read_config(configPath)

config['bodyparts'] = bodyParts

for vid in trainFiles:
    paramIdx = vidList.index(vid)
    params = [x1_all[paramIdx] + ', ' + x2_all[paramIdx] + ', ' + y1_all[paramIdx] + ', ' + y2_all[paramIdx]]
    config['video_sets'][vid]['crop'] = params[0]
    
deeplabcut.utils.auxiliaryfunctions.write_config(configPath,config)

## Extract frames for labeling
deeplabcut.extract_frames(configPath,'automatic','uniform',crop=True,userfeedback=False)

## Remove frames that are the same size as the original video
projPath = config['project_path']
pngList = setDLCFunc.fileFinder(projPath+'/labeled-data/','.png')
for img in pngList:
    im = Image.open(img)
    size = im.size
    
    if size[0] >= vidDims[0] and size[1] >= vidDims[1]:
        os.remove(img)
    else:
        continue
    

    



