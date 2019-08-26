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
import frameDict


### For now, processing on 710 only
dirDLC = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/'

xLMin = []
xLMax = []
yLMin = []
yLMax = []
eucLMin = []
eucLMax = []

xRMin = []
xRMax = []
yRMin = []
yRMax = []
eucRMin = []
eucRMax = []

xLScale = []
xRScale = []

yLScale = []
yRScale = []

eucLScale = []
eucRScale = []



animals = list(frameDict.abMovFrames.keys())

for animal in animals:
    folders = list(frameDict.abMovFrames[animal].keys())
    
    for folder in folders:
        
        allFiles = os.listdir(dirDLC + animal + '/DLC/' + folder)
        csvFiles = []
        for file in allFiles:
            if 'Center' not in file:
                continue
            elif not file.endswith('.csv'):
                continue
            else:
                csvFiles.append(file)
        
        reaches = list(frameDict.abMovFrames[animal][folder].keys())
        
        for reach in reaches:
            for file in csvFiles:
            
                if reach not in file:
                    continue
                oframe1 = frameDict.abMovFrames[animal][folder][reach][0]
                oframe2 = frameDict.abMovFrames[animal][folder][reach][1]
                
                frame1 = oframe1
                frame2 = oframe2
                frameDiff = frame2-frame1
                
                while frameDiff < 200:
                    frame1 = frame1 - 5
                    frame2 = frame2 + 5
                    frameDiff = frame2-frame1
                    
                print(file)
                
                
                
                distanceLeft = []
                distanceRight = []
                distanceNose = []
                euclidDistLeft = []
                euclidDistRight = []
                
                # Read in file
                [leftPaw, rightPaw, nose, pellet] = funcs.readDLC(dirDLC + animal + '/DLC/' + folder + '/' + file)
            
                # Calculate distances (distanceLeft/Right/Nose is between frames for same bodypart, euclidDistLeft/Right is between nose and paw)
                for index in range(1,len(leftPaw)):
                    distanceLeft.append(funcs.ptDist(leftPaw[index],leftPaw[index-1]))
                for index in range(1,len(rightPaw)):
                    distanceRight.append(funcs.ptDist(rightPaw[index],rightPaw[index-1]))
                for index in range(1,len(nose)):
                    distanceNose.append(funcs.ptDist(nose[index],nose[index-1]))
                for index in range(0,len(nose)):
                    euclidDistLeft.append(funcs.ptDist(leftPaw[index],nose[index]))
                    euclidDistRight.append(funcs.ptDist(rightPaw[index],nose[index]))
                    
                # Convert things into numpy masked arrays
                leftPaw = np.ma.array(leftPaw)
                rightPaw = np.ma.array(rightPaw)
                nose = np.ma.array(nose)
                pellet = np.ma.array(pellet)
                euclidDistLeft = np.ma.array(euclidDistLeft)
                euclidDistRight = np.ma.array(euclidDistRight)
                
                # Define x,y,and p values for body parts with mask
                pLeftPaw_masked = np.ma.masked_where(leftPaw[:,-1] < 0.75, leftPaw[:,2])
                xLeftPaw_masked = np.ma.masked_where(leftPaw[:,-1]  < 0.75,leftPaw[:,0])
                yLeftPaw_masked = np.ma.masked_where(leftPaw[:,-1] < 0.75,leftPaw[:,1])
                euclidDistLeft_masked = np.ma.masked_where(nose[:,-1] < 0.75,euclidDistLeft)
                
                pRightPaw_masked = np.ma.masked_where(rightPaw[:,-1] < 0.75,rightPaw[:,2])
                xRightPaw_masked = np.ma.masked_where(rightPaw[:,-1] < 0.75,rightPaw[:,0])
                yRightPaw_masked = np.ma.masked_where(rightPaw[:,-1] < 0.75,rightPaw[:,1])
                euclidDistRight_masked = np.ma.masked_where(nose[:,-1] < 0.75,euclidDistRight)
                
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
                
                
                
                fps = 100
                
                ## Start working x and y coordinates separately to form smoothing functions
                
                # x coordinates
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
                fxL = interp1d(xL_compressed,xLeftPaw_compressed,kind = 'cubic')
                xfLnew = fxL(xLnew)
                
                xRnew = np.linspace(xR_compressed[0],xR_compressed[-1],num = len(x), endpoint=True)
                fxR = interp1d(xR_compressed,xRightPaw_compressed,kind = 'cubic')
                xfRnew = fxR(xRnew)
                
                # y coordinates
                y = list(range(1,len(yLeftPaw_masked)+1)) 
                y = [i/fps for i in y]
                yL_masked = np.ma.array(y)
                yR_masked = np.ma.array(y)
                
                yL_masked.mask = yLeftPaw_masked.mask
                yR_masked.mask = yRightPaw_masked.mask
                
                yLeftPaw_compressed = yLeftPaw_masked.compressed()
                yRightPaw_compressed = yRightPaw_masked.compressed()
                yL_compressed = yL_masked.compressed()
                yR_compressed = yR_masked.compressed()
                
                yLnew = np.linspace(yL_compressed[0],yL_compressed[-1],num = len(y), endpoint=True)
                fyL = interp1d(yL_compressed,yLeftPaw_compressed,kind = 'cubic')
                yfLnew = fyL(yLnew)
                
                yRnew = np.linspace(yR_compressed[0],yR_compressed[-1],num = len(y), endpoint=True)
                fyR = interp1d(yR_compressed,yRightPaw_compressed,kind = 'cubic')
                yfRnew = fyR(yRnew)
                
                ## Euclidean Distance From Nose
                xD = list(range(1,len(euclidDistLeft)+1)) 
                xD = [i/fps for i in xD]
                dL_masked = np.ma.array(xD)
                dR_masked = np.ma.array(xD)
                
                dL_masked.mask = euclidDistLeft_masked.mask
                dR_masked.mask = euclidDistRight_masked.mask
                
                euclidDistLeft_compressed = euclidDistLeft_masked.compressed()
                euclidDistRight_compressed = euclidDistRight_masked.compressed()
                dL_compressed = dL_masked.compressed()
                dR_compressed = dR_masked.compressed()
                
                dLnew = np.linspace(dL_compressed[0],dL_compressed[-1],num = len(xD), endpoint=True)
                fdL = interp1d(dL_compressed,euclidDistLeft_compressed,kind = 'cubic')
                dfLnew = fdL(dLnew)
                
                dRnew = np.linspace(dR_compressed[0],dR_compressed[-1],num = len(xD), endpoint=True)
                fdR = interp1d(dR_compressed,euclidDistRight_compressed,kind = 'cubic')
                dfRnew = fdR(dRnew)
                
                xLScale.append(np.ma.max(xfLnew[frame1:frame2]) - np.ma.min(xfLnew[frame1:frame2]))
                xRScale.append(np.ma.max(xfRnew[frame1:frame2]) - np.ma.min(xfRnew[frame1:frame2]))
                
#                yLScale.append(np.ma.max(yLeftPaw_masked[frame1:frame2]) - np.ma.min(yLeftPaw_masked[frame1:frame2]))
#                yRScale.append(np.ma.max(yRightPaw_masked[frame1:frame2]) - np.ma.min(yRightPaw_masked[frame1:frame2]))
#                
#                eucLScale.append(np.ma.max(euclidDistLeft_masked[frame1:frame2]) - np.ma.min(euclidDistLeft_masked[frame1:frame2]))
#                eucRScale.append(np.ma.max(euclidDistRight_masked[frame1:frame2]) - np.ma.min(euclidDistRight_masked[frame1:frame2]))
#                

                xLmin = np.floor(np.ma.min(xfLnew[frame1:frame2]))
                xLmax = np.ceil(np.ma.max(xfLnew[frame1:frame2]))
                xRmin = np.floor(np.ma.min(xfRnew[frame1:frame2]))
                xRmax = np.ceil(np.ma.max(xfRnew[frame1:frame2]))
                
                Ldiff = xLmax - xLmin
                Rdiff = xRmax - xRmin
                
                if Ldiff < Rdiff:
                    while Rdiff < 350:
                        xRmin += -1
                        xRmax += 1
                        Rdiff = xRmax - xRmin
                        
                    xMin = xRmin
                    xMax = xRmax
                else:
                    while Ldiff < 250:
                        xLmin += -1
                        xLmax += 1
                        Ldiff = xLmax - xLmin
                    xMin = xLmin
                    xMax= xLmax
#                xMin = 100
#                xMax = 900
                yMin = 0
                yMax = 900
                eucMin = -550
                eucMax = 550
                
                ## Begin Plotting
                
                fig = plt.figure()
                ax1 = fig.add_subplot(231)
                ax2 = fig.add_subplot(232)
                ax5 = fig.add_subplot(233)
                ax3 = fig.add_subplot(234)
                ax4 = fig.add_subplot(235)
                ax6 = fig.add_subplot(236)
                
                            
                ax1.plot(x[frame1:frame2],xLeftPaw_masked[frame1:frame2],'o',label='Original Data')
                ax1.plot(xLnew[frame1:frame2],xfLnew[frame1:frame2],'-',label='Cubic 1D Interpolation')
                ax1.axvspan(oframe1/fps, oframe2/fps, facecolor='#d7f4d7', alpha=0.5)
                ax1.set_ylim([xMin,xMax])

            
                ax2.plot(x[frame1:frame2],xRightPaw_masked[frame1:frame2],'o',label='Original Data')
                ax2.plot(xRnew[frame1:frame2],xfRnew[frame1:frame2],'-',label='Cubic 1D Interpolation')
                ax2.axvspan(oframe1/fps, oframe2/fps, facecolor='#d7f4d7', alpha=0.5)
                ax2.set_ylim([100,500])

                
                ax3.plot(y[frame1:frame2],yLeftPaw_masked[frame1:frame2],'o',label='Original Data')
                ax3.plot(yLnew[frame1:frame2],yfLnew[frame1:frame2],'-',label='Cubic 1D Interpolation')
                ax3.axvspan(oframe1/fps, oframe2/fps, facecolor='#d7f4d7', alpha=0.5)
                ax3.set_ylim([xMin,xMax])

                
                ax4.plot(y[frame1:frame2],yRightPaw_masked[frame1:frame2],'o',label='Original Data')
                ax4.plot(yRnew[frame1:frame2],yfRnew[frame1:frame2],'-',label='Cubic 1D Interpolation')
                ax4.axvspan(oframe1/fps, oframe2/fps, facecolor='#d7f4d7', alpha=0.5)
                ax4.set_ylim([yMin,yMax])

                
                ax5.plot(xD[frame1:frame2],euclidDistLeft_masked[frame1:frame2],'o',label='Original Data')
                ax5.plot(dLnew[frame1:frame2],dfLnew[frame1:frame2],'-',label='Cubic 1D Interpolation')
                ax5.axvspan(oframe1/fps,oframe2/fps,facecolor='#d7f4d7', alpha=0.5)
                ax5.set_ylim([eucMin,eucMax]) 
 
                
                ax6.plot(xD[frame1:frame2],euclidDistRight_masked[frame1:frame2],'o',label='Original Data')
                ax6.plot(dRnew[frame1:frame2],dfRnew[frame1:frame2],'-',label='Cubic 1D Interpolation')
                ax6.axvspan(oframe1/fps,oframe2/fps,facecolor='#d7f4d7', alpha=0.5) 
                ax6.set_ylim([eucMin,eucMax])

                
                fig.tight_layout()
                fig.savefig(dirDLC + 'DLCProcessing/' + file[:-3] + 'pdf')

                plt.close()



    