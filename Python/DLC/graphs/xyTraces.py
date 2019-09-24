#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 12:01:02 2019

@author: kkrista
"""

import os
import funcs
import frameDict
#from scipy import signal
#from scipy import fftpack
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
#import numpy.ma as ma

dirDLC = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/'
vidDir = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/'
outDir = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/DLCProcessing/xyTraces/'
fps = fs = 100

lrange = 0
urange = 20

fig = plt.figure()
ax = plt.axes(xlim=(200,500), ylim=(0,700))
line, = ax.plot([], [], lw=2)

firstPass = 0


# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    return line,

# animation function.  This is called sequentially
def animate(i):
    
    fxNew = fx(xNew[:i])
    fyNew = fy(yNew[:i])
    
    line.set_data(fxNew,fyNew)
    return line,


# =============================================================================
# Beginning Abnormal Movement analysis
# =============================================================================


## Begin searching through all files, starting with animal folders
animals = list(frameDict.abMovFrames.keys())

for animal in animals:
    if animal != 'et717':
        continue
    
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
            if reach != '01_R20D':
                continue
            
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
                
                pRightPaw_masked = np.ma.masked_where(rightPaw[:,-1] < 0.75,rightPaw[:,2])
                xRightPaw_masked = np.ma.masked_where(rightPaw[:,-1] < 0.75,rightPaw[:,0])
                yRightPaw_masked = np.ma.masked_where(rightPaw[:,-1] < 0.75,rightPaw[:,1])
                
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
                
                ## Begin creating interpolated datasets using function
                x = list(range(frame1,frame2))
                x = [i/fps for i in x]
                xD = x[1:]
                
                tsXLeftPaw_inter, xLeftPaw_inter, xLP_f = funcs.interpolData(x,xLeftPaw_masked)
                tsXRightPaw_inter, xRightPaw_inter, yLP_f = funcs.interpolData(x,xRightPaw_masked)
                
                tsYLeftPaw_inter, yLeftPaw_inter, xRP_f = funcs.interpolData(x,yLeftPaw_masked)
                tsYRightPaw_inter, yRightPaw_inter, yRP_f = funcs.interpolData(x,yRightPaw_masked)
                
                tsDLeftPaw_inter, xDLeftPaw_inter, dist_f = funcs.interpolData(xD,distanceLeft)
                tsDRightPaw_inter, xDRightPaw_inter, dist_f = funcs.interpolData(xD,distanceRight)
                
                print('now we play with graphs')
                
                # First set up the figure, the axis, and the plot element we want to animate
                fig = plt.figure()
                ax = plt.axes(xlim=(200,500), ylim=(0,900))
                line, = ax.plot([], [], lw=2)
                
                fx = xLP_f
                fy = yLP_f
                xNew = tsXLeftPaw_inter
                yNew = tsYRightPaw_inter
                
                # call the animator.  blit=True means only re-draw the parts that have changed.
                anim = animation.FuncAnimation(fig, animate, init_func=init,
                                               frames=len(x)-1, interval=20, blit=True)
                
#                fx = xRP_f
#                fy = yRP_f
#                xNew = tsXRightPaw_inter
#                yNew = tsYRightPaw_inter
#                
#                anim = animation.FuncAnimation(fig, animate, init_func=init,
#                                               frames=len(xNew), interval=20, blit=True)
                
                # save the animation as an mp4.  This requires ffmpeg or mencoder to be
                # installed.  The extra_args ensure that the x264 codec is used, so that
                # the video can be embedded in html5.  You may need to adjust this for
                # your system: for more information, see
                # http://matplotlib.sourceforge.net/api/animation_api.html
                anim.save(outDir + 'groom/' + file[:-4]+'.mp4', fps=15, extra_args=['-vcodec', 'libx264'])
                
                plt.close()

                
                