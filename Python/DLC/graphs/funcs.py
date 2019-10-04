#!/usr/bin/env python3

"""
Created on Thu Jan 24 15:57:44 2019

@author: kkrista
"""

import math
from scipy import signal
import numpy as np
from scipy import interpolate

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
    
    sos = signal.butter(1, 5,'highpass',fs=100,output='sos')
    y = signal.sosfilt(sos,xn)
    
    return y

def interpolData(x,data):
    x_masked = np.ma.array(x)
    x_masked.mask = data.mask
    
    data_comp = data.compressed()
    x_comp = x_masked.compressed()
    
    xNew = np.linspace(x_comp[0],x_comp[-1],num = len(x), endpoint=True)
#    yNew = interpolate.pchip_interpolate(x_comp,data_comp,x)
#    fx = interpolate.PchipInterpolator(x_comp, data_comp, axis=0, extrapolate=None)
#    tck = interpolate.splrep(x_comp, data_comp, s=0)
#    yNew = interpolate.splev(xNew, tck, der=0)
#    yDer = interpolate.splev(xNew, tck, der=1)
    fx = interpolate.interp1d(x_comp,data_comp,kind = 'cubic')
    
    yNew = fx(xNew)
#    fxNew = fx(xNew)
    return xNew, yNew, fx

def maskData(data):
    
    # Get the distance between each point and mask outliers
    mask = []
    for index in range(0,len(data)):
        if index == 0:
            if ptDist(data[index],data[index+1]) > 50:
                mask.append(True)
            else:
                mask.append(False)
        elif index == len(data)-1:
            if ptDist(data[index-1],data[index]) > 50:
                mask.append(True)
            else:
                mask.append(False)
        elif mask[index-1] == True and ptDist(data[index],data[index+1]) > 50:
            mask.append(True)
        elif ptDist(data[index-1],data[index]) > 50:
            mask.append(True)
        else:
            mask.append(False) 
    
    maskData = np.ma.array(data)
    
    # Define p values for body parts with mask based on p value

    pData_masked = np.ma.masked_where(maskData[:,-1] < 0.75, maskData[:,2])
    
    mask = [any(tup) for tup in zip(mask,pData_masked.mask)]
    
    xData_masked = maskData[:,0]
    yData_masked = maskData[:,1]
    xData_masked.mask = mask
    yData_masked.mask = mask
    pData_masked.mask = mask
    
    return xData_masked, yData_masked, pData_masked
    


    
    
    
    
    
    
    
    
    
    
    