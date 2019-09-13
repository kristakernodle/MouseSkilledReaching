#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scoring Algorithm

Originally authored by Annie Taylor (annietay@umich.edu) for Alex Bova's rat
reaching data. Modified by Krista Kernodle (kkrista@umich.edu) for mouse
reaching data.

Created on Mon Sep  9 10:47:35 2019

@author: Annie Taylor
@author: Krista Kernodle
"""

import numpy as np
import time
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
import scoringFuncs
 
time1 = time.time()   
    
directoryString = 'Rats'
labelArray = []
featureArray = 0
featureArray = list()
keyErrors = 0

scoresheets, pathnames_direct = scoringFuncs.importDirect(directoryString)

fileNum = len(pathnames_direct)
fileNum = int(fileNum)
print(fileNum)

for i in range(fileNum):
    #try:
        pathname = pathnames_direct[i]
        features = scoringFuncs.readDLC(pathname)
        rat,date1,date2,trialNum = scoringFuncs.getInfo(pathname)
        for i in scoresheets:
            print(i)
            print(rat)
            if (i == rat):
                print('yes')
            else:
                print('no')
            break
        #labels = importLabels(scoresheets,rat)
        #label = labels.at[trialNum,date2]
        #labelArray = np.append(labelArray,label)
        #featureArray.append(features)
    #except KeyError:
        #keyErrors = keyErrors + 1
        #print(pathname)
        #print('Key Error #%d' % keyErrors)
        #print(date1)
        #print(date2)
        #print(trialNum)
        #break
    
#normalizedFeatures = normalize(featureArray)

time2 = time.time()
print('Total runtime is: %f' % (time2 - time1))

# Get euclidean features
#####
# ASK ANNIE, WHAT'S UP WITH FEATUREARRAY? SHOULD IT BE FEATUREARRAY.APPEND(FEATURES)? THIS IS NOT WELL DEFINED. COULD USE HELP.
distFeatures = scoringFuncs.distFromPellet(featureArray)
distFeatures = np.asarray(distFeatures)

ln = len(distFeatures)

redDimFeatures = np.empty([ln,30]) # 30 dimensions of the feature space
x = featureArray[0].transpose()
x = np.asarray(x, dtype=float)
pca = PCA(n_components=30) # 30 dimensions of the feature space
pca.fit(x)
x = pca.transform(x)
ycount = 0
for y in featureArray:
    y = y.transpose()
    y = np.asarray(y, dtype=float)
    redDimFeatures[ycount] = pca.transform(y)[0] 
    ycount= ycount+1
    
time2 = time.time()
print('PCA runtime is: %f' % (time2 - time1))

split_sz = scoringFuncs.getSplitSize(redDimFeatures,20)

ar1, ar2, ar3, ar4, ar5, ar6, ar7, ar8, ar9, ar10 = np.split(redDimFeatures,split_sz)
print(np.shape(ar1))
trainData = ar1
temp1 = np.concatenate(ar2, ar3, ar4)
temp2 =np.concatenate(ar5, ar6, ar7)
temp3 = np.concatenate(ar8, ar9, ar10)
testData = np.concatenate(t1,t2,t3)

l1, l2, l3, l4, l5, l6, l7, l8, l9, l10 = np.split(labelArray,split_sz)
trainLabel=l1
temp1 = np.concatenate(l2, l3, l4)
temp2 =np.concatenate(l5, l6, l7,)
temp3 = np.concatenate(l8, l9, l10)
testLabel = np.concatenate(t1,t2,t3)


neigh = KNeighborsClassifier(n_neighbors = 3)
time1 = time.time()
neigh.fit(trainData, trainLabel) 
time2 = time.time()
trainingOutput = neigh.predict(trainData)
time3 = time.time()
testOutput = neigh.predict(testData)
time4 = time.time()

tstdata_sz = len(testData)
print('Time to train dataset is: %f' % (time2 - time1))
print('Time to test training set is: %f'% (time3 - time2))
print('Time to predict test set is: %f'% (time4 - time3))
print('Average time to predict trial outcome: %f' % ((time4 - time3)/tstdata_sz))

tr_sz = len(trainingOutput)
tr_score = 0

for i in range(sz):
    if trainingOutput[i] == trainLabel[i]:
        tr_score = tr_score + 1

print(tr_score)
print(tr_sz)
print(tr_score/tr_sz)

tst_sz = len(testOutput)
score = 0

for i in range(sz):
    if testOutput[i] == testLabel[i]:
        tst_score = tst_score + 1

print(tst_score)
print(tst_sz)
print(tst_score/tst_sz)