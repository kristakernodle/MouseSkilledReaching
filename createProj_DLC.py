# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 11:54:18 2019

@author: kkrista
"""

import os
import deeplabcut

## Define User Input Variables
subDir = '/media/kkrista/KRISTAEHD/groomingDLC/' # Location of all animal files
foldID = 'et' # Identifier for all wanted folders (e.g., 'R' or 'et')
vidID = 'V' # Identifier for all wanted videos 

## Script defined variables
mp4=[]

## get all video files
for path, subdirs, files in os.walk(subDir):
    for name in files: 
        if vidID in name:
            mp4.append(name)
        else:
            continue

