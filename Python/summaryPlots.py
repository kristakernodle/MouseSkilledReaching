#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 18:17:34 2019

@author: Krista
"""
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import animalInfo

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
    
    for mouse in animalInfo.WT:
        mouse = 'et' + mouse
        if animal in mouse:
            geno = 'WT'
            break
    
    for mouse in animalInfo.KO:
        mouse = 'et' + mouse
        if animal in mouse:
            geno = 'KO'
            break
    
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
    print('Trials')
    y = [float(i) for i in trials]
    print('next line')
    y = [int(i) for i in y]
    mask = y == 999
    
    fig, ax = plt.subplots()
    ax.scatter(x[mask],y[mask])
    ax.set(xlabel='Training Day',ylabel='Count', title=animal+' Number of Trials')
    ax.set_xticklabels(x,rotation=60,ha='right')
    plt.tight_layout()
    
    fig.savefig(currAnDir + animal + '_numTrials.pdf')
    plt.close()
    
    
    # Reaches
    print('Reaches')
    y = [float(i) for i in reaches]
    y = [int(i) for i in y]
    mask = y == 999
    
    fig, ax = plt.subplots()
    ax.scatter(x[mask],y[mask])
    ax.set(xlabel='Training Day',ylabel='Count', title=animal+' Number of Reaches')
    ax.set_xticklabels(x,rotation=60,ha='right')
    plt.tight_layout()
    
    fig.savefig(currAnDir + animal + '_numReaches.pdf')
    plt.close()
    
    # Number of Abnormal Movements
    print('number ab mov')
    y = [float(i) for i in numAbMov]
    y = [int(i) for i in y]
    mask = y == 999

    fig, ax = plt.subplots()
    ax.scatter(x[mask],y[mask])
    ax.set(xlabel='Training Day',ylabel='Count', title=animal+' Number of Trials with Abnormal Movements')
    ax.set_xticklabels(x,rotation=60,ha='right')
    plt.tight_layout()
    
    fig.savefig(currAnDir + animal + '_numAbMov.pdf')
    plt.close()
    
    # Number of Grooming Bouts
    print('number grooming')
    y = [float(i) for i in numGroom]
    y = [int(i) for i in y]
    mask = y == 999
    
    fig, ax = plt.subplots()
    ax.scatter(x[mask],y[mask])
    ax.set(xlabel='Training Day',ylabel='Count', title=animal+' Number of Trials with Grooming')
    ax.set_xticklabels(x,rotation=60,ha='right')
    plt.tight_layout()
    
    fig.savefig(currAnDir + animal + '_numGroom.pdf')
    plt.close()
    
    # First Success
    print('first Suc')
    y = [float(i) for i in firstSuc]
    mask = y == 999

    fig, ax = plt.subplots()
    ax.scatter(x[mask],y[mask])
    ax.set(xlabel='Training Day',ylabel='Percent of Trials', title=animal+' First Success Rate')
    ax.set_xticklabels(x,rotation=60,ha='right')
    plt.tight_layout()
    
    fig.savefig(currAnDir + animal + '_firstSuc.pdf')
    plt.close()
    
    # Any Success
    print('any suc')
    y = [float(i) for i in anySuc]
    mask = y == 999
    
    fig, ax = plt.subplots()
    ax.scatter(x[mask],y[mask])
    ax.set(xlabel='Training Day',ylabel='Percent of Trials', title=animal+' Any Success Rate')
    ax.set_xticklabels(x,rotation=60,ha='right')
    plt.tight_layout()
    
    fig.savefig(currAnDir + animal + '_anySuc.pdf')
    plt.close()
    
    # Percent Abnormal Movements
    print('perc ab mov')
    y = [float(i) for i in percAbMov]
    mask = y == 999
    
    fig, ax = plt.subplots()
    ax.scatter(x[mask],y[mask])
    ax.set(xlabel='Training Day',ylabel='Percent of Trials', title=animal+' Percent Trials with Abnormal Movements')
    ax.set_xticklabels(x,rotation=60,ha='right')
    plt.tight_layout()
    
    fig.savefig(currAnDir + animal + '_percAbMov.pdf')
    plt.close()
    
    # Percent Grooming
    print('perc Groom')
    y = [float(i) for i in percGroom]
    mask = y == 999
    
    fig, ax = plt.subplots()
    ax.scatter(x[mask],y[mask])
    ax.set(xlabel='Training Day',ylabel='Percent of Trials', title=animal+' Percent Trials with Grooming')
    ax.set_xticklabels(x,rotation=60,ha='right')
    plt.tight_layout()
    
    fig.savefig(currAnDir + animal + '_percGroom.pdf')
    plt.close()

                
        
        
    
    
    