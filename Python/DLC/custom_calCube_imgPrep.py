import os
import glob
import cv2

os.chdir('/Users/Krista/Documents/GitHub/mouseSkilledReaching/Python/DLC')
import custom_auxiliaryFunctions as caf

cropParams_direct_csv = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/DLCNetworks/cropParams/CC1_directCrops.csv'
cropParams_right_csv = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/DLCNetworks/cropParams/CC1_rightCrops.csv'

img_dir = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/DLCNetworks/rightPP/rightPP_Right-Krista-2019-11-18-3d/calibImages/'

images = glob.glob(os.path.join(img_path,'*.jpg'))

for image in images:
    filename = image.split('/')[-1]
    
    # Read in crop parameters
    
    
    img = cv2.imread(image)
