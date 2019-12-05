

import os

def Foldernames3Dproject(cfg_3d,intrinsic=False):
    ''' Definitions of subfolders in 3D projects '''
    
    if intrinsic == True: 
        img_path = os.path.join(cfg_3d['project_path'],'intrinsic_calibImages')
        path_corners = os.path.join(cfg_3d['project_path'],'intrinsic_corners')
    else: 
        img_path = os.path.join(cfg_3d['prtypeoject_path'],'calibImages')
        path_corners = os.path.join(cfg_3d['project_path'],'corners')

    path_camera_matrix = os.path.join(cfg_3d['project_path'],'camera_matrix')
    path_undistort = os.path.join(cfg_3d['project_path'],'undistortion')
    
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    if not os.path.exists(path_corners):
        os.makedirs(path_corners)
    
    return img_path,path_corners,path_camera_matrix,path_undistort