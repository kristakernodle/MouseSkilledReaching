#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 06:13:15 2019

@author: Krista
"""

import pickle

dirDLC = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/DLCProcessing/currentDLCIter/'

# Load dictionaries
with open(dirDLC + 'combined_allData.pickle','rb') as pickleFile:
    interpData = pickle.load(pickleFile) 

with open(dirDLC + 'combined_fftData.pickle','rb') as pickleFile:
    fftData = pickle.load(pickleFile)
    
## Loop through interpData and plot x,y traces

behaviors = list(interpData.keys())

for beh in behaviors:
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
                    continue
                print('Data Loaded')
                
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
                
                
    
