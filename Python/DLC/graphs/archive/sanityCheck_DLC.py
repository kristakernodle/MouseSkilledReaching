#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 11:29:59 2019

@author: kkrista
"""

import modDLC

config = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/DLCProcessing/DLC_ConfigFiles/rightPP/rightPP_Center-Krista-2019-02-09/config.yaml'
videos = ['/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/DLCProcessing/makeVid/717_20181130_01_R20.MP4']

frame1 = 800
frame2 = 940

modDLC.create_labeled_video(config,videos,frame1,frame2,videotype='mp4')




