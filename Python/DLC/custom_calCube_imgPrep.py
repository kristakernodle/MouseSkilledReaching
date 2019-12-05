import os
import glob
import cv2

os.chdir('/Users/Krista/Documents/GitHub/mouseSkilledReaching/Python/DLC')
import custom_auxiliaryFunctions as caf

cropParams_direct_csv = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/DLCNetworks/cropParams/CC1_directCrops.csv'
cropParams_right_csv = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/DLCNetworks/cropParams/CC1_rightCrops.csv'
img_path = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/DLCNetworks/rightPP/rightPP_Right-Krista-2019-11-18-3d/calibImages/'

# Read in all crop parameters
cropParams_direct = caf.readCSV(cropParams_direct_csv)
cropParams_right = caf.readCSV(cropParams_right_csv)

# Read in all the images
images = glob.glob(os.path.join(img_path,'*.jpg'))

for image in images:
    filename = image.split('/')[-1]
    date = filename.split('_')[0]

    img = cv2.imread(image)

    # Direct Crop
    for day in cropParams_direct:
        if date == day.split(',')[0]:
            x1 = day.split(',')[1]
            x2 = day.split(',')[2]
            y1 = day.split(',')[3]
            y2 = day.split(',')[4]
            break
    img_directView = img(x1:x2,y1:y2,:)
    
    # Mirror Crop
    for day in cropParams_right:
        if date == day.split(',')[0]:
            x1 = day.split(',')[1]
            x2 = day.split(',')[2]
            y1 = day.split(',')[3]
            y2 = day.split(',')[4]
            break
    img_rightView = img(x1:x2,y1:y2,:)

    

    
    
    
