#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 16:09:01 2019

@author: kkrista
"""

box1 = ['710','713','719','745','749','757','764']
box2 = ['704','717','740','743','7081']


# 7081 not presently listed in labArchives
left = ['704','740','743','745','749','757']
right = ['710','713','717','719','764']

WT = ['704','713','740','743','749','757','764','7081']
KO = ['710','717','719','745']

def pawPref(subj):
    if subj in left:
        pawPref = 'left'
        nonPrefPaw = 'right'
        return pawPref, nonPrefPaw
    elif subj in right:
        pawPref = 'right'
        nonPrefPaw = 'left'
        return pawPref, nonPrefPaw
    else:
        print('No paw preference found')
        
def boxID(subj):
    if subj in box1:
        return '1'
    elif subj in box2:
        return '2'
    else:
        print('No box ID found')
        
def genotype(subj):
    if subj in WT:
        return 'WT'
    elif subj in KO:
        return 'KO'
    else:
        print('Genotype not found')