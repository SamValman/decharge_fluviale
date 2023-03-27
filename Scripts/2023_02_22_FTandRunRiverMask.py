# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 14:24:50 2023

@author: lgxsv2
"""

import os
import glob
import pandas as pd
import gc


os.chdir(r'E:\Mitacs\decharge_fluviale\Scripts\IsolatedRiverMaskFunctions')
from RiverTwinWaterMask import RiverTwinWaterMask
from FineTune2 import fineTune

gc.collect()
#%% Fine Tune model
trainingDataTifs = r'E:\Mitacs\decharge_fluviale\Scripts\IsolatedRiverMaskFunctions\train\*.tif'
trainingDataTifs = r'E:\Mitacs\decharge_fluviale\Scripts\IsolatedRiverMaskFunctions\train\*.tif'
FolderContents = [os.path.basename(x) for x in glob.glob(trainingDataTifs)] # gets all files needed
# do soemthing with os.path.basepath here ****************** above lambda or something 
trainingDataLocation=r'E:\Mitacs\decharge_fluviale\Scripts\IsolatedRiverMaskFunctions'
outfile=r'E:\Mitacs\decharge_fluviale\Scripts\IsolatedRiverMaskFunctions\StM_20230222'
tile_dir = r'C:\Users\lgxsv2\TrainingData'





#%%
fineTune(newTrainingData=True, trainingData=FolderContents,
                             balanceTrainingData=1, trainingFolder='',
                             outfile=outfile,
                             tile_dir=tile_dir, 
                             trainingDataLocation=trainingDataLocation,
                              epochs=10, bs=32, lr_type='plain',
                              tileSize=20)


#%% ANN Section
imPath = r'E:\Mitacs\decharge_fluviale\Rivers\Ste-Marguerite\raw\*.tif'
fn_model = r"E:\Mitacs\decharge_fluviale\Scripts\IsolatedRiverMaskFunctions\StM_20230222\model"
output = r"E:\Mitacs\decharge_fluviale\Rivers\Ste-Marguerite\watermask"

for i in glob.glob(imPath)[:]:
    im_name = i.split('\\')[-1]
    print(im_name)
    
    p1,p2,p3, time = RiverTwinWaterMask(image_fp=i,
                                            model=fn_model, tileSize=20,
                                            output=output)
#%%