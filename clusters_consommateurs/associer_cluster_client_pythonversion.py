# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 15:02:54 2020

@author: liliana JALPA PINEDA
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from scipy.spatial.distance import pdist
#________________________Mise en forme table_______________________

file="C:/Users/lili-/Desktop/PROJET_FIL_ROUGE/clusters_consommateurs/table_analyse_3.csv"
table_analyser = pd.read_csv(file, sep = ",", encoding = 'latin-1')

cols = list(table_analyser.columns)
df_18=pd.DataFrame(table_analyser[cols].loc[table_analyser['tage']>3])


def creer_colonnes_table(df, modalites):
    cols = list(df.columns)
    for i in range(1,len(modalites)+1) :
        col = cols[i]
        mod = modalites[i-1]
        for j in range(mod-1):
            df[col+str(j+1)] = df[col]
        
   
def bool_col(df, names, valeurs): 
    for i in range(len(names)):
        name = names[i]
        val = valeurs[i]
        #print(name,val)
        df.loc[(df[name]!=val), name] = 'Wrong'
        df.loc[(df[name]==val), name] = 'Right'
        df.loc[(df[name]=="Wrong"), name] = False
        df.loc[(df[name]=='Right'), name] = True         
            
def booleaniser_table(df, modalites): #[3,2,2,2,2,3,5,2,2,2]
    cols = list(df.columns)
    sorted_cols = cols[1:]
    sorted_cols.sort()
    n = len(sorted_cols)
    i = 0
    j = 0
    mod = modalites[i]
    while i<n :
        #print("i1 : ",i," j1 : ",j, " mod1 : ", mod)
        names = sorted_cols[i:i+mod]
        if 'tage' in names :
            valeurs = [4,5,6,7,8]
        else :
            valeurs = [j for j in range(mod)]
        i+=mod
        if j < len(modalites)-1:
            j+=1
            mod = modalites[j]
        #print("i2 : ",i," j2 : ",j, " mod2 : ", mod)
        bool_col(df, names, valeurs)
            
creer_colonnes_table(df_18, [3,5,3,2,2,2,2,2,2,2])        
booleaniser_table(df_18, [3,2,2,2,2,3,5,2,2,2])

def fonction_gower(x_1,x_2):
    n_1 = len(x_1)
    n_2 = len(x_2) # x_2.shape[0]
    compteur = 0
    if n_1 == n_2 :
        for i in range(n_1):
            if x_1[i]==x_2[i]:
                compteur +=1
        return(compteur/n_1)
    return()

def distances(df, distance=None):
    #dimension = df.shape
    lignes = df.index
    n = len(lignes)
    X = []
    if distance == "Gower" :
        for i in range(n):
            j = lignes[i]
            for iprime in range(i+1,n):
                jprime = lignes[iprime]
                #df_i = list(df.loc[j])
                #df_iprime = list(df.loc[jprime])
                dist = fonction_gower(list(df.loc[j]),list(df.loc[jprime]))
                X+=[dist]
                #X[iprime][i]=dist
    return(np.array([X]))


#________________________Classif hierarchique ascendante_______________________
#df_skip = df_18.drop(columns=['nomen'])
#df_skip.reset_index(drop=True)

#X = distances(df_skip, 'Gower')
df_18 = df_18.drop(columns=['nomen'])
Xprime=pdist(df_18, 'hamming')
X = pdist(df_skip, fonction_gower)

Z= linkage(X, method='ward')
Zprime = linkage(Xprime, method='ward')

dendrogram(Zprime,labels=df_18.index,orientation='left')
fcluster(Zprime, t=4.3, criterion='distance')
dendrogram(Z,labels=df_18.index,orientation='left')

plt.show()        
