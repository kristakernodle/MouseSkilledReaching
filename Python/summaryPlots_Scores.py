#!/usr/bin/env python3.7
import os
import numpy as np
import matplotlib.pyplot as plt

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
    
    summary = []
    
    # Define training directory for animal
    currAnDir=animalDir+animal+'/Training/'
        
    if not os.path.isdir(currAnDir):
        # If there is no 'Training' directory, skip this animal
        continue
    
    # Get contents of 'Training' directory
    allTrainDays=os.listdir(currAnDir)

    for day in allTrainDays:

        if ('.MP4' in day):
            # Skip .MP4 files in 'Training' directory
            continue

        # Define training day directory
        currDayDir=currAnDir+day

        if not os.path.isdir(currDayDir):
            # Skip 'Training/*' items that are not directories
            continue

                # Identify where we're at in the code, in case of issues

        # Get all contents of the training day directory
        allFiles=os.listdir(currDayDir)

        # Separate out files and directories by type
        scoreFiles = [file for file in allFiles if file.endswith('Scored.csv')]
        vidFiles = [file for file in allFiles if file.endswith('.MP4')]
        reachDirs = [file for file in allFiles if 'Reaches' in file]
        
        if len(scoreFiles) < len(vidFiles) and len(scoreFiles) < len(reachDirs):
            continue
        
        reach = []
        abMov = []
        groom = []
        
        for file in scoreFiles:
            
            with open(currDayDir + '/' + file) as f:
                scores = f.read().splitlines()
                scores = scores[1:]
                
            for trial in scores:
                trial = trial.split(',')
                    
                if len(trial[1]) > 0:
                    reach.append(int(trial[1]))
                    needBreak = False
                else:
                    needBreak = True
                    break
                        
                if len(trial[2]) > 0:
                    abMov.append(int(trial[2]))
                            
                if len(trial[3]) > 0:
                    groom.append(int(trial[3]))
                
            if needBreak is True:
                break
        
        if needBreak is True:
            print('the day has not been completely scored')
            continue
        
        print('all data for this day is collected')
        
        score1 = reach.count(1)
        score2 = reach.count(2)
        
        firstSuc = score1 / len(reach) * 100
        anySuc = score2 / len(reach) * 100

        totAbMov = sum(abMov)
        percAbMov = totAbMov / len(reach) * 100
        
        tday = day.split('_')[-1]
        
        if len(tday) < 3:
            tday = 'T0' + tday[-1]
        
        tDayData = [tday,firstSuc,anySuc,totAbMov,percAbMov]
        
        summary.append(tDayData)
        
    print('This animal summary stats are collected')
    
    summary.sort()
    
    
    
    xaxis = []
    allFirstSuc = []
    allAnySuc = []
    allTotAbMov = []
    allPercAbMov = []
    
    for day in summary:
        xaxis.append(day[0])
        allFirstSuc.append(day[1])
        allAnySuc.append(day[2])
        allTotAbMov.append(day[3])
        allPercAbMov.append(day[4])
        
    plt.plot(xaxis,allFirstSuc)
    
    
        
        
