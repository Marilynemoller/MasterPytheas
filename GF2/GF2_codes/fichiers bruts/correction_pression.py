# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 10:10:07 2021

@author: emmaj
"""
#################
### libraries ###
#################

import pandas as pd
from datetime import datetime
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.dates as dt


#### paramètres à préciser

fichier_atm = 'baro.csv'  #pressions atmosphériques
fichier_sonde = 'Sonde standard_37039_20210316_171006.csv'  #pressions eau
cadence = 0.5     # période d'acquisition
date1 = '2021-03-16 12:26:00'   #date de début
date2 = '2021-03-16	16:55:00'   #date de fin
corr = 0.28 #correction obtenue d'après la calibration




###################################    
#### conversion NKE en pression####
###################################

def func_h2bar(level):
            ''' Converts NKE height into pressure:
            equation from Saunders, P.M. 1981
            "Practical conversion of Pressure to Depth"
            Journal of Physical Oceanography, 11, 573-574    '''
            Profondeur=np.copy(level)
            c1=0.101
            c2=0.5*10**(-6)
            p=c1*(Profondeur) + (c2 *(Profondeur)**2)
            level=p
            message='{:.<40}{:.>20}'.format('Process: NKE height into pressure', 'Ok')  
            print (message)
            return level

#################
### conversion ##
#################

def conv(Pression):
        #convertit la pression en prof
            rho = 1028.5 #entre 1028 et 1029 d'après les profils CTD
            g = 9.81
            h = Pression*10**(5) / (rho*g)
            message='pression convertie en prof'  
            print (message)
            return h

###################
###imp data atm ###
###################

os.chdir('C:/Users/emmaj/Desktop/M1_S2 - OPB Biogéochimique et Biodiversité/Mesures en Mer/sortie/data/NKE/NKE/archives')
dateparse = lambda X: datetime.strptime(X,'%d/%m/%Y\t%H:%M:%S')
baro = pd.read_table(fichier_atm,header=11,
                      sep=';',
                      decimal=',',
                      usecols=[0,1,3,4],
                      names=["thedate", "thetime","level","temperature"],
                      parse_dates={"Date": ["thedate","thetime"]},
                      date_parser=dateparse,
                      skip_blank_lines=True)

baro=baro.set_index('Date')
baro['level']=baro['level']/100000


##################
###imp data eau###
##################

sonde = pd.read_table(fichier_sonde,header=6,
                      sep=';',
                      decimal=',',
                      usecols=[1,2,3],
                      names=["level","thedate", "thetime"],
                      parse_dates={"Date": ["thedate","thetime"]},
                      date_parser=dateparse,
                      #delim_whitespace = True,
                      #delimiter='\s+',
                      #skiprows=100202,
                      #nrows=2537035,
                      dtype={'level':np.float64},
                      skip_blank_lines=True)
if cadence == 0.25 :
    sonde['NewDate'] = pd.date_range(sonde.Date[0], periods=len(sonde), freq="0.25S")
if cadence == 0.5 :
    sonde['NewDate'] = pd.date_range(sonde.Date[0], periods=len(sonde), freq="0.5S")
sonde=sonde.set_index('NewDate')
sonde['Pression']=func_h2bar(sonde['level'])




####################
###interpolations###
####################

if cadence == 0.25 :
    upsampled = baro.resample('0.25S')
if cadence == 0.5 :
    upsampled = baro.resample('0.5S')
baro_interpolated = upsampled.interpolate()
baro_interpolated.query('index > @sonde.index[0] and index < @sonde.index[-1]')


####################
###Correction    ###
####################
sonde['PressioncorrigeePam']=sonde['Pression']-baro_interpolated['level']
sonde['hauteurcorrigeePam']=conv(sonde['PressioncorrigeePam'])

###################
### Calibration ###
###################

calib = [corr]*len(sonde['hauteurcorrigeePam'])
sonde['hauteurcorrigeecalibree']=sonde['hauteurcorrigeePam']-calib        


###########################
# CUTTING IRRELEVANT DATA

formatemps = '%Y-%m-%d %H:%M:%S'
X1 = datetime.strptime(date1, formatemps)
X2 = datetime.strptime(date2, formatemps)


for i in range(len(sonde.index)) :
    if sonde.index[i] == X1:
        i1 = i
for i in range(len(sonde.index)) :
    if sonde.index[i] == X2:
        i2 = i
     
indexNamesi1 = sonde.index[:i1]
indexNamesi2 = sonde.index[i2:]


sonde.drop(indexNamesi1, inplace = True)
sonde.drop(indexNamesi2, inplace = True)




############################################
### Visualisation graphique vite fait   ####
############################################

plt.plot(sonde.index, sonde.level, 'b')
plt.plot(sonde.index, sonde.hauteurcorrigeePam, 'r')
plt.show()


