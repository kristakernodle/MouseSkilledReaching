

import os

def Foldernames3Dproject(cfg_3d):
    ''' Definitions of subfolders in 3D projects '''
    
    img_path = os.path.join(cfg_3d['project_path'],'intrinsicParam_images')
    path_corners = os.path.join(cfg_3d['project_path'],'corners')
    path_camera_matrix = os.path.join(cfg_3d['project_path'],'camera_matrix')
    path_undistort = os.path.join(cfg_3d['project_path'],'undistortion')
    
    return img_path,path_corners,path_camera_matrix,path_undistort