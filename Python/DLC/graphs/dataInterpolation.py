#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 14:25:53 2019

@author: kkrista
"""

import os
import numpy as np
from scipy import fftpack

import funcs
import plots
import frameDict
frameDict = frameDict.frameDict

def makeInterpDicts(dirDLC,outDir,view='Center',fps=100):
    """
    Creates .pickle files for each training day
    """

    ## Get the behaviors (keys) from the frameDict
    behaviors = list(frameDict.keys())
    
    for item in behaviors:
        interpData[item] = {}
    
    ## Start looping through the keys in frameDict (abMovFrames and groom)
    for beh in behaviors:
        
        # Get the animals for this key
        animals = list(frameDict[beh].keys())
        
        # Start looping through the animals
        for mouse in animals:
    
            interpData[beh][mouse] = {}
            
            # Get all relevant dates for this mouse
            allDates = list(frameDict[beh][mouse].keys())
            
            # Start looping through relevant dates
            for day in allDates:
    
                interpData[beh][mouse][day] = {}
                
                # Get all relevant reaches
                reaches = list(frameDict[beh][mouse][day].keys())
                interpData[beh][mouse][day]['reaches']=reaches
                # Get all files in DLC directory for this mouse
                allFiles = os.listdir(dirDLC + mouse + '/DLC/')
                
                # Start processing one reach at a time
                for reach in reaches:
                    
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
                    
                    # Get the start and stop frames for this reach
                    frame1 = frameDict[beh][mouse][day][reach][0]
                    frame2 = frameDict[beh][mouse][day][reach][1]
                    
                    if frame2 > len(leftPaw):
                        frame2 = len(leftPaw)
                        
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
                    
                    # Mask data
                    xLeft_masked, yLeft_masked, pLeft_masked = funcs.maskData(leftPaw)
                    xRight_masked, yRight_masked, pRight_masked = funcs.maskData(rightPaw)
                    xNose_masked, yNose_masked, pNose_masked = funcs.maskData(nose)
                    
                    EDLeftMask = [any(tup) for tup in zip(xLeft_masked.mask,xNose_masked.mask)]
                    EDRightMask = [any(tup) for tup in zip(xRight_masked.mask,xNose_masked.mask)]
                    edLeft_masked = np.ma.masked_array(data=ED_Left,mask=EDLeftMask)
                    edRight_masked = np.ma.masked_array(data=ED_Right,mask=EDRightMask)
                    
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