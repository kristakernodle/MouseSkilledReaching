#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 18:17:34 2019

@author: Krista
"""
import os
import matplotlib.pyplot as plt
import numpy as np
import LLC_animalInfo

animalDir = '/Volumes/SharedX/Neuro-Leventhal/data/LawrenceLab_Collab/'

# Initialize Variables
allAnimals=[]
allFolders = os.listdir(animalDir)

fig1, trialPlot = plt.subplots()
fig2, reachPlot = plt.subplots()
fig3, firstSucPlot = plt.subplots()
fig4, anySucPlot = plt.subplots()

baseArray = np.ma.array([999]*20)

meanExp_trials = np.ma.masked_where(baseArray > 990,baseArray)
meanExp_reaches = np.ma.masked_where(baseArray > 990,baseArray)
meanExp_firstSuc = np.ma.masked_where(baseArray > 990,baseArray)
meanExp_anySuc = np.ma.masked_where(baseArray > 990,baseArray)

meanSham_trials = np.ma.masked_where(baseArray > 990,baseArray)
meanSham_reaches = np.ma.masked_where(baseArray > 990,baseArray)
meanSham_firstSuc = np.ma.masked_where(baseArray > 990,baseArray)
meanSham_anySuc = np.ma.masked_where(baseArray > 990,baseArray)

# Get all animal folders
for file in allFolders:
    if 'et' in file[:2]:
        # Collect the files that have 'et', denoting 'Ear Tag' into one list
        allAnimals.append(file)

allAnimals.sort()

for animal in allAnimals:

    print(animal)
    
    # Define training directory for animal
    currAnDir=animalDir+animal+'/'
    
    if not os.path.isdir(currAnDir):
        # If there is no 'Training' directory, skip this animal
        continue
    
    animalDetails = LLC_animalInfo.animals[animal]
    
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

    for item in summary:
        
        item = item.split(',')
        tDays.append(item[0])
        trials.append(item[1])
        reaches.append(item[2])
        firstSuc.append(item[3])
        anySuc.append(item[4])
    
    if animal == 'et7126':
        plotX = tDays
    
    x = tDays

    if animalDetails[0] in 'sham':
        groupColor = 'b'
        
    elif animalDetails[0] in 'exp':
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
        
    if animal == 'et7129':
        meanExp_trials[0:10] = np.ma.mean([meanExp_trials[0:10],y_masked],axis=0)
    elif animal == 'et7132':
        meanSham_trials[:-1] = np.ma.mean([meanSham_trials[:-1],y_masked],axis=0)
    else:
        if animalDetails[0] in 'sham':
            meanSham_trials = np.ma.mean([meanSham_trials,y_masked],axis=0)
        elif animalDetails[0] in 'exp':
            meanExp_trials = np.ma.mean([meanExp_trials,y_masked],axis=0)

    trialPlot.scatter(x,y_masked,c=groupColor,marker=subMark)
    trialPlot.set(xlabel='Training Day',ylabel='Count', title='Number of Trials')
    trialPlot.set_xticklabels(x,rotation=60,ha='right')
    plt.tight_layout()

    # Reaches
    y = [float(i) for i in reaches]
    y = [int(i) for i in y]
    y = np.ma.array(y)
    y_masked = np.ma.masked_where(y > 990, y)
    
    if animal == 'et7129':
        meanExp_reaches[0:10] = np.ma.mean([meanExp_reaches[0:10],y_masked],axis=0)
    elif animal == 'et7132':
        meanSham_reaches[:-1] = np.ma.mean([meanSham_reaches[:-1],y_masked],axis=0)
    else:
        if animalDetails[0] in 'sham':
            meanSham_reaches = np.ma.mean([meanSham_reaches,y_masked],axis=0)
        elif animalDetails[0] in 'exp':
            meanExp_treaches = np.ma.mean([meanExp_reaches,y_masked],axis=0)

    reachPlot.scatter(x,y_masked,c=groupColor,marker=subMark)
    reachPlot.set(xlabel='Training Day',ylabel='Count', title='Number of Reaches')
    reachPlot.set_xticklabels(x,rotation=60,ha='right')
    plt.tight_layout()
    
    # First Success
    y = [float(i) for i in firstSuc]
    y = np.ma.array(y)
    y_masked = np.ma.masked_where(y > 990, y)

    if animal == 'et7129':
        meanExp_firstSuc[0:10] = np.ma.mean([meanExp_firstSuc[0:10],y_masked],axis=0)
    elif animal == 'et7132':
        meanSham_firstSuc[:-1] = np.ma.mean([meanSham_firstSuc[:-1],y_masked],axis=0)
    else:
        if animalDetails[0] in 'sham':
            meanSham_firstSuc = np.ma.mean([meanSham_firstSuc,y_masked],axis=0)
        elif animalDetails[0] in 'exp':
            meanExp_firstSuc = np.ma.mean([meanExp_firstSuc,y_masked],axis=0)
        
    firstSucPlot.scatter(x,y_masked,c=groupColor,marker=subMark)
    firstSucPlot.set(xlabel='Training Day',ylabel='Percent of Trials', title='First Success Rate')
    firstSucPlot.set_xticklabels(x,rotation=60,ha='right')
    plt.tight_layout()

    # Any Success
    y = [float(i) for i in anySuc]
    y = np.ma.array(y)
    y_masked = np.ma.masked_where(y > 990, y)
    
    if animal == 'et7129':
        meanExp_anySuc[0:10] = np.ma.mean([meanExp_anySuc[0:10],y_masked],axis=0)
    elif animal == 'et7132':
        meanSham_anySuc[:-1] = np.ma.mean([meanSham_anySuc[:-1],y_masked],axis=0)
    else:
        if animalDetails[0] in 'sham':
            meanSham_anySuc = np.ma.mean([meanSham_anySuc,y_masked],axis=0)
        elif animalDetails[0] in 'exp':
            meanExp_anySuc = np.ma.mean([meanExp_anySuc,y_masked],axis=0)
        
    anySucPlot.scatter(x,y_masked,c=groupColor,marker=subMark)
    anySucPlot.set(xlabel='Training Day',ylabel='Percent of Trials', title='Any Success Rate')
    anySucPlot.set_xticklabels(x,rotation=60,ha='right')
    plt.tight_layout()

x = plotX
trialPlot.plot(x,meanSham_trials,c='b')
trialPlot.plot(x,meanExp_trials,c='r')

reachPlot.plot(x,meanSham_reaches,c='b')
reachPlot.plot(x,meanExp_reaches,c='r')

firstSucPlot.plot(x,meanSham_firstSuc,c='b')
firstSucPlot.plot(x,meanExp_firstSuc,c='r')

anySucPlot.plot(x,meanSham_anySuc,c='b')
anySucPlot.plot(x,meanExp_anySuc,c='r')

fig1.savefig(animalDir + 'all_numTrials.pdf')
fig2.savefig(animalDir + 'all_numReaches.pdf')
fig3.savefig(animalDir + 'all_firstSuccess.pdf')
fig4.savefig(animalDir + 'all_anySuccess.pdf')

                
        
        
    
    
    