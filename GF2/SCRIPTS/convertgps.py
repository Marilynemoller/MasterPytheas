#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 08:56:40 2021

@author: Nathan Kientz
"""
from pyproj import Proj, transform
import csv
import numpy as np

'------------NOM_DU_FICHIER-------------------------------'
my_file = open("210317matrix.txt","w+")

'-----------DONNEES---------------------------------------'
with open(file='frioul20210317.csv') as f:
    reader = csv.reader(f, delimiter=",")
    d = list(reader)
    n = len(d)

x = []
y = []

'----------CONVERTION_DES_DONNEES-------------------------'
for i in range(0,(n)):
    inproj = Proj(init='epsg:2154')
    outproj = Proj(init='epsg:4326')
    l = d[i][1]
    m = d[i][2] 
    x1,y1 = l, m
    x2,y2 = transform(inproj, outproj, x1,y1)
    x.append(x2)
    y.append(y2)


'----------ORGANISATION_DES_LISTES_SOUS_FORME_MATRICIEL----'
X=np.array(x)
Y=np.array(y)
results = np.vstack((x, y))
print(results)

'---------ECRITURE_DANS_FICHIER-----------------------------'
my_matrix = np.matrix(results)
np.savetxt('210317matrix.txt', my_matrix, delimiter = ';') 