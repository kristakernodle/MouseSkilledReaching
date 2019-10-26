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
#from scipy import signal
from scipy import fftpack
import matplotlib.pyplot as plt
import numpy as np
#import numpy.ma as ma

dirDLC = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/DLCProcessing/currentDLCIter/'
outDir = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/DLCProcessing/powerAnalysis/'
fps = 100
fs = fps

lrange = 0
urange = 20

fig = plt.figure()

firstPass = 0

# =============================================================================
# Beginning Abnormal Movement analysis
# =============================================================================
#fig = plt.figure()

## Begin searching through all files, starting with animal folders
animals = list(frameDict.abMovFrames.keys())

for animal in animals:
    folders = list(frameDict.abMovFrames[animal].keys())

    ## Begin searching through animal's subdirectories, looking for DLC folders
    for folder in folders:
        
        allFiles = os.listdir(dirDLC + animal + '/DLC/')
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
                if file == '710_20181105_01_R5DeepCut_resnet50_rightPP_CenterFeb9shuffle1_200000.csv':
                    print('pause')
            
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
                [leftPaw, rightPaw, nose, pellet] = funcs.readDLC(dirDLC + animal + '/DLC/' + '/' + file)
            
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
                
#                ## Apply filter to interpolated data
#                xLeftPaw_interFilt = funcs.filterFunc(xLeftPaw_inter)
#                yLeftPaw_interFilt = funcs.filterFunc(yLeftPaw_inter)
#                
#                xRightPaw_interFilt = funcs.filterFunc(xRightPaw_inter)
#                yRightPaw_interFilt = funcs.filterFunc(yRightPaw_inter)
#                
#                xDLeftPaw_interFilt = funcs.filterFunc(xDLeftPaw_inter)
#                xDRightPaw_interFilt = funcs.filterFunc(xDRightPaw_inter)
#                
#                ## Begin PSD analysis
#                xLP_freq, xLP_pS = signal.periodogram(xLeftPaw_inter,fs)
#                yLP_freq, yLP_pS = signal.periodogram(yLeftPaw_inter,fs)
#                
#                xRP_freq, xRP_pS = signal.periodogram(xRightPaw_inter,fs)
#                yRP_freq, yRP_pS = signal.periodogram(yRightPaw_inter,fs)
#                
#                xDL_freq, xDL_pS = signal.periodogram(xDLeftPaw_inter,fs)
#                xDR_freq, xDR_pS = signal.periodogram(xDRightPaw_inter,fs)
                
                ## FFT
                FFT_xLeftPaw = fftpack.fft(xLeftPaw_inter)
                freqs_xLeftPaw = fftpack.fftfreq(len(xLeftPaw_inter))*100
                
                FFT_yLeftPaw = fftpack.fft(yLeftPaw_inter)
                freqs_yLeftPaw = fftpack.fftfreq(len(yLeftPaw_inter))*100
                
                FFT_xRightPaw = fftpack.fft(xRightPaw_inter)
                freqs_xRightPaw = fftpack.fftfreq(len(xRightPaw_inter))*100
                
                FFT_yRightPaw = fftpack.fft(xRightPaw_inter)
                freqs_yRightPaw = fftpack.fftfreq(len(xRightPaw_inter))*100
                
                FFT_LD = fftpack.fft(xDLeftPaw_inter)
                freqs_LD = fftpack.fftfreq(len(xDLeftPaw_inter))*100
                
                FFT_RD = fftpack.fft(xDRightPaw_inter)
                freqs_RD = fftpack.fftfreq(len(xDRightPaw_inter))*100
                
                if firstPass == 0:
                    mean_xLeftPaw = np.abs(FFT_xLeftPaw)
                    meanF_xLeftPaw = freqs_xLeftPaw
                    
                    mean_yLeftPaw = np.abs(FFT_yLeftPaw)
                    meanF_yLeftPaw = freqs_yLeftPaw
                    
                    mean_xRightPaw = np.abs(FFT_xRightPaw)
                    meanF_xRightPaw = freqs_xRightPaw
                    
                    mean_yRightPaw = np.abs(FFT_yRightPaw)
                    meanF_yRightPaw = freqs_yRightPaw
                    
                    mean_leftDist = np.abs(FFT_LD)
                    meanF_leftDist = freqs_LD
                    
                    mean_rightDist = np.abs(FFT_RD)
                    meanF_rightDist = freqs_RD
                    firstPass = 1
                else:
                    mean_xLeftPaw = [(i+j)/2 for i in np.abs(FFT_xLeftPaw) for j in mean_xLeftPaw]
                    meanF_xLeftPaw = [(i+j)/2 for i in freqs_xLeftPaw for j in meanF_xLeftPaw]
                    
                    mean_yLeftPaw = [(i+j)/2 for i in np.abs(FFT_yLeftPaw) for j in mean_yLeftPaw]
                    meanF_yLeftPaw = [(i+j)/2 for i in freqs_yLeftPaw for j in meanF_yLeftPaw]
                    
                    mean_xRightPaw = [(i+j)/2 for i in np.abs(FFT_xRightPaw) for j in mean_xRightPaw]
                    meanF_xRightPaw = [(i+j)/2 for i in freqs_xRightPaw for j in meanF_xRightPaw]
                    
                    mean_yRightPaw = [(i+j)/2 for i in np.abs(FFT_yRightPaw) for j in mean_yRightPaw]
                    meanF_yRightPaw = [(i+j)/2 for i in freqs_yRightPaw for j in meanF_yRightPaw]
                    
                    mean_leftDist = [(i+j)/2 for i in np.abs(FFT_LD) for j in mean_leftDist]
                    meanF_leftDist = [(i+j)/2 for i in freqs_LD for j in meanF_leftDist]
                    
                    mean_rightDist = [(i+j)/2 for i in np.abs(FFT_RD) for j in mean_rightDist]
                    meanF_rightDist = [(i+j)/2 for i in freqs_RD for j in meanF_rightDist]
                                
                
## Begin Plotting

ax1 = fig.add_subplot(321)
ax2 = fig.add_subplot(322)
ax3 = fig.add_subplot(323)

ax4 = fig.add_subplot(324)
ax5 = fig.add_subplot(325)
ax6 = fig.add_subplot(326)

ax1.plot(meanF_xLeftPaw,mean_xLeftPaw,'r')
ax1.set_xlim(lrange, urange)
ax1.set_ylim(-5, 2500)
ax1.set_title('Left Paw, x-values', size = 8)


ax2.plot(meanF_yLeftPaw,mean_yLeftPaw,'r')
ax2.set_xlim(lrange, urange)
ax2.set_ylim(-5, 2500)
ax2.set_title('Left Paw, y-values', size = 8)

ax3.plot(meanF_xRightPaw,mean_xRightPaw,'r')
ax3.set_xlim(lrange, urange)
ax3.set_ylim(-5, 2500)
ax3.set_title('Right Paw, x-values', size = 8)
ax3.set_ylabel('Amplitude (pixels)')

ax4.plot(meanF_yRightPaw,mean_yRightPaw,'r')
ax4.set_xlim(lrange, urange)
ax4.set_ylim(-5, 2500)
ax4.set_title('Right Paw, y-values', size = 8)

ax5.plot(meanF_leftDist,mean_leftDist,'r')
ax5.set_xlim(lrange, urange)
ax5.set_ylim(-5, 2500)
ax5.set_title('Left Paw ED', size = 8)
ax5.set_xlabel('Frequency (Hz)')


ax6.plot(meanF_rightDist,mean_rightDist,'r')
ax6.set_xlim(lrange, urange)
ax6.set_ylim(-5, 2500)
ax6.set_title('Right Paw ED', size = 8)
ax6.set_xlabel('Frequency (Hz)')

firstPass = 0

## Begin searching through all files, starting with animal folders
animals = list(frameDict.groom.keys())

for animal in animals:
    folders = list(frameDict.groom[animal].keys())

    ## Begin searching through animal's subdirectories, looking for DLC folders
    for folder in folders:
        
        allFiles = os.listdir(dirDLC + animal + '/DLC/')
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
                [leftPaw, rightPaw, nose, pellet] = funcs.readDLC(dirDLC + animal + '/DLC/' + '/' + file)
            
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
                
#                ## Apply filter to interpolated data
#                xLeftPaw_interFilt = funcs.filterFunc(xLeftPaw_inter)
#                yLeftPaw_interFilt = funcs.filterFunc(yLeftPaw_inter)
#                
#                xRightPaw_interFilt = funcs.filterFunc(xRightPaw_inter)
#                yRightPaw_interFilt = funcs.filterFunc(yRightPaw_inter)
#                
#                xDLeftPaw_interFilt = funcs.filterFunc(xDLeftPaw_inter)
#                xDRightPaw_interFilt = funcs.filterFunc(xDRightPaw_inter)
#                
#                ## Begin PSD analysis
#                xLP_freq, xLP_pS = signal.periodogram(xLeftPaw_inter,fs)
#                yLP_freq, yLP_pS = signal.periodogram(yLeftPaw_inter,fs)
#                
#                xRP_freq, xRP_pS = signal.periodogram(xRightPaw_inter,fs)
#                yRP_freq, yRP_pS = signal.periodogram(yRightPaw_inter,fs)
#                
#                xDL_freq, xDL_pS = signal.periodogram(xDLeftPaw_inter,fs)
#                xDR_freq, xDR_pS = signal.periodogram(xDRightPaw_inter,fs)
                
                ## FFT
                FFT_xLeftPaw = fftpack.fft(xLeftPaw_inter)
                freqs_xLeftPaw = fftpack.fftfreq(len(xLeftPaw_inter))*100
                
                FFT_yLeftPaw = fftpack.fft(yLeftPaw_inter)
                freqs_yLeftPaw = fftpack.fftfreq(len(yLeftPaw_inter))*100
                
                FFT_xRightPaw = fftpack.fft(xRightPaw_inter)
                freqs_xRightPaw = fftpack.fftfreq(len(xRightPaw_inter))*100
                
                FFT_yRightPaw = fftpack.fft(xRightPaw_inter)
                freqs_yRightPaw = fftpack.fftfreq(len(xRightPaw_inter))*100
                
                FFT_LD = fftpack.fft(xDLeftPaw_inter)
                freqs_LD = fftpack.fftfreq(len(xDLeftPaw_inter))*100
                
                FFT_RD = fftpack.fft(xDRightPaw_inter)
                freqs_RD = fftpack.fftfreq(len(xDRightPaw_inter))*100
                
                if firstPass == 0:
                    mean_xLeftPaw = np.abs(FFT_xLeftPaw)
                    meanF_xLeftPaw = freqs_xLeftPaw
                    
                    mean_yLeftPaw = np.abs(FFT_yLeftPaw)
                    meanF_yLeftPaw = freqs_yLeftPaw
                    
                    mean_xRightPaw = np.abs(FFT_xRightPaw)
                    meanF_xRightPaw = freqs_xRightPaw
                    
                    mean_yRightPaw = np.abs(FFT_yRightPaw)
                    meanF_yRightPaw = freqs_yRightPaw
                    
                    mean_leftDist = np.abs(FFT_LD)
                    meanF_leftDist = freqs_LD
                    
                    mean_rightDist = np.abs(FFT_RD)
                    meanF_rightDist = freqs_RD
                    firstPass = 1
                else:
                    mean_xLeftPaw = [(i+j)/2 for i in np.abs(FFT_xLeftPaw) for j in mean_xLeftPaw]
                    meanF_xLeftPaw = [(i+j)/2 for i in freqs_xLeftPaw for j in meanF_xLeftPaw]
                    
                    mean_yLeftPaw = [(i+j)/2 for i in np.abs(FFT_yLeftPaw) for j in mean_yLeftPaw]
                    meanF_yLeftPaw = [(i+j)/2 for i in freqs_yLeftPaw for j in meanF_yLeftPaw]
                    
                    mean_xRightPaw = [(i+j)/2 for i in np.abs(FFT_xRightPaw) for j in mean_xRightPaw]
                    meanF_xRightPaw = [(i+j)/2 for i in freqs_xRightPaw for j in meanF_xRightPaw]
                    
                    mean_yRightPaw = [(i+j)/2 for i in np.abs(FFT_yRightPaw) for j in mean_yRightPaw]
                    meanF_yRightPaw = [(i+j)/2 for i in freqs_yRightPaw for j in meanF_yRightPaw]
                    
                    mean_leftDist = [(i+j)/2 for i in np.abs(FFT_LD) for j in mean_leftDist]
                    meanF_leftDist = [(i+j)/2 for i in freqs_LD for j in meanF_leftDist]
                    
                    mean_rightDist = [(i+j)/2 for i in np.abs(FFT_RD) for j in mean_rightDist]
                    meanF_rightDist = [(i+j)/2 for i in freqs_RD for j in meanF_rightDist]
                                
                
## Begin Plotting

ax1 = fig.add_subplot(321)
ax2 = fig.add_subplot(322)
ax3 = fig.add_subplot(323)

ax4 = fig.add_subplot(324)
ax5 = fig.add_subplot(325)
ax6 = fig.add_subplot(326)

ax1.plot(meanF_xLeftPaw,mean_xLeftPaw,'b')
ax1.set_xlim(lrange, urange)
ax1.set_ylim(-5, 2500)
ax1.set_title('Left Paw, x-values', size = 8)


ax2.plot(meanF_yLeftPaw,mean_yLeftPaw,'b')
ax2.set_xlim(lrange, urange)
ax2.set_ylim(-5, 2500)
ax2.set_title('Left Paw, y-values', size = 8)

ax3.plot(meanF_xRightPaw,mean_xRightPaw,'b')
ax3.set_xlim(lrange, urange)
ax3.set_ylim(-5, 2500)
ax3.set_title('Right Paw, x-values', size = 8)
ax3.set_ylabel('Amplitude (pixels)')

ax4.plot(meanF_yRightPaw,mean_yRightPaw,'b')
ax4.set_xlim(lrange, urange)
ax4.set_ylim(-5, 2500)
ax4.set_title('Right Paw, y-values', size = 8)

ax5.plot(meanF_leftDist,mean_leftDist,'b')
ax5.set_xlim(lrange, urange)
ax5.set_ylim(-5, 2500)
ax5.set_title('Left Paw ED', size = 8)
ax5.set_xlabel('Frequency (Hz)')


ax6.plot(meanF_rightDist,mean_rightDist,'b')
ax6.set_xlim(lrange, urange)
ax6.set_ylim(-5, 2500)
ax6.set_title('Right Paw ED', size = 8)
ax6.set_xlabel('Frequency (Hz)')
                
#fig.suptitle(folder + ', Video: ' + reach + ' Grooming', size=10)
#fig.tight_layout()
#fig.subplots_adjust(top=0.88)
#fig.savefig(outDir + 'groom/' + 'grooming.pdf')
#
#plt.close()
                

                

                
                
      
fig.suptitle('Average FFT: Abnormal Movements versus Grooming', size=10)
fig.tight_layout()
fig.subplots_adjust(top=0.88)
fig.savefig(outDir + 'average_plot.pdf')

plt.close()
                
#                
#                
                
                
                