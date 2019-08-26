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
    
import os
import funcs
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

### For now, processing on 710 only
dirDLC = '/Users/Krista/Desktop/et710/'

folder = '710_20181107'

allFiles = os.listdir(dirDLC + folder)
csvFiles = []
for file in allFiles:
    if 'Center' not in file:
        continue
    elif not file.endswith('.csv'):
        continue
    else:
        csvFiles.append(file)

for file in csvFiles:

    if '01_R37' not in file:
        continue
    oframe1 = 700
    oframe2 = 800
    
    frame1 = oframe1
    frame2 = oframe2
    frameDiff = frame2-frame1
    
    while frameDiff < 300:
        frame1 = frame1 - 10
        frame2 = frame2 + 10
        frameDiff = frame2-frame1
        
    print(file)
    
    distanceLeft = []
    distanceRight = []
    
    # Read in file
    [leftPaw, rightPaw, nose, pellet] = funcs.readDLC(dirDLC + folder + '/' + file)

    for index in range(1,len(leftPaw)):
        distanceLeft.append(funcs.ptDist(leftPaw[index],leftPaw[index-1]))
    for index in range(1,len(rightPaw)):
        distanceRight.append(funcs.ptDist(rightPaw[index],rightPaw[index-1]))
        
    leftPaw = np.ma.array(leftPaw)
    rightPaw = np.ma.array(rightPaw)
    nose = np.ma.array(nose)
    pellet = np.ma.array(pellet)
    
    pLeftPaw_masked = np.ma.masked_where(leftPaw[:,-1] < 0.75, leftPaw[:,2])
    xLeftPaw_masked = np.ma.masked_where(leftPaw[:,-1]  < 0.75,leftPaw[:,0])
    yLeftPaw_masked = np.ma.masked_where(leftPaw[:,-1] < 0.75,leftPaw[:,1])
    
    pRightPaw_masked = np.ma.masked_where(rightPaw[:,-1] < 0.75,rightPaw[:,2])
    xRightPaw_masked = np.ma.masked_where(rightPaw[:,-1] < 0.75,rightPaw[:,0])
    yRightPaw_masked = np.ma.masked_where(rightPaw[:,-1] < 0.75,rightPaw[:,1])
    
    dLeftRem = []
    dRightRem = []
    
    for dist in distanceLeft:
        if dist > 30:
            dLeftRem.append(distanceLeft.index(dist))
    for dist in distanceRight:
        if dist > 30:
            dRightRem.append(distanceRight.index(dist))
            
    distanceLeft = np.ma.array(distanceLeft)
    distanceRight = np.ma.array(distanceRight)
    
    distanceLeft.mask = pLeftPaw_masked.mask[1:-1]
    distanceRight.mask = pRightPaw_masked.mask[1:-1]
    
    for item in dLeftRem:
        distanceLeft.mask[item] = True
    for item in dRightRem:
        distanceRight.mask[item] = True
    
    fps = 59.94
    x = list(range(1,len(xLeftPaw_masked)+1)) 
    x = [i/fps for i in x]
    xL_masked = np.ma.array(x)
    xR_masked = np.ma.array(x)
    
    xL_masked.mask = xLeftPaw_masked.mask
    xR_masked.mask = xRightPaw_masked.mask
    
    xLeftPaw_compressed = xLeftPaw_masked.compressed()
    xRightPaw_compressed = xRightPaw_masked.compressed()
    xL_compressed = xL_masked.compressed()
    xR_compressed = xR_masked.compressed()
    
    xLnew = np.linspace(xL_compressed[0],xL_compressed[-1],num = len(x), endpoint=True)
    fL = interp1d(xL_compressed,xLeftPaw_compressed,kind = 'cubic')
    yLnew = fL(xLnew)
    
    xRnew = np.linspace(xR_compressed[0],xR_compressed[-1],num = len(x), endpoint=True)
    fR = interp1d(xR_compressed,xRightPaw_compressed,kind = 'cubic')
    yRnew = fR(xRnew)
    
    fig, (ax1,ax2) = plt.subplots(2,1,sharex=False)
    
    ax1.plot(x[frame1:frame2],xLeftPaw_masked[frame1:frame2],'o',label='Original Data')
    ax1.plot(xLnew[frame1:frame2],yLnew[frame1:frame2],'-',label='Cubic 1D Interpolation')
    ax1.axvspan(oframe1/fps, oframe2/fps, facecolor='#d7f4d7', alpha=0.5)

    ax2.plot(x[frame1:frame2],xRightPaw_masked[frame1:frame2],'o',label='Original Data')
    ax2.plot(xRnew[frame1:frame2],yRnew[frame1:frame2],'-',label='Cubic 1D Interpolation')
    ax2.axvspan(oframe1/fps, oframe2/fps, facecolor='#d7f4d7', alpha=0.5)
    fig.tight_layout()
    fig.savefig(dirDLC + folder + '/' + file[:-3] + 'pdf')
    print('Next File')
    plt.close()




  

#fig, ((axLx,axLy,axLd),(axRx,axRy,axRd)) = plt.subplots(2,3,sharex='row',sharey=False)
#axLx.scatter(x,xLeftPaw_masked)
#axLy.scatter(x,yLeftPaw_masked)
#axLd.scatter(x[1:],distanceLeft)
#axRx.scatter(x,xRightPaw_masked)
#axRy.scatter(x,yRightPaw_masked)
#axRd.scatter(x[1:],distanceRight)
#fig.tight_layout()



    