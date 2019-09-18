# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 08:58:50 2019

@author: krista kernodle
"""

# =============================================================================
# The purpose of this file is to set up a script that allows for power spectral
# density calculations on my data. I'm using a variety of functions from the funcs
# file as well as my frameDict file to pull in the appropriate frame sets for analysis.
# 
# Right now, the analysis is entirely focused on comparing the grooming bouts to 
# the abnormal movement bouts.
# =============================================================================

import os
import funcs
import frameDict
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma

dirDLC = 'X:/Neuro-Leventhal/data/mouseSkilledReaching/'
outDir = 'X:/Neuro-Leventhal/data/mouseSkilledReaching/DLCProcessing/powerAnalysis/cubicInterpol/hpFilt_1-5/'
fps = 100
fs = fps


## Begin searching through all files, starting with animal folders
animals = list(frameDict.groom.keys())

for animal in animals:
    folders = list(frameDict.groom[animal].keys())

    ## Begin searching through animal's subdirectories, looking for DLC folders
    for folder in folders:
        
        allFiles = os.listdir(dirDLC + animal + '/DLC/' + folder)
        csvFiles = []
        
        ## Check for 'Center' in filename (direct view only analysis)
        for file in allFiles:
            
            if 'Center' not in file:
                continue
            elif not file.endswith('.csv'):
                continue
            else:
                csvFiles.append(file)
        
        reaches = list(frameDict.groom[animal][folder].keys())
        
        ## Begin searching through all of the reaches for the ones of interest
        for reach in reaches:

            
            # Check to see if reach is one of interest
            for file in csvFiles:
            
                if reach not in file:
                    continue
                
                print('beginning analysis on: ' + file)
                
                ## Pull in the behavior of interest frame numbers
                frame1 = frameDict.groom[animal][folder][reach][0]
                frame2 = frameDict.groom[animal][folder][reach][1]
                
                ## Define lists that will be filled later
                leftPawX = []
                leftPawY = []
                
                distanceLeft = []
                distanceRight = []
                distanceNose = []
                euclidDistLeft = []
                euclidDistRight = []
                
                # Read in file
                [leftPaw, rightPaw, nose, pellet] = funcs.readDLC(dirDLC + animal + '/DLC/' + folder + '/' + file)
            
                if frame2 > len(leftPaw):
                    frame2 = len(leftPaw)
                    
                # Cut down the read in files to be just the areas of interest
                leftPaw = leftPaw[frame1:frame2]
                rightPaw = rightPaw[frame1:frame2]
                nose = nose[frame1:frame2]
                pellet = pellet[frame1:frame2]
                
                # Calculate distances (distanceLeft/Right/Nose is between frames for same bodypart, euclidDistLeft/Right is between nose and paw)
                for index in range(1,len(leftPaw)):
                    distanceLeft.append(funcs.ptDist(leftPaw[index],leftPaw[index-1]))
                    distanceRight.append(funcs.ptDist(rightPaw[index],rightPaw[index-1]))
                    distanceNose.append(funcs.ptDist(nose[index],nose[index-1]))
                for index in range(0,len(nose)):
                    euclidDistLeft.append(funcs.ptDist(leftPaw[index],nose[index]))
                    euclidDistRight.append(funcs.ptDist(rightPaw[index],nose[index]))
                    
                # Convert things into numpy masked arrays and trim to desired frames only
                leftPaw = np.ma.array(leftPaw)
                rightPaw = np.ma.array(rightPaw)
                nose = np.ma.array(nose)
                pellet = np.ma.array(pellet)
                euclidDistLeft = np.ma.array(euclidDistLeft)
                euclidDistRight = np.ma.array(euclidDistRight)
                
                noseMask = nose[:,-1] < 0.75
                noseMask = noseMask.data
                
                # Define x,y,and p values for body parts with mask based on p value
                pLeftPaw_masked = np.ma.masked_where(leftPaw[:,-1] < 0.75, leftPaw[:,2])
                xLeftPaw_masked = np.ma.masked_where(leftPaw[:,-1]  < 0.75,leftPaw[:,0])
                yLeftPaw_masked = np.ma.masked_where(leftPaw[:,-1] < 0.75,leftPaw[:,1])
#                euclidDistLeft_masked = np.ma.masked_where(nose[:,-1] < 0.75,euclidDistLeft)
                
                pRightPaw_masked = np.ma.masked_where(rightPaw[:,-1] < 0.75,rightPaw[:,2])
                xRightPaw_masked = np.ma.masked_where(rightPaw[:,-1] < 0.75,rightPaw[:,0])
                yRightPaw_masked = np.ma.masked_where(rightPaw[:,-1] < 0.75,rightPaw[:,1])
#                euclidDistRight_masked = np.ma.masked_where(nose[:,-1] < 0.75,euclidDistRight)
                
                euclidDistRight_masked = euclidDistRight
                euclidDistRight_masked.mask = noseMask
                
                euclidDistLeft_masked = euclidDistLeft
                euclidDistLeft_masked.mask = noseMask
                
                ## Make masked based on whether a point jumped significanntly (defined as greater than 50 pxls here)
                dLeftRem = []
                dRightRem = []
                dNoseRem = []
                
                for dist in distanceLeft:
                    if dist > 50:
                        dLeftRem.append(distanceLeft.index(dist))
                for dist in distanceRight:
                    if dist > 50:
                        dRightRem.append(distanceRight.index(dist))
                for dist in distanceNose:
                    if dist > 50:
                        dNoseRem.append(distanceNose.index(dist))
                        
                distanceLeft = np.ma.array(distanceLeft)
                distanceRight = np.ma.array(distanceRight)
                distanceNose = np.ma.array(distanceNose)
                
                distanceLeft.mask = pLeftPaw_masked.mask[1:-1]
                distanceRight.mask = pRightPaw_masked.mask[1:-1]
                
                for item in dNoseRem:
                    euclidDistRight_masked.mask[item] = True
                    euclidDistLeft_masked.mask[item] = True
                for item in dLeftRem:
                    distanceLeft.mask[item] = True
                for item in dRightRem:
                    distanceRight.mask[item] = True
                    
                print('this is our dataset')
                
                ## Begin creating interpolated datasets using function
                x = list(range(frame1,frame2))
                x = [i/fps for i in x]
                xD = x[1:]
                
                tsXLeftPaw_inter, xLeftPaw_inter = funcs.interpolData(x,xLeftPaw_masked)
                tsXRightPaw_inter, xRightPaw_inter = funcs.interpolData(x,xRightPaw_masked)
                
                tsYLeftPaw_inter, yLeftPaw_inter = funcs.interpolData(x,yLeftPaw_masked)
                tsYRightPaw_inter, yRightPaw_inter = funcs.interpolData(x,yRightPaw_masked)
                
                tsDLeftPaw_inter, xDLeftPaw_inter = funcs.interpolData(xD,distanceLeft)
                tsDRightPaw_inter, xDRightPaw_inter = funcs.interpolData(xD,distanceRight)
                
                ## Apply filter to interpolated data
                xLeftPaw_interFilt = funcs.filterFunc(xLeftPaw_inter)
                yLeftPaw_interFilt = funcs.filterFunc(yLeftPaw_inter)
                
                xRightPaw_interFilt = funcs.filterFunc(xRightPaw_inter)
                yRightPaw_interFilt = funcs.filterFunc(yRightPaw_inter)
                
                xDLeftPaw_interFilt = funcs.filterFunc(xDLeftPaw_inter)
                xDRightPaw_interFilt = funcs.filterFunc(xDRightPaw_inter)
                
                ## Begin PSD analysis
                xLP_freq, xLP_pS = signal.periodogram(xLeftPaw_interFilt,fs)
                yLP_freq, yLP_pS = signal.periodogram(yLeftPaw_interFilt,fs)
                
                xRP_freq, xRP_pS = signal.periodogram(xRightPaw_interFilt,fs)
                yRP_freq, yRP_pS = signal.periodogram(yRightPaw_interFilt,fs)
                
                xDL_freq, xDL_pS = signal.periodogram(xDLeftPaw_interFilt,fs)
                xDR_freq, xDR_pS = signal.periodogram(xDRightPaw_interFilt,fs)
                
                ## Begin Plotting
                fig = plt.figure()
                ax1 = fig.add_subplot(321)
                ax2 = fig.add_subplot(322)
                ax3 = fig.add_subplot(323)
                
                ax4 = fig.add_subplot(324)
                ax5 = fig.add_subplot(325)
                ax6 = fig.add_subplot(326)
                
                ax1.plot(xLP_freq,xLP_pS)
                ax1.set_title('Left Paw, x-values', size = 8)
                
                ax2.plot(yLP_freq,yLP_pS)
                ax2.set_title('Left Paw, y-values', size = 8)
                
                ax3.plot(xRP_freq,xRP_pS)
                ax3.set_title('Right Paw, x-values', size = 8)
                
                ax4.plot(xRP_freq,xRP_pS)
                ax4.set_title('Right Paw, y-values', size = 8)
                
                ax5.plot(xDL_freq,xDL_pS)
                ax5.set_title('Left Paw ED', size = 8)
                
                ax6.plot(xDR_freq,xDR_pS)
                ax6.set_title('Right Paw ED', size = 8)
                
                fig.suptitle(folder + ', Video: ' + reach + ' Grooming', size=10)
                fig.tight_layout()
                fig.subplots_adjust(top=0.88)
                fig.savefig(outDir + 'groom/' + file[:-3] + 'pdf')
                
                plt.close()
                
                
                
                
# =============================================================================
# Beginning Abnormal Movement analysis
# =============================================================================




## Begin searching through all files, starting with animal folders
animals = list(frameDict.abMovFrames.keys())

for animal in animals:
    folders = list(frameDict.abMovFrames[animal].keys())

    ## Begin searching through animal's subdirectories, looking for DLC folders
    for folder in folders:
        
        allFiles = os.listdir(dirDLC + animal + '/DLC/' + folder)
        csvFiles = []
        
        ## Check for 'Center' in filename (direct view only analysis)
        for file in allFiles:
            
            if 'Center' not in file:
                continue
            elif not file.endswith('.csv'):
                continue
            else:
                csvFiles.append(file)
        
        reaches = list(frameDict.abMovFrames[animal][folder].keys())
        
        ## Begin searching through all of the reaches for the ones of interest
        for reach in reaches:

            
            # Check to see if reach is one of interest
            for file in csvFiles:
            
                if reach not in file:
                    continue
                
                print('beginning analysis on: ' + file)
                
                ## Pull in the behavior of interest frame numbers
                frame1 = frameDict.abMovFrames[animal][folder][reach][0]
                frame2 = frameDict.abMovFrames[animal][folder][reach][1]
                
                ## Define lists that will be filled later
                leftPawX = []
                leftPawY = []
                
                distanceLeft = []
                distanceRight = []
                distanceNose = []
                euclidDistLeft = []
                euclidDistRight = []
                
                # Read in file
                [leftPaw, rightPaw, nose, pellet] = funcs.readDLC(dirDLC + animal + '/DLC/' + folder + '/' + file)
            
                if frame2 > len(leftPaw):
                    frame2 = len(leftPaw)
                    
                # Cut down the read in files to be just the areas of interest
                leftPaw = leftPaw[frame1:frame2]
                rightPaw = rightPaw[frame1:frame2]
                nose = nose[frame1:frame2]
                pellet = pellet[frame1:frame2]
                
                # Calculate distances (distanceLeft/Right/Nose is between frames for same bodypart, euclidDistLeft/Right is between nose and paw)
                for index in range(1,len(leftPaw)):
                    distanceLeft.append(funcs.ptDist(leftPaw[index],leftPaw[index-1]))
                    distanceRight.append(funcs.ptDist(rightPaw[index],rightPaw[index-1]))
                    distanceNose.append(funcs.ptDist(nose[index],nose[index-1]))
                for index in range(0,len(nose)):
                    euclidDistLeft.append(funcs.ptDist(leftPaw[index],nose[index]))
                    euclidDistRight.append(funcs.ptDist(rightPaw[index],nose[index]))
                    
                # Convert things into numpy masked arrays and trim to desired frames only
                leftPaw = np.ma.array(leftPaw)
                rightPaw = np.ma.array(rightPaw)
                nose = np.ma.array(nose)
                pellet = np.ma.array(pellet)
                euclidDistLeft = np.ma.array(euclidDistLeft)
                euclidDistRight = np.ma.array(euclidDistRight)
                
                noseMask = nose[:,-1] < 0.75
                noseMask = noseMask.data
                
                # Define x,y,and p values for body parts with mask based on p value
                pLeftPaw_masked = np.ma.masked_where(leftPaw[:,-1] < 0.75, leftPaw[:,2])
                xLeftPaw_masked = np.ma.masked_where(leftPaw[:,-1]  < 0.75,leftPaw[:,0])
                yLeftPaw_masked = np.ma.masked_where(leftPaw[:,-1] < 0.75,leftPaw[:,1])
#                euclidDistLeft_masked = np.ma.masked_where(nose[:,-1] < 0.75,euclidDistLeft)
                
                pRightPaw_masked = np.ma.masked_where(rightPaw[:,-1] < 0.75,rightPaw[:,2])
                xRightPaw_masked = np.ma.masked_where(rightPaw[:,-1] < 0.75,rightPaw[:,0])
                yRightPaw_masked = np.ma.masked_where(rightPaw[:,-1] < 0.75,rightPaw[:,1])
#                euclidDistRight_masked = np.ma.masked_where(nose[:,-1] < 0.75,euclidDistRight)
                
                euclidDistRight_masked = euclidDistRight
                euclidDistRight_masked.mask = noseMask
                
                euclidDistLeft_masked = euclidDistLeft
                euclidDistLeft_masked.mask = noseMask
                
                ## Make masked based on whether a point jumped significanntly (defined as greater than 50 pxls here)
                dLeftRem = []
                dRightRem = []
                dNoseRem = []
                
                for dist in distanceLeft:
                    if dist > 50:
                        dLeftRem.append(distanceLeft.index(dist))
                for dist in distanceRight:
                    if dist > 50:
                        dRightRem.append(distanceRight.index(dist))
                for dist in distanceNose:
                    if dist > 50:
                        dNoseRem.append(distanceNose.index(dist))
                        
                distanceLeft = np.ma.array(distanceLeft)
                distanceRight = np.ma.array(distanceRight)
                distanceNose = np.ma.array(distanceNose)
                
                distanceLeft.mask = pLeftPaw_masked.mask[1:-1]
                distanceRight.mask = pRightPaw_masked.mask[1:-1]
                
                for item in dNoseRem:
                    euclidDistRight_masked.mask[item] = True
                    euclidDistLeft_masked.mask[item] = True
                for item in dLeftRem:
                    distanceLeft.mask[item] = True
                for item in dRightRem:
                    distanceRight.mask[item] = True
                    
                print('this is our dataset')
                
                ## Begin creating interpolated datasets using function
                x = list(range(frame1,frame2))
                x = [i/fps for i in x]
                xD = x[1:]
                
                tsXLeftPaw_inter, xLeftPaw_inter = funcs.interpolData(x,xLeftPaw_masked)
                tsXRightPaw_inter, xRightPaw_inter = funcs.interpolData(x,xRightPaw_masked)
                
                tsYLeftPaw_inter, yLeftPaw_inter = funcs.interpolData(x,yLeftPaw_masked)
                tsYRightPaw_inter, yRightPaw_inter = funcs.interpolData(x,yRightPaw_masked)
                
                tsDLeftPaw_inter, xDLeftPaw_inter = funcs.interpolData(xD,distanceLeft)
                tsDRightPaw_inter, xDRightPaw_inter = funcs.interpolData(xD,distanceRight)
                
                ## Apply filter to interpolated data
                xLeftPaw_interFilt = funcs.filterFunc(xLeftPaw_inter)
                yLeftPaw_interFilt = funcs.filterFunc(yLeftPaw_inter)
                
                xRightPaw_interFilt = funcs.filterFunc(xRightPaw_inter)
                yRightPaw_interFilt = funcs.filterFunc(yRightPaw_inter)
                
                xDLeftPaw_interFilt = funcs.filterFunc(xDLeftPaw_inter)
                xDRightPaw_interFilt = funcs.filterFunc(xDRightPaw_inter)
                
                ## Begin PSD analysis
                xLP_freq, xLP_pS = signal.periodogram(xLeftPaw_interFilt,fs)
                yLP_freq, yLP_pS = signal.periodogram(yLeftPaw_interFilt,fs)
                
                xRP_freq, xRP_pS = signal.periodogram(xRightPaw_interFilt,fs)
                yRP_freq, yRP_pS = signal.periodogram(yRightPaw_interFilt,fs)
                
                xDL_freq, xDL_pS = signal.periodogram(xDLeftPaw_interFilt,fs)
                xDR_freq, xDR_pS = signal.periodogram(xDRightPaw_interFilt,fs)
                
                ## Begin Plotting
                fig = plt.figure()
                ax1 = fig.add_subplot(321)
                ax2 = fig.add_subplot(322)
                ax3 = fig.add_subplot(323)
                
                ax4 = fig.add_subplot(324)
                ax5 = fig.add_subplot(325)
                ax6 = fig.add_subplot(326)
                
                ax1.plot(xLP_freq,xLP_pS)
                ax1.set_title('Left Paw, x-values', size = 8)
                
                ax2.plot(yLP_freq,yLP_pS)
                ax2.set_title('Left Paw, y-values', size = 8)
                
                ax3.plot(xRP_freq,xRP_pS)
                ax3.set_title('Right Paw, x-values', size = 8)
                
                ax4.plot(xRP_freq,xRP_pS)
                ax4.set_title('Right Paw, y-values', size = 8)
                
                ax5.plot(xDL_freq,xDL_pS)
                ax5.set_title('Left Paw ED', size = 8)
                
                ax6.plot(xDR_freq,xDR_pS)
                ax6.set_title('Right Paw ED', size = 8)
                
                fig.suptitle(folder + ', Video: ' + reach + ' Abnormal Movement', size=10)
                fig.tight_layout()
                fig.subplots_adjust(top=0.88)
                fig.savefig(outDir + 'abMov/' + file[:-3] + 'pdf')
                
                plt.close()
                
                
                
                
                
                