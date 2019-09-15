# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 19:03:22 2019

@author: Krista Kernodle

"""

import os
import funcs
import frameDict
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

dirDLC = 'X:/Neuro-Leventhal/data/mouseSkilledReaching/'
fps = 59.55
fs = 100

animals = list(frameDict.groom.keys())

for animal in animals:
    folders = list(frameDict.groom[animal].keys())
    
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
        
        reaches = list(frameDict.groom[animal][folder].keys())
        
        for reach in reaches:
            for file in csvFiles:
            
                if reach not in file:
                    continue
                oframe1 = frameDict.groom[animal][folder][reach][0]
                oframe2 = frameDict.groom[animal][folder][reach][1]
                    
                print(file)
                
                
                leftPawX = []
                leftPawY = []
                
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
                    
                # Convert things into numpy masked arrays and trim to desired frames only
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
                                
                ## Start working x and y coordinates separately to get power spectral analysis
                
                xLP_freq, xLP_pS = signal.periodogram(xLeftPaw_masked[oframe1:oframe2+1],fs)
                yLP_freq, yLP_pS = signal.periodogram(yLeftPaw_masked[oframe1:oframe2+1],fs)
                xRP_freq, xRP_pS = signal.periodogram(xRightPaw_masked[oframe1:oframe2+1],fs)
                yRP_freq, yRP_pS = signal.periodogram(yRightPaw_masked[oframe1:oframe2+1],fs)
                xDL_freq, xDL_pS = signal.periodogram(distanceLeft[oframe1:oframe2+1],fs)
                xDR_freq, xDR_pS = signal.periodogram(distanceRight[oframe1:oframe2+1],fs)
                
                
                ## Start Plotting
                
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
                fig.savefig(dirDLC + 'DLCProcessing/powerAnalysis/' + file[:-3] + 'pdf')
                
                plt.close()
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                