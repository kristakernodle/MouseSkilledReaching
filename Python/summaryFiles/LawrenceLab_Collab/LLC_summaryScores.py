#!/usr/bin/env python3.7

import os

animalDir = '/Volumes/SharedX/Neuro-Leventhal/data/LawrenceLab_Collab/'

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
    rawSummary = []
    
    # Define subdirectories for animal
    trainDir = animalDir+animal+'/Training/'
    postSurgDir = animalDir+animal+'/postSurgery/'
       
    currAnim_subDirs = [trainDir, postSurgDir]
    
    for currDir in currAnim_subDirs:
        if currDir == trainDir:
            currFold = 'training'
        else:
            currFold = 'postSurgery'
        ## Start with 'Training' directory
        if not os.path.isdir(currDir):
            # If there is no 'Training' directory, skip this animal
            continue
        
        # Get contents of 'Training' directory
        allDays=os.listdir(currDir)
        allDays.sort()
        
        # Loop through each day
        for day in allDays:
            if ('.MP4' in day):
                # Skip .MP4 files in 'Training' directory
                continue
            
            tday = day.split('_')[-1]
            if len(tday) < 3 and 'T' in tday:
                tday = 'T0' + tday[-1]
            elif len(tday) < 4 and 'PS' in tday:
                tday = 'PS0' + tday[-1]
    
            # Define training day directory
            currDayDir=currDir+day
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
                tDayData = [tday,999,999,999,999]
                summary.append(tDayData)
                continue
            
            reach = []
            
            for file in scoreFiles:
                
                # Open the file and save into scores
                with open(currDayDir + '/' + file) as f:
                    scores = f.read().splitlines()
                    scores = scores[1:]
                    
                for entry in scores:
                    entry = entry.split(',')
                    
                    if len(entry[1]) == 0:
                        # If there is no score for the first reach video, skip it
                        skipDay = True
                        break
                    else:
                        skipDay = False
                        reach.append(int(entry[1]))
                                            
            if skipDay == True:
                # If there is no score for the first reach video, use placeholder data
                tDayData = [tday,999,999,999,999]
                summary.append(tDayData)
                
                continue
            
            trials = len(reach)
            
            score0 = reach.count(0)
            score1 = reach.count(1)
            score2 = reach.count(2)
            score3 = reach.count(3)
            score4 = reach.count(4)
            score5 = reach.count(5)
            score6 = reach.count(6)
            score7 = reach.count(7)
            score8 = reach.count(8)
            score9 = reach.count(9)
            
            numReaches = trials - score0 - score6 - score7 - score8
            
            firstSuc = score1 / trials * 100
            anySuc = (score1 + score2) / trials * 100
            
            tDayData = [tday,trials,numReaches,firstSuc,anySuc]
            rawData = [tday,trials,score0,score1,score2,score3,score4,score5,score6,score7,score8,score9]
            
            summary.append(tDayData)
            rawSummary.append(rawData)
            
    f = open(animalDir+animal + '/summaryStatistics_'+ animal + '.csv','w+')
    f.write('Behavior Day,Number of Trials,Number of Reaches,First Success,Any Success\n')
    for tDay in summary:
        f.write('%s,%f,%f,%f,%f\n' %(tDay[0],tDay[1],tDay[2],tDay[3],tDay[4]))
    f.close()
    
    f = open(animalDir+animal + '/rawSummaryStatistics_'+ animal + '.csv','w+')
    f.write('Behavior Day,Number of Trials,score0,score1,score2,score3,score4,score5,score6,score7,score8,score9\n')
    for tDay in rawSummary:
        f.write('%s,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n' %(tDay[0],tDay[1],tDay[2],tDay[3],tDay[4],tDay[5],tDay[6],tDay[7],tDay[8],tDay[9],tDay[10],tDay[11]))
    f.close()

    
        
        
