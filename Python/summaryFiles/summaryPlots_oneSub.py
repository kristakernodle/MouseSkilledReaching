#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 18:17:34 2019

@author: Krista
"""
import os
import matplotlib.pyplot as plt
import numpy as np

animalDir = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/'

# Initialize Variables
allAnimals=[]
allFolders = os.listdir(animalDir)

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
    
    
    # Trials
    y = [float(i) for i in trials]
    y = [int(i) for i in y]
    y = np.ma.array(y)
    y_masked = np.ma.masked_where(y > 990, y)
    
    fig, ax = plt.subplots()
    ax.scatter(x,y_masked)
    ax.set(xlabel='Training Day',ylabel='Count', title=animal+' Number of Trials')
    ax.set_xticklabels(x,rotation=60,ha='right')
    plt.tight_layout()
    
    fig.savefig(currAnDir + animal + '_numTrials.pdf')
    plt.close()
    
    
    # Reaches
    y = [float(i) for i in reaches]
    y = [int(i) for i in y]
    y = np.ma.array(y)
    y_masked = np.ma.masked_where(y > 990, y)
    
    fig, ax = plt.subplots()
    ax.scatter(x,y_masked)
    ax.set(xlabel='Training Day',ylabel='Count', title=animal+' Number of Reaches')
    ax.set_xticklabels(x,rotation=60,ha='right')
    plt.tight_layout()
    
    fig.savefig(currAnDir + animal + '_numReaches.pdf')
    plt.close()
    
    # Number of Abnormal Movements
    y = [float(i) for i in numAbMov]
    y = [int(i) for i in y]
    y = np.ma.array(y)
    y_masked = np.ma.masked_where(y > 990, y)

    fig, ax = plt.subplots()
    ax.scatter(x,y_masked)
    ax.set(xlabel='Training Day',ylabel='Count', title=animal+' Number of Trials with Abnormal Movements')
    ax.set_xticklabels(x,rotation=60,ha='right')
    plt.tight_layout()
    
    fig.savefig(currAnDir + animal + '_numAbMov.pdf')
    plt.close()
    
    # Number of Grooming Bouts
    y = [float(i) for i in numGroom]
    y = [int(i) for i in y]
    y = np.ma.array(y)
    y_masked = np.ma.masked_where(y > 990, y)
    
    fig, ax = plt.subplots()
    ax.scatter(x,y_masked)
    ax.set(xlabel='Training Day',ylabel='Count', title=animal+' Number of Trials with Grooming')
    ax.set_xticklabels(x,rotation=60,ha='right')
    plt.tight_layout()
    
    fig.savefig(currAnDir + animal + '_numGroom.pdf')
    plt.close()
    
    # First Success
    y = [float(i) for i in firstSuc]
    y = np.ma.array(y)
    y_masked = np.ma.masked_where(y > 990, y)

    fig, ax = plt.subplots()
    ax.scatter(x,y_masked)
    ax.set(xlabel='Training Day',ylabel='Percent of Trials', title=animal+' First Success Rate')
    ax.set_xticklabels(x,rotation=60,ha='right')
    plt.tight_layout()
    
    fig.savefig(currAnDir + animal + '_firstSuc.pdf')
    plt.close()
    
    # Any Success
    y = [float(i) for i in anySuc]
    y = np.ma.array(y)
    y_masked = np.ma.masked_where(y > 990, y)
    
    fig, ax = plt.subplots()
    ax.scatter(x,y_masked)
    ax.set(xlabel='Training Day',ylabel='Percent of Trials', title=animal+' Any Success Rate')
    ax.set_xticklabels(x,rotation=60,ha='right')
    plt.tight_layout()
    
    fig.savefig(currAnDir + animal + '_anySuc.pdf')
    plt.close()
    
    # Percent Abnormal Movements
    y = [float(i) for i in percAbMov]
    y = np.ma.array(y)
    y_masked = np.ma.masked_where(y > 990, y)
    
    fig, ax = plt.subplots()
    ax.scatter(x,y_masked)
    ax.set(xlabel='Training Day',ylabel='Percent of Trials', title=animal+' Percent Trials with Abnormal Movements')
    ax.set_xticklabels(x,rotation=60,ha='right')
    plt.tight_layout()
    
    fig.savefig(currAnDir + animal + '_percAbMov.pdf')
    plt.close()
    
    # Percent Grooming
    y = [float(i) for i in percGroom]
    y = np.ma.array(y)
    y_masked = np.ma.masked_where(y > 990, y)
    
    fig, ax = plt.subplots()
    ax.scatter(x,y_masked)
    ax.set(xlabel='Training Day',ylabel='Percent of Trials', title=animal+' Percent Trials with Grooming')
    ax.set_xticklabels(x,rotation=60,ha='right')
    plt.tight_layout()
    
    fig.savefig(currAnDir + animal + '_percGroom.pdf')
    plt.close()

                
        
        
    
    
    