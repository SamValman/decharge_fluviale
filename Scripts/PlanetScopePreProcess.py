# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 15:03:17 2023

@author: lgxsv2
"""
import pandas as pd 
import os
from glob import glob as gl

def PlanetScopePreProcess(folderPath, riverName, AOI, csvOutput):
    print('providing metadata csv')
    
    dirname = os.path.join(folderPath, 'files')
    file_extension = 0
    #lists to be filled
    ID = []
    times = []
    dates = []
    mids = []
    
    for i in gl(os.path.join(dirname, '*.tif')):
        if i[-13:-10]=='udm':
            continue
        print(i)
        fn = os.path.basename(i)[:23]
        
        #Add ID
        ID.append(fn)
        
        #md for metadata
        md = fn + '_metadata.json'
        md = os.path.join(dirname, md)
        datetime = pd.read_json(md)
        
        #divides into date and time
        datetime = datetime.loc['acquired']['properties'].split('T')
        date = datetime[0].replace('-', '_')
        time = datetime[1][:8]
        
        # get file extension
        if date in dates:
            file_extension+=1
        else:
            file_extension = 0 
        
        #needs to be done after file extension
        dates.append(date)
        times.append(time)

        
        # my id 
        mid = date+'_'+str(file_extension)
        mids.append(mid)

        
        # sort out files
        # remove json
        os.remove(md)
        # remove markdown
        md = fn + '_3B_AnalyticMS_metadata_clip.xml'
        md = os.path.join(dirname, md)
        os.remove(md)
        udm = fn + '_3B_udm2_clip.tif'
        udm = os.path.join(dirname, udm)
        os.remove(udm)
        
        # rename tif file we want to keep
        new_fn = os.path.join(dirname, mid+'.tif')
        

        os.rename(i, new_fn)
        
    ## Writing the csv
    csv = pd.DataFrame({'river name': riverName, 'AOI': AOI, 'im_code':mids, 'im_id':ID, 'date':dates, 'time':times})
    
    csv.to_csv(csvOutput)
    return csv        