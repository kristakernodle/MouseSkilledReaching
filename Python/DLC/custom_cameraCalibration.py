#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 10:30:35 2019

@author: kkrista
"""

import numpy as np
from pathlib import Path
import cv2
import os
import pickle
import glob
from deeplabcut.utils import auxiliaryfunctions
from deeplabcut.utils import auxiliaryfunctions_3d

os.chdir('/Users/Krista/Documents/GitHub/mouseSkilledReaching/Python/DLC/')
import custom_auxiliaryFunctions as caf


def intrinsicParameters(config,cbrow = 9,cbcol = 6,calibrate=False,alpha=0.4):
    '''
    Note: The checkerboard I used for getting the intrinsic parameters of the cameras is 9 by 6
    '''

    # Termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    
    # Prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    # This is an enumeration of the points on the checkerboard
    objp = np.zeros((cbrow * cbcol, 3), np.float32)
    objp[:, :2] = np.mgrid[0:cbcol, 0:cbrow].T.reshape(-1, 2)
    
    # Read the config file
    cfg_3d = auxiliaryfunctions.read_config(config)
    img_path,path_corners,path_camera_matrix,path_undistort=caf.Foldernames3Dproject(cfg_3d,True)
    
    images = glob.glob(os.path.join(img_path,'*.jpg'))
    cam_names = cfg_3d['camera_names']
    
    # update the variable snapshot* in config file according to the name of the cameras
    try:
        for i in range(len(cam_names)):
            cfg_3d[str('config_file_'+cam_names[i])] = cfg_3d.pop(str('config_file_camera-'+str(i+1)))
        for i in range(len(cam_names)):
            cfg_3d[str('shuffle_'+cam_names[i])] = cfg_3d.pop(str('shuffle_camera-'+str(i+1)))
    except:
        pass
    
    project_path = cfg_3d['project_path']
    projconfigfile=os.path.join(str(project_path),'config.yaml')
    auxiliaryfunctions.write_config_3d(projconfigfile,cfg_3d)

    # Initialize the dictionary 
    img_shape = {}
    objpoints = {} # 3d point in real world space
    imgpoints = {} # 2d points in image plane.
    dist_pickle = {}
    for cam in cam_names:
        objpoints.setdefault(cam, [])
        imgpoints.setdefault(cam, [])
        dist_pickle.setdefault(cam, [])
    
    # Sort the images.
    images.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    if len(images)==0:
        raise Exception("No calibration images found. Make sure the calibration images are saved as .jpg and with prefix as the camera name as specified in the config.yaml file.")
    
    for fname in images:
        for cam in cam_names:
            if cam in fname:
                filename = Path(fname).stem
                img = cv2.imread(fname)
                gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

                # Find the chess board corners
                ret, corners = cv2.findChessboardCorners(gray, (cbcol,cbrow),None,) #  (8,6) pattern (dimensions = common points of black squares)
                # If found, add object points, image points (after refining them)
                if ret == True:
                    img_shape[cam] = gray.shape[::-1]
                    objpoints[cam].append(objp)
                    corners = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
                    imgpoints[cam].append(corners)
                    # Draw the corners and store the images
                    img = cv2.drawChessboardCorners(img, (cbcol,cbrow), corners,ret)
                    cv2.imwrite(os.path.join(str(path_corners),filename+'_corner.jpg'),img)
                else:
                    print("Corners not found for the image %s" %Path(fname).name)
    try:
        h,  w = img.shape[:2]
    except:
        raise Exception("It seems that the name of calibration images does not match with the camera names in the config file. Please make sure that the calibration images are named with camera names as specified in the config.yaml file.")

    # Perform calibration for each cameras and store the matrices as a pickle file
    if calibrate == True:
        # Calibrating each camera
        for cam in cam_names:
            ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints[cam], imgpoints[cam], img_shape[cam],None,None)

            # Save the camera calibration result for later use (we won't use rvecs / tvecs)
            dist_pickle[cam] = {'mtx':mtx , 'dist':dist, 'objpoints':objpoints[cam] ,'imgpoints':imgpoints[cam] }
            pickle.dump( dist_pickle, open( os.path.join(path_camera_matrix,cam+'_intrinsic_params.pickle'), "wb" ) )
            print('Saving intrinsic camera calibration matrices for %s as a pickle file in %s'%(cam, os.path.join(path_camera_matrix)))
            
            # Compute mean re-projection errors for individual cameras
            mean_error = 0
            for i in range(len(objpoints[cam])):
                imgpoints_proj, _ = cv2.projectPoints(objpoints[cam][i], rvecs[i], tvecs[i], mtx, dist)
                error = cv2.norm(imgpoints[cam][i],imgpoints_proj, cv2.NORM_L2)/len(imgpoints_proj)
                mean_error += error
            print("Mean re-projection error for %s images: %.3f pixels " %(cam, mean_error/len(objpoints[cam])))