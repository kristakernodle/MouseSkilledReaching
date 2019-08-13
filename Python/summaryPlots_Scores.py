#!/usr/bin/env python3.7

import os

animalDir = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/'

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
        reachDirs = [file for file in allFiles if 'Reaches' in file]
        
        if len(reachDirs) < len(vidFiles) or (len(vidFiles) == 0 and len(reachDirs) == 0) or len(scoreFiles) < len(reachDirs):
            # This means not all videos have had the pre-processing done, 
            # continue to the next training day
            tDayData = [tday,999,999,999,999,999]
            summary.append(tDayData)
            continue
        
        reach = []
        abMov = []
        groom = []
        
        skipAbMov = False
        skipGroom = False
        
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
                    
                    if len(entry[2]) > 0 and skipAbMov == False:
                        abMov.append(int(entry[2]))
                    else:
                        
                        if skipAbMov == False:
                            needAbMov.append(currDayDir)
                            
                        skipAbMov = True
                        abMov = []
                        
                    if len(entry[3]) > 0 and skipGroom == False:
                        groom.append(int(entry[3]))
                    else:
                        
                        if skipGroom == False:
                            needGroom.append(currDayDir)
                        
                        skipGroom = True
                        groom = []         
            
        if skipDay == True:
            tDayData = [tday,999,999,999,999,999]
            summary.append(tDayData)
            
            continue
               
        score1 = reach.count(1)
        score2 = reach.count(2)
        
        firstSuc = score1 / len(reach) * 100
        anySuc = score2 / len(reach) * 100
        
        if len(abMov) != 0:
            totAbMov = sum(abMov)
            percAbMov = totAbMov / len(reach) * 100
        else:
            totAbMov = 999
            percAbMov = 999
        
        if len(groom) != 0:
            totGroom = sum(groom)
        else:
            totGroom = 999
        
        tDayData = [tday,firstSuc,anySuc,totAbMov,percAbMov,totGroom]
        
        summary.append(tDayData)
    
    summary.sort()
    f = open(currAnDir + 'summaryStatistics_' + animal + '.csv','w+')
    f.write('Training Day,First Success,Any Success, Trials with Abnormal Movement,Percent Trials with Abnormal Movemovent, Trials with Grooming\n')
    for tDay in summary:
        f.write('%s,%f,%f,%f,%f,%f\n' %(tDay[0],tDay[1],tDay[2],tDay[3],tDay[4],tDay[5]))
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
    
        
        
