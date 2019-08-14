#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 16:09:01 2019

@author: kkrista
"""

animals = {
        "et704":['WT', 'left', 'box2', '.'],
        "et710":['KO','right','box1',''],
        "et713":['WT','','',''],
        "et717":[],
        "et719":[],
        "et740":[],
        "et743":[],
        "et745":[],
        "et749":[],
        "et7061":[],
        "et7062":[],
        "et7063":[],
        "et7064":[],
        "et7065":[],
        "et7068":[],
        "et7076":[],
        "et7081":[]
        }

box1 = ['713','719','745','749','757','764']
box2 = ['717','740','743','7081']


# 7081 not presently listed in labArchives
left = ['740','743','745','749','757']
right = ['713','717','719','764']

WT = ['713','740','743','749','757','764','7081']
KO = ['717','719','745']



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