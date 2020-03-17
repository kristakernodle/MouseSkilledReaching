import os
import glob
import cv2
from pathlib import Path

os.chdir('/Users/Krista/Documents/GitHub/mouseSkilledReaching/Python/DLC')
import custom_auxiliaryFunctions as caf

cropParams_direct_csv = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/DLCNetworks/cropParams/CC1_directCrops.csv'
cropParams_right_csv = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/DLCNetworks/cropParams/CC1_leftCrops.csv'
img_path = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/DLCNetworks/rightPP/rightPP_Right-Krista-2019-11-18-3d/calibImages/'

# Read in all crop parameters
cropParams_direct = caf.readCSV(cropParams_direct_csv)
cropParams_right = caf.readCSV(cropParams_right_csv)

# Read in all the images
images = glob.glob(os.path.join(img_path,'*.jpg'))

for image in images:
    filename = Path(image).stem
    date = filename.split('_')[0]
    filename_parts = filename.split('-')
    img = cv2.imread(image)

    # Direct Crop
    for day in cropParams_direct:
        if date == day.split(',')[0]:
            d_x1 = int(day.split(',')[1])
            d_x2 = int(day.split(',')[2])
            d_y1 = int(day.split(',')[3])
            d_y2 = int(day.split(',')[4])
            break
    if d_y2 == len(img[:,0,0]):
        d_y2 = d_y2-1
    img_directView = img[d_y1:d_y2,d_x1:d_x2,:]
    
    # Mirror Crop
    for day in cropParams_right:
        if date == day.split(',')[0]:
            m_x1 = int(day.split(',')[1])
            m_x2 = int(day.split(',')[2])
            m_y1 = int(day.split(',')[3])
            m_y2 = int(day.split(',')[4])
            break
    if m_x2 == len(img[0,:,0]):
        m_x2 = m_x2 - 1
    if m_y2 == len(img[:,0,0]):
        m_y2 = m_y2-1
    img_rightView = img[m_y1:m_y2,m_x1:m_x2,:]
    
    cv2.imwrite(img_path + filename_parts[0] + '_direct-' + filename_parts[-1] + '.jpg',img_directView)
    cv2.imwrite(img_path + filename_parts[0] + '_mirror-' + filename_parts[-1] + '.jpg',img_rightView)
