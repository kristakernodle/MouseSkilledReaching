#!/usr/bin/env python3

"""
Created on Thu Jan 24 15:57:44 2019

@author: kkrista
"""

import math
from scipy import signal

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
            rightPaw.append([float(item[4]),float(item[5]),float(item[6])])
            nose.append([float(item[7]),float(item[8]),float(item[9])])
            pellet.append([float(item[10]),float(item[11]),float(item[12])])
        
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

def filterFunc(xn):
    
    sos = signal.butter(3, 7,'highpass',fs=59.95,output='sos')
    y = signal.sosfilt(sos,xn)
    
    return y
    
    
    
    
    
    
    
    
    
    