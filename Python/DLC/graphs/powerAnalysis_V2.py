#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 09:14:28 2019

@author: kkrista
"""

# =============================================================================
# Power Analysis for New DLC Iteration (10/15/2019)
# =============================================================================

import os
import pickle
import numpy as np
from scipy import fftpack

import funcs
import frameDict
frameDict = frameDict.frameDict

dirDLC = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/DLCProcessing/currentDLCIter/'

view = 'Center'
plotting = False
averages = False

fs = 100
firstPass = 0

xPixRange = []
yPixRange = []
EDPixRange = []

fftData = {}
interpData = {}
 
frameDist = []

## Get the behaviors (keys) from the frameDict
behaviors = list(frameDict.keys())

for item in behaviors:
    fftData[item] = {}
    interpData[item] = {}

## Start looping through the keys in frameDict (abMovFrames and groom)
for beh in behaviors:
    
    if averages == True:
        mean_leftPaw_freq = []
        mean_leftPaw_fft = []
        mean_rightPaw_freq = []
        mean_rightPaw_fft = []
        mean_nose_freq = []
        mean_nose_fft = []
        mean_EDLeft_fft = []
        mean_EDRight_fft = []
    
    # Get the animals for this key
    animals = list(frameDict[beh].keys())
    
    # Start looping through the animals
    for mouse in animals:

        fftData[beh][mouse] = {}
        interpData[beh][mouse] = {}
        
        # Get all relevant dates for this mouse
        allDates = list(frameDict[beh][mouse].keys())
        
        # Start looping through relevant dates
        for day in allDates:

            fftData[beh][mouse][day] = {}
            interpData[beh][mouse][day] = {}
            
            # Get all relevant reaches
            reaches = list(frameDict[beh][mouse][day].keys())
            fftData[beh][mouse][day]['reaches']=reaches
            interpData[beh][mouse][day]['reaches']=reaches
            # Get all files in DLC directory for this mouse
            allFiles = os.listdir(dirDLC + mouse + '/DLC/')
            
            # Start processing one reach at a time
            for reach in reaches:
                
                fftData[beh][mouse][day][reach] = {}
                interpData[beh][mouse][day][reach] = {}
                
                allcsvFiles = []
                
                # Get the relevant reach file
                for file in allFiles:
                    if file.endswith('.csv'):
                        allcsvFiles.append(file)
                
                for file in allcsvFiles:
                    if view not in file or reach not in file:
                        continue
                    else:
                        csvFile = file
                        break
                    
                # Read in file
                [leftPaw, rightPaw, nose, pellet] = funcs.readDLC(dirDLC + mouse + '/DLC/' + csvFile)
                
                interpData[beh][mouse][day][reach]['dlcData'] = {}
                interpData[beh][mouse][day][reach]['dlcData']['leftPaw'] = leftPaw
                interpData[beh][mouse][day][reach]['dlcData']['rightPaw'] = rightPaw
                interpData[beh][mouse][day][reach]['dlcData']['nose'] = nose
                interpData[beh][mouse][day][reach]['dlcData']['pellet'] = pellet
                
                # Get the start and stop frames for this reach
                frame1 = frameDict[beh][mouse][day][reach][0]
                frame2 = frameDict[beh][mouse][day][reach][1]
                
                frameDist.append(frame2-frame1)
                
                if frame2 > len(leftPaw):
                    frame2 = len(leftPaw)
                    
#                # Based on previous run of max(frameDist), adjust frame1 and frame2 to have the same number of frames
#                if frame2-frame1 < 300:
#                        
#                    
#                    while frame2 < len(leftPaw) and frame1 > 0:
#                        frame1 -= 1
#                        frame2 += 1
                
                # Cut to relevant frames
                leftPaw = leftPaw[frame1:frame2]
                rightPaw = rightPaw[frame1:frame2]
                nose = nose[frame1:frame2]
                    
                print('beginning analysis on: ' + day + ', reach: ' + reach)
                
# =============================================================================
#                 File and information is set up for beginning analysis
# =============================================================================
                
                # Calculate Euclidean Distance
                ED_Left = []
                ED_Right = []
                index = 0
                for item in nose:
                    ED_Left.append(funcs.ptDist(leftPaw[index][0:2],item[0:2]))
                    ED_Right.append(funcs.ptDist(rightPaw[index][0:2],item[0:2]))
                    index += 1
                interpData[beh][mouse][day][reach]['rawData'] = {}
                interpData[beh][mouse][day][reach]['rawData']['leftPaw'] = leftPaw
                interpData[beh][mouse][day][reach]['rawData']['rightPaw'] = rightPaw
                interpData[beh][mouse][day][reach]['rawData']['nose'] = nose
                interpData[beh][mouse][day][reach]['rawData']['ED_Left'] = ED_Left
                interpData[beh][mouse][day][reach]['rawData']['ED_Right'] = ED_Right
                
                # Mask data
                xLeft_masked, yLeft_masked, pLeft_masked = funcs.maskData(leftPaw)
                xRight_masked, yRight_masked, pRight_masked = funcs.maskData(rightPaw)
                xNose_masked, yNose_masked, pNose_masked = funcs.maskData(nose)
                
                EDLeftMask = [any(tup) for tup in zip(xLeft_masked.mask,xNose_masked.mask)]
                EDRightMask = [any(tup) for tup in zip(xRight_masked.mask,xNose_masked.mask)]
                edLeft_masked = np.ma.masked_array(data=ED_Left,mask=EDLeftMask)
                edRight_masked = np.ma.masked_array(data=ED_Right,mask=EDRightMask)
                
                interpData[beh][mouse][day][reach]['maskedData'] = {}
                interpData[beh][mouse][day][reach]['maskedData']['leftPaw'] = {}
                interpData[beh][mouse][day][reach]['maskedData']['rightPaw'] = {}
                interpData[beh][mouse][day][reach]['maskedData']['nose'] = {}
                
                interpData[beh][mouse][day][reach]['maskedData']['leftPaw']['x'] = xLeft_masked
                interpData[beh][mouse][day][reach]['maskedData']['leftPaw']['y'] = yLeft_masked
                interpData[beh][mouse][day][reach]['maskedData']['rightPaw']['x'] = xRight_masked
                interpData[beh][mouse][day][reach]['maskedData']['rightPaw']['y'] = yRight_masked
                interpData[beh][mouse][day][reach]['maskedData']['nose']['x'] = xNose_masked
                interpData[beh][mouse][day][reach]['maskedData']['nose']['y'] = yNose_masked
                
                interpData[beh][mouse][day][reach]['maskedData']['ED_Left'] = edLeft_masked
                interpData[beh][mouse][day][reach]['maskedData']['ED_Right'] = edRight_masked
                
                # Begin Interpolation
                x = list(range(frame1,frame2))
                x = [i/fs for i in x]
                
                try: 
                    tsXLeftPaw_inter, xLeft_inter = funcs.interpolData(x,xLeft_masked)
                    tsYLeftPaw_inter, yLeft_inter = funcs.interpolData(x,yLeft_masked)
                    
                    tsXRightPaw_inter, xRight_inter = funcs.interpolData(x,xRight_masked)
                    tsYRightPaw_inter, yRight_inter = funcs.interpolData(x,yRight_masked)
                    
                    tsXNose_inter, xNose_inter = funcs.interpolData(x,xNose_masked)
                    tsYNose_inter, yNose_inter = funcs.interpolData(x,yNose_masked)
                    
                    tsEDLeft_inter, EDLeft_inter = funcs.interpolData(x,edLeft_masked)
                    tsEDRight_inter, EDRight_inter = funcs.interpolData(x,edRight_masked)
    
                    interLeftPaw = list(zip(xLeft_inter,yLeft_inter))
                    interRightPaw = list(zip(xRight_inter,yRight_inter))
                    interNose = list(zip(xNose_inter,yNose_inter))
                    interEDLeft = list(zip(tsEDLeft_inter,EDLeft_inter))
                    interEDRight = list(zip(tsEDRight_inter,EDRight_inter))
                    
                except:
                    print('This data is missing something')
                    continue

                interpData[beh][mouse][day][reach]['interpData'] = {}
                interpData[beh][mouse][day][reach]['interpData']['leftPaw'] = interLeftPaw
                interpData[beh][mouse][day][reach]['interpData']['rightPaw'] = interRightPaw
                interpData[beh][mouse][day][reach]['interpData']['nose'] = interNose
                interpData[beh][mouse][day][reach]['interpData']['ED_Left'] = interEDLeft
                interpData[beh][mouse][day][reach]['interpData']['ED_Right'] = interEDRight

                # Perform FFT
                leftPaw_fft = fftpack.fft2(interLeftPaw)
                
                rightPaw_fft = fftpack.fft2(interRightPaw)
                
                nose_fft = fftpack.fft2(interNose)
                
                EDLeft_fft = fftpack.fft2(interEDLeft)
                EDRight_fft = fftpack.fft2(interEDRight)
                
                N = len(leftPaw_fft)
                
                leftPaw_freq = fftpack.fftfreq(N,d=0.01)
                rightPaw_freq = fftpack.fftfreq(N,d=0.01)
                nose_freq = fftpack.fftfreq(N,d=0.01)
                EDLeft_freq = fftpack.fftfreq(N,d=0.01)
                EDRight_freq = fftpack.fftfreq(N,d=0.01)
                        
                ## Save values into dictionary for later mean calculations
                fftData[beh][mouse][day][reach]['leftPaw_freq'] = np.abs(leftPaw_freq[:N // 2])
                fftData[beh][mouse][day][reach]['leftPaw_fft'] = np.abs(leftPaw_fft[:N // 2])
                fftData[beh][mouse][day][reach]['rightPaw_freq'] = np.abs(rightPaw_freq[:N // 2])
                fftData[beh][mouse][day][reach]['rightPaw_fft'] = np.abs(rightPaw_fft[:N // 2])
                fftData[beh][mouse][day][reach]['nose_freq'] = np.abs(nose_freq[:N // 2])
                fftData[beh][mouse][day][reach]['nose_fft'] = np.abs(nose_fft[:N // 2])
                fftData[beh][mouse][day][reach]['EDLeft_fft'] = np.abs(EDLeft_fft[:N // 2])
                fftData[beh][mouse][day][reach]['EDRight_fft'] = np.abs(EDRight_fft[:N // 2])
                
                ## Save into the mean
                if firstPass == 0:
                    mean_leftPaw_freq = np.abs(leftPaw_freq[:N // 2])
                    mean_leftPaw_fft = np.abs(leftPaw_fft[:N // 2])
                    mean_rightPaw_freq = np.abs(rightPaw_freq[:N // 2])
                    mean_rightPaw_fft = np.abs(rightPaw_fft[:N // 2])
                    mean_nose_freq = np.abs(nose_freq[:N // 2])
                    mean_nose_fft = np.abs(nose_fft[:N // 2])
                    mean_EDLeft_fft = np.abs(EDLeft_fft[:N // 2])
                    mean_EDRight_fft = np.abs(EDRight_fft[:N // 2])
                    mean_EDLeft_freq = np.abs(EDLeft_freq[:N // 2])
                    mean_EDRight_freq = np.abs(EDRight_freq[:N // 2])
                else:
                    
                    for freq in np.abs(leftPaw_freq[:N // 2]):
                        try:
                            index = mean_leftPaw_freq[freq]
                            mean_leftPaw_fft[index] = (mean_leftPaw_fft[index] + freq)/2
                        except:
                            mean_leftPaw_fft.append(np.abs(leftPaw_freq.index(freq)))
                            mean_leftPaw_freq.append(freq)
 
                    for freq in np.abs(rightPaw_freq[:N // 2]):
                        try:
                            index = mean_rightPaw_freq[freq]
                            mean_rightPaw_fft[index] = (mean_rightPaw_fft[index] + freq)/2
                        except:
                            mean_rightPaw_fft.append(np.abs(rightPaw_freq.index(freq)))
                            mean_rightPaw_freq.append(freq)
                            
                    for freq in np.abs(nose_freq[:N // 2]):
                        try:
                            index = mean_nose_freq[freq]
                            mean_nose_fft[index] = (mean_nose_fft[index] + freq)/2
                        except:
                            mean_nose_fft.append(np.abs(nose_freq.index(freq)))
                            mean_nose_freq.append(freq)
                    
                    for freq in np.abs(EDLeft_freq[:N // 2]):
                        try:
                            index = mean_EDLeft_freq[freq]
                            mean_EDLeft_fft[index] = (mean_EDLeft_fft[index] + freq)/2
                        except:
                            mean_EDLeft_fft.append(np.abs(EDLeft_freq.index(freq)))
                            mean_EDLeft_freq.append(freq)
                            
                    for freq in np.abs(EDRight_freq[:N // 2]):
                        try:
                            index = mean_EDRight_freq[freq]
                            mean_EDRight_fft[index] = (mean_EDRight_fft[index] + freq)/2
                        except:
                            mean_EDRight_fft.append(np.abs(EDRight_freq.index(freq)))
                            mean_EDRight_freq.append(freq)
                
# =============================================================================
# I now have fftData and interpData dictionaries to work from
# =============================================================================
                            
# Save these dictionaries for future use
with open(dirDLC + 'combined_allData.pickle','wb+') as pickleFile:
    pickle.dump(interpData, pickleFile, protocol=pickle.HIGHEST_PROTOCOL)   

with open(dirDLC + 'combined_fftData.pickle','wb+') as pickleFile:
    pickle.dump(fftData, pickleFile, protocol=pickle.HIGHEST_PROTOCOL)                        


                    
                
                    
                
                
                
                
                
                
                
                
                

