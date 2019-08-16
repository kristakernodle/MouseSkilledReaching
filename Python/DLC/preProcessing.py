#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 13:08:38 2019

@author: kkrista
"""

# DLC Pre-Processing
# Thoughts: 
# 1. Plot all p-values and try to identify, in the various views, what my pval cut offs should be. 
    # I will likely have a couple of different tiers (one FOR SURE and one 'maybe') -- The 'maybe'
    # class will need further processing
# 2. Develop and implement an algorithm assessing if a  point jumped very far 
    # between two frames. If so, remove the offending point
# 3. Try some filtering of the data to clean it up and make it more obvious
    
import funcs
import matplotlib.pyplot as plt
import numpy as np


## For now, processing on 710 only
dirDLC = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/et710/DLC/'

filename = '710_20181126/710_20181126_01_R24DeepCut_resnet50_rightPP_CenterFeb9shuffle1_1030000.csv'

## Read in file
[leftPaw, rightPaw, nose, pellet] = funcs.readDLC(dirDLC + filename)

distance = []
for index in range(1,len(leftPaw)):
    distance.append(funcs.ptDist(leftPaw[index],leftPaw[index-1]))

leftPaw = np.ma.array(leftPaw)
rightPaw = np.ma.array(rightPaw)
nose = np.ma.array(nose)
pellet = np.ma.array(pellet)

distLeftPaw_masked = np.ma.array(distance)

## Mask where p-values are less than 0.60 -- This is a highly confident interval

frames = list(range(1,len(leftPaw)+1))
frames = np.ma.array(frames)




for pval in list(funcs.frange(0.6,0.95,0.05)):
    leftPaw_masked = np.ma.masked_where(leftPaw < pval,leftPaw)
    distLeftPaw_masked.mask = leftPaw_masked.mask[1:,-1]
    
    fig, (ax1,ax2) = plt.subplots(2,1,sharex=True)
    ax1.scatter(frames,leftPaw_masked[:,-1])
    ax1.set(ylabel='p value', title='Points when ThreshP = ' + str(pval))
    ax1.set_xlim(0, 950)
    ax2.scatter(frames[1:],distLeftPaw_masked)
    ax2.set(xlabel='Frame Number',ylabel='euclidean distance in pixels', title='Euclidean Distance when ThreshP = ' + str(pval))
    ax2.set_xlim(0, 950)
    fig.tight_layout()
    fig.savefig('/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/et710/findThresholds_'+ str(pval) + '.pdf')
    plt.close()







#distLeftPaw_masked2 = np.ma.masked_where(distLeftPaw_masked > 40, distLeftPaw_masked)
#
#frames = list(range(1,len(leftPaw_masked)+1))
#
#plt.scatter(frames[1:],distLeftPaw_masked)
#
##plt.scatter(frames,leftPaw_masked[:,2])
##plt.yticks(np.arange(0,1,step=0.05))
#plt.show()
    