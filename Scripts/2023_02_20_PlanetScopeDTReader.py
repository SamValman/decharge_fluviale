# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 14:30:12 2023

@author: lgxsv2
"""
import os
os.chdir(r'E:\Mitacs\decharge_fluviale\Scripts')
from PlanetScopePreProcess import PlanetScopePreProcess


#%%
folderPath = r"E:\Mitacs\decharge_fluviale\MiTACS_zips\Val_StM_Oct22_psscene_analytic_sr_udm2"


a = PlanetScopePreProcess(folderPath, riverName='Sainte-Margurite', AOI='SM_1', csvOutput='E:\\Mitacs\\decharge_fluviale\\oct22.csv')

#%%
folderPath=r"E:\Mitacs\decharge_fluviale\MiTACS_zips\Val_M_sept_psscene_analytic_sr_udm2"

a = PlanetScopePreProcess(folderPath, riverName='Sainte-Margurite', AOI='SM_1', csvOutput='E:\\Mitacs\\decharge_fluviale\\sept22.csv')

    