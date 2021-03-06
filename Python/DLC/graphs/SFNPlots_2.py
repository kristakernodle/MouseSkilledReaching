#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 17:09:32 2019

@author: kkrista
"""

import matplotlib.pyplot as plt

def plotPixels(time, interLeftPaw, interRightPaw, ED_Left, ED_Right, leftPaw_fft, figSize_width = 11, figSize_length = 8.5):
    
    ## Generate Plot with axs representing the axes
    fig, axs = plt.subplots(3,2,figsize=(figSize_width,figSize_length),dpi=300)
    
    line1, = axs[0,0].plot(time,interLeftPaw[0],'b')
    line1.set_linewidth(4)
    axs[0,0].grid(b=True,which='major',axis='x',linestyle='-.')
    axs[0,0].set_yticklabels([])
    axs[0,0].set_xticklabels([])
    #axs[0,0].set_title('Left Paw',size=26)
    #axs[0,0].set_ylabel('x Coordinate of Pixels',size=20)
    #
    line2, = axs[1,0].plot(time,interLeftPaw[1],'b')
    line2.set_linewidth(4)
    axs[1,0].grid(b=True,which='major',axis='x',linestyle='-.')
    axs[1,0].set_yticklabels([])
    axs[1,0].set_xticklabels([])
    #axs[1,0].set_ylabel('y Coordinate of Pixels',size=20)
    
    
    line3, = axs[2,0].plot(time,ED_Left,'b')
    axs[2,0].grid(b=True,which='major',axis='x',linestyle='-.')
    axs[2,0].set_yticklabels([])
    
    
    
    line4, = axs[0,1].plot(time,interRightPaw[0],'g')
    line4.set_linewidth(4)
    axs[0,1].grid(b=True,which='major',axis='x',linestyle='-.')
    axs[0,1].set_yticklabels([])
    axs[0,1].set_xticklabels([])
    #axs[0,1].set_title('Right Paw',size=26)
    
    
    line5, = axs[1,1].plot(time,interRightPaw[1],'g')
    line5.set_linewidth(4)
    axs[1,1].grid(b=True,which='major',axis='x',linestyle='-.')
    axs[1,1].set_yticklabels([])
    axs[1,1].set_xticklabels([])
    
    
    line6,=axs[2,1].plot(time,ED_Right,'g')
    line6.set_linewidth(4)
    axs[2,1].grid(b=True,which='major',axis='x',linestyle='-.')
    axs[2,1].set_yticklabels([])
    
    #axs[2,1].set_xlabel('Time (s)',size=20)
    fig.tight_layout()
    
    fig.subplots_adjust(top=0.8,hspace=0.3)
#    fig.savefig('/Users/kkrista/Desktop/grooming_ED.pdf')

