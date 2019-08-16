#!/usr/bin/env python3

"""
Created on Thu Jan 24 15:57:44 2019

@author: kkrista
"""

import math

def readDLC(F):
    
    leftPaw = []
    rightPaw = []
    nose =[]
    pellet = []
    
    
    with open(F) as f:
        obj = f.read().splitlines()
        obj = obj[3:]
        
        for item in obj:
            item = item.split(',')
            
            leftPaw.append([float(item[1]),float(item[2]),float(item[3])])
            rightPaw.append(item[4:7])
            nose.append(item[7:10])
            pellet.append(item[10:])
        
        return leftPaw, rightPaw, nose, pellet
    
def ptDist(pt1,pt2):
    
    dist = math.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)
    
    return dist

def frange(start,stop,step):
    i = start
    out = []
    while i < stop:
        out.append(i)
        i += step
    return out