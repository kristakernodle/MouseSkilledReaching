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
import numpy as np
from scipy import fftpack

import funcs
import plots
import frameDict
frameDict = frameDict.frameDict

dirDLC = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/DLCProcessing/currentDLCIter/'
outDir = '/Users/kkrista/Desktop/'

view = 'Center'

fs = 100
lrange = 0
urange = 15
firstPass = 0

rows = 4
cols = 4

plotting = False

xPixRange = []
yPixRange = []
EDPixRange = []

fftData = {}
 
## Get the behaviors (keys) from the frameDict
behaviors = list(frameDict.keys())

for item in behaviors:
    fftData[item] = {}

## Start looping through the keys in frameDict (abMovFrames and groom)
for beh in behaviors:
    
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
        
        # Get all relevant dates for this mouse
        allDates = list(frameDict[beh][mouse].keys())
        
        # Start looping through relevant dates
        for day in allDates:

            fftData[beh][mouse][day] = {}
            
            # Get all relevant reaches
            reaches = list(frameDict[beh][mouse][day].keys())
            fftData[beh][mouse][day]['reaches']=reaches
            # Get all files in DLC directory for this mouse
            allFiles = os.listdir(dirDLC + mouse + '/DLC/')
            
            # Start processing one reach at a time
            for reach in reaches:
                
                fftData[beh][mouse][day][reach] = {}
                
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
                [leftPaw, rightPaw, nose, pellet] = funcs.readDLC(dirDLC + mouse + '/DLC/' + file)
                
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
                
                    if beh == 'abMovFrames':
                        desc = 'Abnormal Movement'
                    else:
                        desc = 'Grooming'
                
                interLeftPaw = [list(a) for a in interLeftPaw]
                interLeftPaw = list(zip(*interLeftPaw))
                interRightPaw = [list(a) for a in interRightPaw]
                interRightPaw = list(zip(*interRightPaw))
                interNose = [list(a) for a in interNose]
                interNose = list(zip(*interNose))
                interEDLeft = [list(a) for a in interEDLeft]
                interEDLeft = list(zip(*interLeftPaw))
                interEDRight = [list(a) for a in interEDRight]
                    
                time = np.linspace(frame1,frame2,len(leftPaw),endpoint=True)
                time = [frame/100 for frame in time]
                
                if plotting == False:
                    
                    xPixRange.append(max(interLeftPaw[0])-min(interLeftPaw[0]))
                    yPixRange.append(max(interLeftPaw[1])-min(interLeftPaw[1]))
                    EDPixRange.append(max(ED_Left)-min(ED_Left))
                
                    xPixRange.append(max(interRightPaw[0])-min(interRightPaw[0]))
                    yPixRange.append(max(interRightPaw[1])-min(interRightPaw[1]))
                    EDPixRange.append(max(ED_Right)-min(ED_Right))
                
                else:
                    filename = plots.plotFilename(csvFile,beh)
                    title = plots.plotTitle(mouse,day,reach,beh)
                    
                    plots.plotPixels(outDir,filename,title,time, interLeftPaw, interRightPaw, ED_Left, ED_Right, leftPaw_fft)
                
                ## Begin Plotting
#                fig = plt.figure()
#                ax1 = fig.add_subplot(rows,cols,1)
#                ax2 = fig.add_subplot(rows,cols,2)
#                ax3 = fig.add_subplot(rows,cols,3)
#                ax4 = fig.add_subplot(rows,cols,4)
#                

#                
#                ## Left Paw (first row, all columns)
#                
#                # First Column = x,y traces
#                ax1.plot(interLeftPaw[0],interLeftPaw[1],'k')
#                ax1.set_title('Trace of Paw over Time', size = 8)
#                # Second Column = x trace over time
#                ax2.plot(time,interLeftPaw[0],'b')
#                ax2.set_title('Horizontal Movement (x-values)', size = 8)
#                # Third Column = y trace over time
#                ax3.plot(time,interLeftPaw[1],'g')
#                ax3.set_title('Vertical Movement (y-values)', size = 8)
#                # Fourth Column = Spectral analysis for animal
#                ax4.plot(np.abs(leftPaw_fft[:N // 2]))
#                ax4.set_xlim(lrange, urange)
#                ax4.set_ylim(-5, 2500)
#                ax4.set_title('Spectrogram', size = 8)
#                
#                plt.show()
                
#                ax1.plot(np.abs(leftPaw_fft[:N // 2]))
#                ax1.set_xlim(lrange, urange)
#                ax1.set_ylim(-5, 2500)
#                ax1.set_title('Left Paw', size = 8)
#                
#                ax2.plot(np.abs(rightPaw_fft[:N // 2]))
#                ax2.set_xlim(lrange, urange)
#                ax2.set_ylim(-5, 2500)
#                ax2.set_title('Right Paw', size = 8)
#                
#                ax3.plot(np.abs(nose_fft[:N // 2]))
#                ax3.set_xlim(lrange, urange)
#                ax3.set_ylim(-5, 2500)
#                ax3.set_title('Nose', size = 8)
#                
#                fig.suptitle(desc + ' Power Analysis: ' + mouse, size=10)
#                fig.tight_layout()
#                fig.subplots_adjust(top=0.88)
#                fig.savefig(outDir + beh + '_' + day + '_' + reach + '.pdf')
#
#                plt.close()
#                

if plotting == False:
    yRange = []
    yRange.append(max(xPixRange))
    yRange.append(max(yPixRange))
    yRange.append(max(EDPixRange))
    yRange = np.ceil(max(yRange))


#    ## Begin Plotting AVERAGES
#    fig = plt.figure()
#    
#    ax1 = fig.add_subplot(rows,cols,1)
#    ax2 = fig.add_subplot(rows,cols,2)
#    ax3 = fig.add_subplot(rows,cols,3)
#    
#    ax1.plot(mean_leftPaw_freq,mean_leftPaw_fft)
#    ax1.set_xlim(lrange, urange)
#    ax1.set_ylim(-5, 2500)
#    ax1.set_ylabel('Power')
#    ax1.set_title('Left Paw', size = 8)
#    ax2.plot(mean_rightPaw_freq,mean_rightPaw_fft)
#    ax2.set_xlim(lrange, urange)
#    ax2.set_ylim(-5, 2500)
#    ax2.set_ylabel('Power')
#    ax2.set_title('Right Paw', size = 8)
#    ax3.plot(mean_nose_freq,mean_nose_fft)
#    ax3.set_xlim(lrange, urange)
#    ax3.set_ylim(-5, 2500)
#    ax3.set_title('Nose', size = 8)
#    ax3.set_xlabel('Frequency (Hz)')
#    ax3.set_ylabel('Power')
#    
#    if beh == 'abMovFrames':
#        desc = 'Abnormal Movements'
#    else:
#        desc = 'Grooming'
#    
#    fig.suptitle('Mean Power Analysis During '+ desc, size=10)
#    fig.tight_layout()
#    fig.subplots_adjust(top=0.88)
#    fig.savefig(outDir + beh + '_mean.pdf')
#    
#    plt.close()
        
                    
                
                    
                
                
                
                
                
                
                
                
                

