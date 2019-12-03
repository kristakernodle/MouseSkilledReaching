#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 06:13:15 2019

@author: Krista
"""

import pickle
import matplotlib.pyplot as plt
import numpy as np

dirDLC = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/DLCProcessing/currentDLCIter/'

# Load dictionaries
with open(dirDLC + 'combined_allData.pickle','rb') as pickleFile:
    interpData = pickle.load(pickleFile) 

with open(dirDLC + 'combined_fftData.pickle','rb') as pickleFile:
    fftData = pickle.load(pickleFile)
    
## Loop through interpData and plot x,y traces

behaviors = list(interpData.keys())

fig = plt.figure(figsize=(8.5,90),dpi=300)

for beh in behaviors:
    if beh == 'groom':
        plotNum = 2
    else:
        plotNum = 1
    animals = list(interpData[beh].keys())
    for mouse in animals:
        allDays = list(interpData[beh][mouse].keys())
        for day in allDays:
            allReaches = list(interpData[beh][mouse][day].keys())
            for reach in allReaches:
                if reach == 'reaches':
                    continue
                try:
                    ED_Left = interpData[beh][mouse][day][reach]['interpData']['ED_Left']
                    ED_Right = interpData[beh][mouse][day][reach]['interpData']['ED_Right']
                    leftPaw = interpData[beh][mouse][day][reach]['interpData']['leftPaw']
                    rightPaw = interpData[beh][mouse][day][reach]['interpData']['rightPaw']
                    nose = interpData[beh][mouse][day][reach]['interpData']['nose']
                except:
                    plotNum += 2
                    continue
                
                ED_Left = [list(a) for a in ED_Left]
                ED_Left = list(zip(*ED_Left))
                ED_Right = [list(a) for a in ED_Right]
                ED_Right = list(zip(*ED_Right))
                leftPaw = [list(a) for a in leftPaw]
                leftPaw = list(zip(*leftPaw))
                rightPaw = [list(a) for a in rightPaw]
                rightPaw = list(zip(*rightPaw))
                nose = [list(a) for a in nose]
                nose = list(zip(*nose))
                
                blues = plt.get_cmap('Blues')
                greens = plt.get_cmap('Greens')
                greys = plt.get_cmap('Greys')
                
                ax = fig.add_subplot(29,2,plotNum)
                ax.set_title(beh+', '+day+', '+reach)
#                ax.set_xlim(100,600)
#                ax.set_ylim(200,900)
                xlp = []
                ylp = []
                xrp = []
                yrp = [] 
                for i in list(range(0,len(leftPaw[0]))):
                    nos_x = nose[0][i]
                    nos_y = nose[0][i]
                    lp_x = leftPaw[0][i]
                    lp_y = leftPaw[1][i]
                    rp_x = rightPaw[0][i]
                    rp_y = rightPaw[1][i]

                    xlp.append(lp_x-nos_x)
                    ylp.append(lp_y-nos_y)
                    xrp.append(rp_x-nos_x)
                    yrp.append(rp_y-nos_y)
                                
                for i in list(range(0,len(leftPaw[0])-1)):
                    ax.plot(xlp[i:i+2],ylp[i:i+2],color = blues(1 - float(i)/(len(leftPaw[0])-1)))
                    ax.plot(xrp[i:i+2],yrp[i:i+2],color = greens(1 - float(i)/(len(leftPaw[0])-1)))
                    ax.plot(0,0,'*',color = 'k')
                
                plotNum += 2
#fig.suptitle('Mean Power Analysis During '+ desc, size=10)
fig.tight_layout()
fig.subplots_adjust(top=0.98)               
fig.savefig('/Users/Krista/Desktop/noseOrig_xyTraces.pdf')
plt.close()
                
                
                
                
                
                
                
    
