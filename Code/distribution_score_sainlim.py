# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 10:56:11 2020

@author: eloda
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sg_scores = pd.read_csv("scores_sainlim_ssgroupes.csv",sep = ",",encoding = 'latin-1')

print(sg_scores.head())

i = 0
for col in sg_scores.columns: 
    print(i,col)
    i += 1
    
def ajout_code_al(data):
    
    liste_code = []
    for i in range(len(data)):
        code = [int(data.iloc[[i],0]),int(data.iloc[[i],2])]
        liste_code.append(code)
    
    data["code_sougr"] = liste_code
    return(liste_code)    
    
    
    
def distrib_aliments(data):
    
    
    lib = list(data.iloc[:,3])
    x = data.iloc[:,6]
    y = data.iloc[:,5]
    
    plt.scatter(x, y)
    plt.annotate(lib[0], (x[0],y[0]))
    for i in range(1,len(lib)):
        if x[i]!= x[i-1] and y[i] != y[i-1]:
            plt.annotate(lib[i], (x[i], y[i]))
    
    plt.plot([7.5,7.5],[0,60],'go--', linewidth=2, marker=None)
    plt.plot([0,70],[5,5],'go--', linewidth=2,marker=None)
    plt.xlabel('LIM3')
    plt.ylabel('SAIN5opt')
    plt.title("Distribution des sous-groupes d'aliments en appliquant (SAIN 5opt, LIM 3)")
    plt.show()
        
        
    
ajout_code_al(sg_scores)
distrib_aliments(sg_scores)

#export_csv = sg_scores.to_csv('scores_sainlim_ssgroupes_codes.csv',index=False)