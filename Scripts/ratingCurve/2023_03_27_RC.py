# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 12:28:10 2023

@author: lgxsv2
"""

# option one
# https://github.com/cojacoo/hydro_tutorial
The important information:
# you have a function like this (and some h and q data)
def RCf_fixc(H,a,b, c=11):
    # rating curve function
    #Calculate flux [m3/s] from a given water level [cm]
    #we convert H and c to meters
    #c is given
    return a*((H-c)/100)**b
# you get values for a and b like this 
Height = RC_dummy.Level
Discharge = RC_dummy.Q_m3s
opt, covar = so.curve_fit(RCf_fixc, Height, Discharge, maxfev = 100000)
# you put them back together for future predictions like this
def RCf_colpach(H):
    #Calculate flux [m3/s] from a given water level [cm] at gauge Colpach
    c=11.
    a=opt[0]
    b=opt[1]
    return a*((H-c)/100.)**b
# option 2 


#%% option one

import pandas as pd
import numpy as np
import scipy.stats as st
import scipy.optimize as so
import matplotlib.pyplot as plt

fn = r"E:\Mitacs\decharge_fluviale\Scripts\ratingCurve\demoData\rating_curve_HQ.csv"

demo_guage = pd.read_csv(fn)


print(demo_guage.Gauge.unique())

#%%
RC_dummy = demo_guage.loc[demo_guage.Gauge=='Colpach']
plt.plot(RC_dummy.Level,RC_dummy.Q_m3s,'o')
plt.xlabel('Water Level [cm]')
plt.ylabel('Measured Discharge [m3/s]')
plt.title('Rating Curve Colpach - measured')
#%%
# fit the equation: Q = a * (water height - Coffset)^b

def RCf_fixc(H,a,b, c=11):
    # rating curve function
    #Calculate flux [m3/s] from a given water level [cm]
    #we convert H and c to meters
    #c is given
    return a*((H-c)/100)**b



#Fit the curve using scipy non linear least squares 
Height = RC_dummy.Level
Discharge = RC_dummy.Q_m3s
opt, covar = so.curve_fit(RCf_fixc, Height, Discharge, maxfev = 100000)


#%%
plt.plot(RC_dummy.Level,RC_dummy.Q_m3s,'.',label='measured')
dummy_range = np.arange(100)
plt.plot(dummy_range,RCf_fixc(dummy_range,opt[0],opt[1]),'-',label='fitted')
plt.text(20,5,''.join(['a = ',str(np.round(opt[0],2)),'\nb = ',str(np.round(opt[1],2))]))
plt.legend(loc=2)
plt.xlabel('Water Level [cm]')
plt.ylabel('Measured Discharge [m3/s]')
plt.title('Rating Curve Colpach')


#%% For all guages
#Let's do that for all gauges:

def RCf_fixw(H,a,b):
    c=10.2
    return a*((H-c)/100.)**b

def RCf_fixu(H,a,b):
    c=5.
    return a*((H-c)/100.)**b

def RCf_fixh(H,a,b):
    c=8.
    return a*((H-c)/100.)**b



#Fit the curves
RC_dummy=demo_guage.loc[demo_guage.Gauge=='Weierbach']
opt_w, covar_w = so.curve_fit(RCf_fixw, RC_dummy.Level,RC_dummy.Q_m3s,maxfev = 100000)

plt.subplot(131)
plt.plot(RC_dummy.Level,RC_dummy.Q_m3s,'.',label='measured')
dummy_range = np.arange(35)
plt.plot(dummy_range,RCf_fixw(dummy_range,opt_w[0],opt_w[1]),'-',label='fitted')
plt.text(15,0.03,''.join(['a = ',str(np.round(opt_w[0],2)),'\nb = ',str(np.round(opt_w[1],2))]))
#legend(loc=2)
plt.xlabel('Water Level [cm]')
plt.ylabel('Measured Discharge [m3/s]')
plt.title('Weierbach')


RC_dummy=demo_guage.loc[demo_guage.Gauge=='Useldange']
opt_u, covar_u = so.curve_fit(RCf_fixu, RC_dummy.Level,RC_dummy.Q_m3s,maxfev = 100000)

plt.subplot(132)
plt.plot(RC_dummy.Level,RC_dummy.Q_m3s,'.',label='measured')
dummy_range = np.arange(250)
plt.plot(dummy_range,RCf_fixc(dummy_range,opt_u[0],opt_u[1]),'-',label='fitted')
plt.text(20,60,''.join(['a = ',str(np.round(opt_u[0],2)),'\nb = ',str(np.round(opt_u[1],2))]))
#legend(loc=2)
plt.xlabel('Water Level [cm]')
#ylabel('Measured Discharge [m3/s]')
plt.title('Useldange')


RC_dummy=demo_guage.loc[demo_guage.Gauge=='Huewelerbach']
opt_h, covar_h = so.curve_fit(RCf_fixh, RC_dummy.Level,RC_dummy.Q_m3s,maxfev = 100000)

plt.subplot(133)
plt.plot(RC_dummy.Level,RC_dummy.Q_m3s,'.',label='measured')
dummy_range = np.arange(30)
plt.plot(dummy_range,RCf_fixh(dummy_range,opt_h[0],opt_h[1]),'-',label='fitted')
plt.text(10,0.2,''.join(['a = ',str(np.round(opt_h[0],2)),'\nb = ',str(np.round(opt_h[1],2))]))
#legend(loc=2)
plt.xlabel('Water Level [cm]')
#ylabel('Measured Discharge [m3/s]')
plt.title('Huewelerbach')


#%%rating function definition...

def RCf_colpach(H):
    #Calculate flux [m3/s] from a given water level [cm] at gauge Colpach
    c=11.
    a=opt[0]
    b=opt[1]
    return a*((H-c)/100.)**b
def RCf_weierbach(H):
    c=10.2
    a=opt_w[0]
    b=opt_w[1]
    return a*((H-c)/100.)**b

def RCf_useldange(H):
    c=5.
    a=opt_u[0]
    b=opt_u[1]
    return a*((H-c)/100.)**b

def RCf_huewelerbach(H):
    c=8.
    a=opt_h[0]
    b=opt_h[1]
    return a*((H-c)/100.)**b

# so we now have from the scipy.optimize the a and b vars

#%%
#read file:
GA = pd.read_csv(r"E:\Mitacs\decharge_fluviale\Scripts\ratingCurve\demoData\Gauges_Attert.csv")
#define time stamp as index
GA.index=pd.to_datetime(GA.iloc[:,0].values)
#drop old time stamp column
GA=GA.drop('Unnamed: 0',axis=1)

print('These are measured water levels in cm:')
GA.head()

#copy the data frame:
QA = GA.copy()

#apply rating curves:
QA.Colpach=RCf_colpach(QA.Colpach)
QA.Weierbach=RCf_weierbach(QA.Weierbach)
QA.Useldange=RCf_useldange(QA.Useldange)
QA.Huewelerbach=RCf_huewelerbach(QA.Huewelerbach)
#%%
#plot the data
QA.plot()
plt.title('Attert Gauges')
plt.ylabel('Q [m3/s]')


