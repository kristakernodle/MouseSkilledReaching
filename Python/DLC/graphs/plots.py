#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 17:09:32 2019

@author: kkrista
"""

import matplotlib.pyplot as plt

def plotFilename(csvFile,beh):
    if beh == 'abMovFrames':
        saveBeh = 'abMov'
    filename = csvFile.split('D')[0]
    return '_'.join([filename,saveBeh])
    
def plotTitle(mouse,day,reach,beh):
    vidID = day.split('_')
    vidID.append(reach)
    vidID = '_'.join(vidID[1:])
    if beh == 'abMovFrames':
        behID = 'Abnormal Movement'
    else:
        behID = 'Grooming'
    return ', '.join([mouse,vidID,behID])
    
def plotPixels(outDir,filename,title,time, interLeftPaw, interRightPaw, ED_Left, ED_Right, leftPaw_fft, figSize_width = 11, figSize_length = 8.5):
    
    ## Generate Plot with axs representing the axes
    fig, axs = plt.subplots(3,2,figsize=(figSize_width,figSize_length),dpi=300)
    
    line1, = axs[0,0].plot(time,interLeftPaw[0],'b')
    line1.set_linewidth(4)
    axs[0,0].grid(b=True,which='major',axis='x',linestyle='-.')
    axs[0,0].set_yticklabels([])
    axs[0,0].set_xticklabels([])
    axs[0,0].set_title('Left Paw',size=16)
    axs[0,0].set_ylabel('x Pixels',size=12)
    
    line2, = axs[1,0].plot(time,interLeftPaw[1],'b')
    line2.set_linewidth(4)
    axs[1,0].grid(b=True,which='major',axis='x',linestyle='-.')
    axs[1,0].set_yticklabels([])
    axs[1,0].set_xticklabels([])
    axs[1,0].set_ylabel('y Pixels',size=12)
    
    
    line3, = axs[2,0].plot(time,ED_Left,'b')
    line3.set_linewidth(4)
    axs[2,0].grid(b=True,which='major',axis='x',linestyle='-.')
    axs[2,0].set_yticklabels([])
    axs[2,0].set_xlabel('Time (s)',size=12)
    axs[2,0].set_ylabel('ED Pixels',size=12)
    
    line4, = axs[0,1].plot(time,interRightPaw[0],'g')
    line4.set_linewidth(4)
    axs[0,1].grid(b=True,which='major',axis='x',linestyle='-.')
    axs[0,1].set_yticklabels([])
    axs[0,1].set_xticklabels([])
    axs[0,1].set_title('Right Paw',size=16)
    
    
    line5, = axs[1,1].plot(time,interRightPaw[1],'g')
    line5.set_linewidth(4)
    axs[1,1].grid(b=True,which='major',axis='x',linestyle='-.')
    axs[1,1].set_yticklabels([])
    axs[1,1].set_xticklabels([])
    
    
    line6,=axs[2,1].plot(time,ED_Right,'g')
    line6.set_linewidth(4)
    axs[2,1].grid(b=True,which='major',axis='x',linestyle='-.')
    axs[2,1].set_yticklabels([])
    axs[2,1].set_xlabel('Time (s)',size=12)
    
    fig.tight_layout()
    fig.suptitle(title,size=20)
    fig.subplots_adjust(top=0.88)
    fig.savefig(outDir+filename+'_timeTraces.pdf')
    
    plt.close()

