#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 18:17:34 2019

@author: Krista
"""
import os
import matplotlib.pyplot as plt
import numpy as np
import animalInfo

animalDir = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/'

# Initialize Variables
allAnimals=[]
allFolders = os.listdir(animalDir)

fig1, trialPlot = plt.subplots()
fig2, reachPlot = plt.subplots()
fig3, firstSucPlot = plt.subplots()
fig4, anySucPlot = plt.subplots()
fig5, abMovPlot = plt.subplots()
fig6, groomPlot = plt.subplots()
fig7, percAbMovPlot = plt.subplots()
fig8, percGroomPlot = plt.subplots()

baseArray = np.ma.array([999]*21)

meanKO_trials = np.ma.masked_where(baseArray > 990,baseArray)
meanKO_reaches = np.ma.masked_where(baseArray > 990,baseArray)
meanKO_firstSuc = np.ma.masked_where(baseArray > 990,baseArray)
meanKO_anySuc = np.ma.masked_where(baseArray > 990,baseArray)
meanKO_abMov = np.ma.masked_where(baseArray > 990,baseArray)
meanKO_groom = np.ma.masked_where(baseArray > 990,baseArray)
meanKO_percAbMov = np.ma.masked_where(baseArray > 990,baseArray)
meanKO_percGroom = np.ma.masked_where(baseArray > 990,baseArray)

meanWT_trials = np.ma.masked_where(baseArray > 990,baseArray)
meanWT_reaches = np.ma.masked_where(baseArray > 990,baseArray)
meanWT_firstSuc = np.ma.masked_where(baseArray > 990,baseArray)
meanWT_anySuc = np.ma.masked_where(baseArray > 990,baseArray)
meanWT_abMov = np.ma.masked_where(baseArray > 990,baseArray)
meanWT_groom = np.ma.masked_where(baseArray > 990,baseArray)
meanWT_percAbMov = np.ma.masked_where(baseArray > 990,baseArray)
meanWT_percGroom = np.ma.masked_where(baseArray > 990,baseArray)

# Get all animal folders
for file in allFolders:
    if 'et' in file[:2]:
        # Collect the files that have 'et', denoting 'Ear Tag' into one list
        allAnimals.append(file)

allAnimals.sort()

for animal in allAnimals:
    
    print(animal)
    
    # Define training directory for animal
    currAnDir=animalDir+animal+'/Training/'
    
    if not os.path.isdir(currAnDir):
        # If there is no 'Training' directory, skip this animal
        continue
    
    animalDetails = animalInfo.animals[animal]
    
    allFiles = os.listdir(currAnDir)
    summaryStats = [file for file in allFiles if file.endswith(animal + '.csv')]
        
    with open(currAnDir + summaryStats[0]) as f:
        summary = f.read().splitlines()
        labels = summary[0].split(',')
        summary = summary[1:]
    
    tDays = []
    trials = []
    reaches = []
    firstSuc = []
    anySuc = []
    numAbMov = []
    percAbMov = []
    numGroom = []
    percGroom = []

    for item in summary:
        
        item = item.split(',')
        tDays.append(item[0])
        trials.append(item[1])
        reaches.append(item[2])
        firstSuc.append(item[3])
        anySuc.append(item[4])
        numAbMov.append(item[5])
        percAbMov.append(item[6])
        numGroom.append(item[7])
        percGroom.append(item[8])
        
    x = tDays

    if animalDetails[0] in 'WT':
        groupColor = 'b'
        
    elif animalDetails[0] in 'KO':
        groupColor = 'r'
    else:
        print('animal details need to be updated')
        continue

    subMark = animalDetails[3]
    
    # Trials
    y = [float(i) for i in trials]
    y = [int(i) for i in y]
    y = np.ma.array(y)
    y_masked = np.ma.masked_where(y > 990, y)
    
    if animalDetails[0] in 'WT':
        meanWT_trials = np.ma.mean([meanWT_trials,y_masked],axis=0)
    elif animalDetails[0] in 'KO':
        meanKO_trials = np.ma.mean([meanKO_trials,y_masked],axis=0)

    trialPlot.scatter(x,y_masked,c=groupColor,marker=subMark)
    trialPlot.set(xlabel='Training Day',ylabel='Count', title='Number of Trials')
    trialPlot.set_xticklabels(x,rotation=60,ha='right')
    plt.tight_layout()

    # Reaches
    y = [float(i) for i in reaches]
    y = [int(i) for i in y]
    y = np.ma.array(y)
    y_masked = np.ma.masked_where(y > 990, y)
    
    if animalDetails[0] in 'WT':
        meanWT_reaches = np.ma.mean([meanWT_reaches,y_masked],axis=0)
    elif animalDetails[0] in 'KO':
        meanKO_reaches = np.ma.mean([meanKO_reaches,y_masked],axis=0)

    reachPlot.scatter(x,y_masked,c=groupColor,marker=subMark)
    reachPlot.set(xlabel='Training Day',ylabel='Count', title='Number of Reaches')
    reachPlot.set_xticklabels(x,rotation=60,ha='right')
    plt.tight_layout()
    
    # Number of Abnormal Movements
    y = [float(i) for i in numAbMov]
    y = [int(i) for i in y]
    y = np.ma.array(y)
    y_masked = np.ma.masked_where(y > 990, y)

    if animalDetails[0] in 'WT':
        meanWT_abMov = np.ma.mean([meanWT_abMov,y_masked],axis=0)
    elif animalDetails[0] in 'KO':
        meanKO_abMov = np.ma.mean([meanKO_abMov,y_masked],axis=0)

    abMovPlot.scatter(x,y_masked,c=groupColor,marker=subMark)
    abMovPlot.set(xlabel='Training Day',ylabel='Count', title='Number of Trials with Abnormal Movements')
    abMovPlot.set_xticklabels(x,rotation=60,ha='right')
    plt.tight_layout()
    
    # Number of Grooming Bouts
    y = [float(i) for i in numGroom]
    y = [int(i) for i in y]
    y = np.ma.array(y)
    y_masked = np.ma.masked_where(y > 990, y)
    
    if animalDetails[0] in 'WT':
        meanWT_groom = np.ma.mean([meanWT_groom,y_masked],axis=0)
    elif animalDetails[0] in 'KO':
        meanKO_groom = np.ma.mean([meanKO_groom,y_masked],axis=0)
    
    groomPlot.scatter(x,y_masked,c=groupColor,marker=subMark)
    groomPlot.set(xlabel='Training Day',ylabel='Count', title='Number of Trials with Grooming')
    groomPlot.set_xticklabels(x,rotation=60,ha='right')
    plt.tight_layout()
    
    # First Success
    y = [float(i) for i in firstSuc]
    y = np.ma.array(y)
    y_masked = np.ma.masked_where(y > 990, y)

    if animalDetails[0] in 'WT':
        meanWT_firstSuc = np.ma.mean([meanWT_firstSuc,y_masked],axis=0)
    elif animalDetails[0] in 'KO':
        meanKO_firstSuc = np.ma.mean([meanKO_firstSuc,y_masked],axis=0)
        
    firstSucPlot.scatter(x,y_masked,c=groupColor,marker=subMark)
    firstSucPlot.set(xlabel='Training Day',ylabel='Percent of Trials', title='First Success Rate')
    firstSucPlot.set_xticklabels(x,rotation=60,ha='right')
    plt.tight_layout()

    # Any Success
    y = [float(i) for i in anySuc]
    y = np.ma.array(y)
    y_masked = np.ma.masked_where(y > 990, y)
    
    if animalDetails[0] in 'WT':
        meanWT_anySuc = np.ma.mean([meanWT_anySuc,y_masked],axis=0)
    elif animalDetails[0] in 'KO':
        meanKO_anySuc = np.ma.mean([meanKO_anySuc,y_masked],axis=0)
        
    anySucPlot.scatter(x,y_masked,c=groupColor,marker=subMark)
    anySucPlot.set(xlabel='Training Day',ylabel='Percent of Trials', title='Any Success Rate')
    anySucPlot.set_xticklabels(x,rotation=60,ha='right')
    plt.tight_layout()
    
    # Percent Abnormal Movements
    y = [float(i) for i in percAbMov]
    y = np.ma.array(y)
    y_masked = np.ma.masked_where(y > 990, y)
    
    if animalDetails[0] in 'WT':
        meanWT_percAbMov = np.ma.mean([meanWT_percAbMov ,y_masked],axis=0)
    elif animalDetails[0] in 'KO':
        meanKO_percAbMov  = np.ma.mean([meanKO_percAbMov ,y_masked],axis=0)
        
    percAbMovPlot.scatter(x,y_masked,c=groupColor,marker=subMark)
    percAbMovPlot.set(xlabel='Training Day',ylabel='Percent of Trials', title='Percent Trials with Abnormal Movements')
    percAbMovPlot.set_xticklabels(x,rotation=60,ha='right')
    plt.tight_layout()
    
    # Percent Grooming
    y = [float(i) for i in percGroom]
    y = np.ma.array(y)
    y_masked = np.ma.masked_where(y > 990, y)
    
    if animalDetails[0] in 'WT':
        meanWT_percGroom = np.ma.mean([meanWT_percGroom ,y_masked],axis=0)
    elif animalDetails[0] in 'KO':
        meanKO_percGroom  = np.ma.mean([meanKO_percGroom ,y_masked],axis=0)

    percGroomPlot.scatter(x,y_masked,c=groupColor,marker=subMark)
    percGroomPlot.set(xlabel='Training Day',ylabel='Percent of Trials', title='Percent Trials with Grooming')
    percGroomPlot.set_xticklabels(x,rotation=60,ha='right')
    plt.tight_layout()
    
trialPlot.plot(x,meanWT_trials,c='b')
trialPlot.plot(x,meanKO_trials,c='r')

reachPlot.plot(x,meanWT_reaches,c='b')
reachPlot.plot(x,meanKO_reaches,c='r')

firstSucPlot.plot(x,meanWT_firstSuc,c='b')
firstSucPlot.plot(x,meanKO_firstSuc,c='r')

anySucPlot.plot(x,meanWT_anySuc,c='b')
anySucPlot.plot(x,meanKO_anySuc,c='r')

abMovPlot.plot(x,meanWT_abMov,c='b')
abMovPlot.plot(x,meanKO_abMov,c='r')

groomPlot.plot(x,meanWT_groom,c='b')
groomPlot.plot(x,meanKO_groom,c='r')

percAbMovPlot.plot(x,meanWT_percAbMov,c='b')
percAbMovPlot.plot(x,meanKO_percAbMov,c='r')

percGroomPlot.plot(x,meanWT_percGroom,c='b')
percGroomPlot.plot(x,meanKO_percGroom,c='r')

fig1.savefig(animalDir + 'all_numTrials.pdf')
fig2.savefig(animalDir + 'all_numReaches.pdf')
fig3.savefig(animalDir + 'all_firstSuccess.pdf')
fig4.savefig(animalDir + 'all_anySuccess.pdf')
fig5.savefig(animalDir + 'all_abnormalMovements.pdf')
fig6.savefig(animalDir + 'all_grooming.pdf')
fig7.savefig(animalDir + 'all_percentAbMov.pdf')
fig8.savefig(animalDir + 'all_percentGroom.pdf')

                
        
        
    
    
    