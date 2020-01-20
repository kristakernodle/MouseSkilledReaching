#!/usr/bin/env python3.7

import os

animalDir = '/Volumes/SharedX/Neuro-Leventhal/data/LawrenceLab_Collab/'

# Initialize Variables
allAnimals=[]
allFolders = os.listdir(animalDir)
needAbMov = []
needGroom = []

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
    allTrainDays.sort()
    for day in allTrainDays:

        tday = day.split('_')[-1]
        if len(tday) < 3:
            tday = 'T0' + tday[-1]
        
        if ('.MP4' in day):
            # Skip .MP4 files in 'Training' directory
            continue

        # Define training day directory
        currDayDir=currAnDir+day

        if not os.path.isdir(currDayDir):
            # Skip 'Training/*' items that are not directories
            continue

        # Get all contents of the training day directory
        allFiles=os.listdir(currDayDir)

        # Separate out files and directories by type
        scoreFiles = [file for file in allFiles if file.endswith('Scored.csv')]
        vidFiles = [file for file in allFiles if file.endswith('.MP4')]
        reachFiles = [file for file in allFiles if file.endswith('.csv') and 'Scored' not in file]
        
        if len(reachFiles) < len(vidFiles) or (len(vidFiles) == 0 and len(reachFiles) == 0) or len(scoreFiles) < len(reachFiles):
            # This means not all videos have had the pre-processing done, 
            # continue to the next training day
            tDayData = [tday,999,999,999,999,999,999,999,999]
            summary.append(tDayData)
            continue
        
        reach = []
        abMov = []
        groom = []
        
        skipAbMov = True
        skipGroom = True
        
        for file in scoreFiles:
            
            # Open the file and save into scores
            with open(currDayDir + '/' + file) as f:
                scores = f.read().splitlines()
                scores = scores[1:]
                
            for entry in scores:
                entry = entry.split(',')
                
                if len(entry[1]) == 0:
                    skipDay = True
                    break
                else:
                    skipDay = False
                    
                    reach.append(int(entry[1]))
                    
#                    if len(entry[2]) > 0 and skipAbMov == False:
#                        abMov.append(int(entry[2]))
#                    else:
#                        
#                        if skipAbMov == False:
#                            needAbMov.append(currDayDir)
#                            
#                        skipAbMov = True
#                        abMov = []
#                        
#                    if len(entry[3]) > 0 and skipGroom == False:
#                        groom.append(int(entry[3]))
#                    else:
#                        
#                        if skipGroom == False:
#                            needGroom.append(currDayDir)
#                        
#                        skipGroom = True
#                        groom = []         
            
        if skipDay == True:
            tDayData = [tday,999,999,999,999,999,999,999,999]
            summary.append(tDayData)
            
            continue
        
        trials = len(reach)
        
        score1 = reach.count(1)
        score2 = reach.count(2)
        
        score0 = reach.count(0)
        score6 = reach.count(6)
        score7 = reach.count(7)
        score8 = reach.count(8)
        
        numReaches = trials - score0 - score6 - score7 - score8
        
        firstSuc = score1 / trials * 100
        anySuc = score2 / trials * 100
        
        if len(abMov) != 0:
            totAbMov = sum(abMov)
            percAbMov = totAbMov / trials * 100
        else:
            totAbMov = 999
            percAbMov = 999
        
        if len(groom) != 0:
            totGroom = sum(groom)
            percGroom = totGroom / trials * 100
        else:
            totGroom = 999
            percGroom = 999
        
        tDayData = [tday,trials,numReaches,firstSuc,anySuc,totAbMov,percAbMov,totGroom,percGroom]
        
        summary.append(tDayData)
    
    allTrainingDays = ['T01','T02','T03','T04','T05','T06','T07','T08','T09','T10','T11','T12','T13','T14','T15','T16','T17','T18','T19','T20','T21']
    if len(summary) < 21:
        for item in summary:
            for day in allTrainingDays:
                if day in item[0]:
                    allTrainingDays.remove(day)
                    break
        for day in allTrainingDays:
            summary.append([day,999,999,999,999,999,999,999,999])
    
    summary.sort()
    f = open(currAnDir + 'summaryStatistics_' + animal + '.csv','w+')
    f.write('Training Day,Number of Trials,Number of Reaches,First Success,Any Success,Trials with Abnormal Movement,Percent Trials with Abnormal Movemovent,Trials with Grooming,Percent Trials with Grooming\n')
    for tDay in summary:
        f.write('%s,%f,%f,%f,%f,%f,%f,%f,%f\n' %(tDay[0],tDay[1],tDay[2],tDay[3],tDay[4],tDay[5],tDay[6],tDay[7],tDay[8]))
    f.close
    
needAbMov.sort()
f = open(animalDir + 'needAbMov.txt','w+')
for item in needAbMov:
    f.write('%s\n' %item)
f.close
    
needGroom.sort()
f = open(animalDir + 'needGroom.txt','w+')
for item in needGroom:
    f.write('%s\n' %item)
f.close
    
        
        
