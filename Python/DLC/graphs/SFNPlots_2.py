#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 17:09:32 2019

@author: kkrista
"""

import matplotlib.pyplot as plt
import matplotlib.text as txt
import numpy as np

rows = 3
cols = 2

lrange = 0
urange = 15

N = leftPaw_fft.size

fig, axs = plt.subplots(rows,cols,figsize=(15.6,8),dpi=300)
#fig.suptitle('Grooming Movements',size=32)
line1, = axs[0,0].plot(time,interLeftPaw[0],'b')
line1.set_linewidth(4)
line1a, = axs[0,0].plot([8.05,8.05],[300,350],'k')
axs[0,0].annotate("50 pixels",
            xy=(8.05,325), xycoords='data',
            xytext=(2,0), textcoords='offset points',)
#line1a, = axs[0,0].plot([8.05,8.05],[250,300],'k')
#axs[0,0].annotate("50 pixels",
#            xy=(8.05,275), xycoords='data',
#            xytext=(2,0), textcoords='offset points',)
axs[0,0].grid(b=True,which='major',axis='x',linestyle='-.')
axs[0,0].set_ylim(150,400) #grooming
#axs[0,0].set_ylim(217,467) #abmov
axs[0,0].set_yticklabels([])
axs[0,0].set_xticklabels([])
#axs[0,0].set_title('Left Paw',size=26)
#axs[0,0].set_ylabel('x Coordinate of Pixels',size=20)
#
line2, = axs[1,0].plot(time,interLeftPaw[1],'b')
line2.set_linewidth(4)
line2a, = axs[1,0].plot([8.05,8.05],[350,400],'k')
axs[1,0].annotate("50 pixels",
            xy=(8.05,375), xycoords='data',
            xytext=(2,0), textcoords='offset points',)
#line2a, = axs[1,0].plot([8.05,8.05],[700,750],'k')
#axs[1,0].annotate("50 pixels",
#            xy=(8.05,725), xycoords='data',
#            xytext=(2,0), textcoords='offset points',)
axs[1,0].grid(b=True,which='major',axis='x',linestyle='-.')
axs[1,0].set_ylim(293,543) #grooming
#axs[1,0].set_ylim(525,775) #abmov
axs[1,0].set_yticklabels([])
axs[1,0].set_xticklabels([])
#axs[1,0].set_ylabel('y Coordinate of Pixels',size=20)


line3, = axs[2,0].plot(time,ED_Left,'b')
line3.set_linewidth(4)
line3a, = axs[2,0].plot([8.05,8.05],[75,125],'k')
axs[2,0].annotate("50 pixels",
            xy=(8.05,100), xycoords='data',
            xytext=(2,0), textcoords='offset points',)
#line3a, = axs[2,0].plot([8.05,8.05],[100,150],'k')
#axs[2,0].annotate("50 pixels",
#            xy=(8.05,125), xycoords='data',
#            xytext=(2,0), textcoords='offset points',)
axs[2,0].grid(b=True,which='major',axis='x',linestyle='-.')
axs[2,0].set_ylim(0,200)
axs[2,0].set_yticklabels([])
#axs[2,0].set_ylabel('Euclidean Distance from Nose',size=20)
#axs[2,0].set_xlabel('Time (s)',size=20)


line4, = axs[0,1].plot(time,interRightPaw[0],'g')
line4.set_linewidth(4)
axs[0,1].grid(b=True,which='major',axis='x',linestyle='-.')
axs[0,1].set_ylim(100,350) #grooming
#axs[0,1].set_ylim(182,432) #abmov
axs[0,1].set_yticklabels([])
axs[0,1].set_xticklabels([])
#axs[0,1].set_title('Right Paw',size=26)


line5, = axs[1,1].plot(time,interRightPaw[1],'g')
line5.set_linewidth(4)
axs[1,1].grid(b=True,which='major',axis='x',linestyle='-.')
axs[1,1].set_ylim(296,546) #grooming
#axs[1,1].set_ylim(550,800) #abmov
axs[1,1].set_yticklabels([])
axs[1,1].set_xticklabels([])


line6,=axs[2,1].plot(time,ED_Right,'g')
line6.set_linewidth(4)
axs[2,1].grid(b=True,which='major',axis='x',linestyle='-.')
axs[2,1].set_ylim(0,200)
axs[2,1].set_yticklabels([])

#axs[2,1].set_xlabel('Time (s)',size=20)
fig.tight_layout()
fig.subplots_adjust(top=0.8,hspace=0.3)
fig.savefig('/Users/kkrista/Desktop/grooming_ED.pdf')

