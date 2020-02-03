# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 13:46:14 2020

@author: lili-
"""

import pandas as pd

path = 'C:/Users/lili-/Desktop/PROJET_FIL_ROUGE/simulation_consommateur/clusters_8.csv'
path_conso = 'C:/Users/lili-/Desktop/PROJET_FIL_ROUGE/tables/consommation.csv'

df_bilan = pd.read_csv(path, sep = ";", encoding = 'latin-1')

consommation = pd.read_csv(path_conso, sep = ";", encoding = 'latin-1')

# PCA

df_bilan = df_bilan.loc[:,['nomen','clust.num']]
consommation = pd.DataFrame.merge(consommation, df_bilan, on = 'nomen')

consommation['contexte'] = consommation.groupby(['tyrep','clust.num']).grouper.group_info[0]

consommation.to_csv('consommation.csv', index=False)
