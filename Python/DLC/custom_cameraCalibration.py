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
    
    # If the paths do not exist, create them
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    if not os.path.exists(path_corners):
        os.makedirs(path_corners)
    
    images = glob.glob(os.path.join(img_path,'*.jpg'))
    cam_names = cfg_3d['camera_names']

    # Initialize the dictionary 
    img_shape = {}
    objpoints = {} # 3d point in real world space
    imgpoints = {} # 2d points in image plane.
    dist_pickle = {}
        
    # Sort the images.
    images.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    if len(images)==0:
        raise Exception("No calibration images found. Make sure the calibration images are saved as .jpg and with prefix as the camera name as specified in the config.yaml file.")
    
    for fname in images:
        filename = Path(fname).stem
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (cbcol,cbrow),None,) #  (8,6) pattern (dimensions = common points of black squares)
        # If found, add object points, image points (after refining them)
        if ret == True:
            img_shape = gray.shape[::-1]
            objpoints.append(objp)
            imgpoints.append(corners)
            corners = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            # Draw the corners and store the images
            img = cv2.drawChessboardCorners(img, (cbcol,cbrow), corners,ret)
            cv2.imwrite(os.path.join(str(path_corners),filename+'_corner.jpg'),img)
        else:
            print("Corners not found for the image %s" %Path(fname).name)

    # Perform calibration for the camera and store the matrix as a pickle file
    if calibrate == True:

        # Calibrating the camera
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img_shape,None,None)
        
        # Compute mean re-projection error for camera
        mean_error = 0
        for i in range(len(objpoints)):
            imgpoints_proj, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
            error = cv2.norm(imgpoints[i],imgpoints_proj, cv2.NORM_L2)/len(imgpoints_proj)
            mean_error += error
        print("Mean re-projection error for your camera: %.3f pixels " %(mean_error/len(objpoints)))

        for cam in cam_names:
            # Save the camera calibration result for later use (we won't use rvecs / tvecs)
            dist_pickle[cam] = {'mtx':mtx , 'dist':dist, 'objpoints':objpoints,'imgpoints':imgpoints}
            pickle.dump( dist_pickle, open( os.path.join(path_camera_matrix,cam+'_intrinsic_params.pickle'), "wb" ) )
            print('Saving intrinsic camera calibration matrices for %s as a pickle file in %s'%(cam, os.path.join(path_camera_matrix)))

def calibrateCamera(config,cbrow = 4,cbcol = 3,calibrate=False,alpha=0.4):
    """This function extracts the corners points from the calibration images, calibrates the camera and stores the calibration files in the project folder (defined in the config file).
    
    Make sure you have around 20-60 pairs of calibration images. The function should be used iteratively to select the right set of calibration images. 
    
    A pair of calibration image is considered "correct", if the corners are detected correctly in both the images. It may happen that during the first run of this function, 
    the extracted corners are incorrect or the order of detected corners does not align for the corresponding views (i.e. camera-1 and camera-2 images).
    
    In such a case, remove those pairs of images and re-run this function. Once the right number of calibration images are selected, 
    use the parameter ``calibrate=True`` to calibrate the cameras.

    Parameters
    ----------
    config : string
        Full path of the config.yaml file as a string.

    cbrow : int
        Integer specifying the number of rows in the calibration image.
    
    cbcol : int
        Integer specifying the number of columns in the calibration image.

    calibrate : bool
        If this is set to True, the cameras are calibrated with the current set of calibration images. The default is ``False``
        Set it to True, only after checking the results of the corner detection method and removing dysfunctional images!
        
    alpha: float
        Floating point number between 0 and 1 specifying the free scaling parameter. When alpha = 0, the rectified images with only valid pixels are stored 
        i.e. the rectified images are zoomed in. When alpha = 1, all the pixels from the original images are retained. 
        For more details: https://docs.opencv.org/2.4/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html
        
    Example
    --------
    Linux/MacOs/Windows
    >>> deeplabcut.calibrate_camera(config)

    Once the right set of calibration images are selected, 
    >>> deeplabcut.calibrate_camera(config,calibrate=True)

    """

    # Termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # Prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((cbrow * cbcol, 3), np.float32)
    objp[:, :2] = np.mgrid[0:cbcol, 0:cbrow].T.reshape(-1, 2)
    
    # Read the config file
    cfg_3d = auxiliaryfunctions.read_config(config)
    img_path,path_corners,path_camera_matrix,path_undistort=caf.Foldernames3Dproject(cfg_3d)
    
    # Make sure that the folders are present (if not, make them)
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    if not os.path.exists(path_corners):
        os.makedirs(path_corners)
    
    # Get images and camera names
    images = glob.glob(os.path.join(img_path,'*.jpg'))
    cam_names = cfg_3d['camera_names']
    
    ## It's not clear to me why I want to do this or what this number represents... I need to read further into it
    # # update the variable snapshot* in config file according to the name of the cameras
    # try:
    #     for i in range(len(cam_names)):
    #         cfg_3d[str('config_file_'+cam_names[i])] = cfg_3d.pop(str('config_file_camera-'+str(i+1)))
    #     for i in range(len(cam_names)):
    #         cfg_3d[str('shuffle_'+cam_names[i])] = cfg_3d.pop(str('shuffle_camera-'+str(i+1)))
    # except:
    #     pass
    
    project_path = cfg_3d['project_path']
    projconfigfile=os.path.join(str(project_path),'config.yaml')
    auxiliaryfunctions.write_config_3d(projconfigfile,cfg_3d)

    # Initialize the dictionary 
    img_shape = {}
    objpoints = {} # 3d point in real world space
    imgpoints = {} # 2d points in image plane.
    dist_pickle = {} ## I think this is the intrinsic parameter file that needs to be read in
    stereo_params= {}
    for cam in cam_names:
        objpoints.setdefault(cam, [])
        imgpoints.setdefault(cam, [])
        dist_pickle.setdefault(cam, [])

    # Sort the images.
    images.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    if len(images)==0:
        raise Exception("No calibration images found. Make sure the calibration images are saved as .jpg and with prefix as the camera name as specified in the config.yaml file.")
    direct_images = [img for img in images if 'direct' in img]
    mirror_images = [img for img in images if 'mirror' in img]

    # Start with mirror to figure out which BGR to use for direct
    for fname in mirror_images:
        
        filename=Path(fname).stem
        img = cv2.imread(fname)

        # Create a dictionary with all of the different image color conversions for testing
        img_colorConv = {
                            "BGR":img,
                            "HSV":cv2.cvtColor(img,40),
                            "Gray":cv2.cvtColor(img,6)
                        }

        ret = False
        for colorConv in img_colorConv:
            currImg = img_colorConv[colorConv]
            size = currImg.shape
            
            if len(size) == 2:
                
                ret, corners = cv2.findChessboardCorners(currImg, (cbcol,cbrow),None,)
                if ret == True: break

                currImg_bw = cv2.threshold(currImg,128,255,cv2.THRESH_BINARY)[1]
                ret, corners = cv2.findChessboardCorners(currImg_bw, (cbcol,cbrow),None,)
                if ret == True: break
                else: continue
            
            chanIdx = 0
            while (ret == False) and (chanIdx < size[2]):
                ret, corners = cv2.findChessboardCorners(currImg[:,:,chanIdx], (cbcol,cbrow),None,)
                if ret == True: break
                channel_bw = cv2.threshold(currImg[:,:,chanIdx],128,255,cv2.THRESH_BINARY)[1]
                ret, corners = cv2.findChessboardCorners(channel_bw, (cbcol,cbrow),None,)
                chanIdx += 1
            
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
        
        # Read in the intrinsic parameters for each camera
        for cam in cam_names:
            dist_pickle[cam] = pickle.load(os.path.join(path_camera_matrix,cam+'_intrinsic_params.pickle'))

    #     # Compute stereo calibration for each pair of cameras
    #     camera_pair = [[cam_names[0], cam_names[1]]]
    #     for pair in camera_pair:
    #         print("Computing stereo calibration for " %pair)
    #         retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F = cv2.stereoCalibrate(objpoints[pair[0]],imgpoints[pair[0]],imgpoints[pair[1]],dist_pickle[pair[0]]['mtx'],dist_pickle[pair[0]]['dist'], dist_pickle[pair[1]]['mtx'], dist_pickle[pair[1]]['dist'],(h,  w),flags = cv2.CALIB_FIX_INTRINSIC)

    #         # Stereo Rectification
    #         rectify_scale = alpha # Free scaling parameter check this https://docs.opencv.org/2.4/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html#fisheye-stereorectify
    #         R1, R2, P1, P2, Q, roi1, roi2 = cv2.stereoRectify(cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, (h, w), R, T, alpha = rectify_scale)
            
    #         stereo_params[pair[0]+'-'+pair[1]] = {"cameraMatrix1": cameraMatrix1,"cameraMatrix2": cameraMatrix2,"distCoeffs1": distCoeffs1,"distCoeffs2": distCoeffs2,"R":R,"T":T,"E":E,"F":F,
    #                      "R1":R1,
    #                      "R2":R2,
    #                      "P1":P1,
    #                      "P2":P2,
    #                      "roi1":roi1,
    #                      "roi2":roi2,
    #                      "Q":Q,
    #                      "image_shape":[img_shape[pair[0]],img_shape[pair[1]]]}
            
    #     print('Saving the stereo parameters for every pair of cameras as a pickle file in %s'%str(os.path.join(path_camera_matrix)))
        
    #     auxiliaryfunctions.write_pickle(os.path.join(path_camera_matrix,'stereo_params.pickle'),stereo_params)
    #     print("Camera calibration done! Use the function ``check_undistortion`` to check the check the calibration")
    # else:
    #     print("Corners extracted! You may check for the extracted corners in the directory %s and remove the pair of images where the corners are incorrectly detected. If all the corners are detected correctly with right order, then re-run the same function and use the flag ``calibrate=True``, to calbrate the camera."%str(path_corners))
