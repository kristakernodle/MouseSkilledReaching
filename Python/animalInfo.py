#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 16:09:01 2019

@author: kkrista
"""

animals = {
        "et704":    ['WT','left', 'box2', '.'],
        "et710":    ['KO','right','box1','.'],
        "et713":    ['WT','right','box1',','],
        "et717":    ['KO','right','box2',','],
        "et719":    ['KO','right','box1','o'],
        "et740":    ['WT','left', 'box2','o'],
        "et743":    ['WT','left', 'box2','^'],
        "et745":    ['KO','left', 'box1','^'],
        "et749":    ['WT','left', 'box1','<'],
        "et757":    ['WT','left', 'box1','>'],
        "et764":    ['WT','right','box1','1'],
        "et7061":   ['KO','left', 'box1','<'],
        "et7062":   ['KO','right','box2','>'],
        "et7063":   ['WT','right','box2','2'],
        "et7064":   ['WT','left', 'box1','3'],
        "et7065":   ['WT','left', 'box2','4'],
        "et7068":   ['WT','left', 'box1','8'],
        "et7076":   ['KO','left', 'box1','2'],
        "et7081":   ['WT','999','box2','s']
        }


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