# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 13:46:14 2020

@author: lili-
"""

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import pandas as pd

path = 'C:/Users/lili-/Desktop/PROJET_FIL_ROUGE/tables/comportement_consommateur.csv'
path_conso = 'tables/consommation.csv'

df_bilan = pd.read_csv(path, sep = ";", encoding = 'latin-1')

consommation = pd.read_csv(path_conso, sep = ";", encoding = 'latin-1')

# PCA

df_bilan = df_bilan.fillna(0)

pca_conso = PCA(n_components=3)
pca_conso.fit(df_bilan.iloc[:,1:])
print(sum(pca_conso.explained_variance_ratio_))
print(pca_conso.get_covariance())

PCA_consommateurs = pca_conso.fit_transform(df_bilan.iloc[:,1:])

PCA_consommateurs = pd.DataFrame(data = PCA_consommateurs,columns = ['PC1', 'PC2', 'PC3'])
PCA_consommateurs = pd.concat([df_bilan[['nomen']], PCA_consommateurs], axis = 1) 

km_conso = KMeans(n_clusters=3, random_state=0).fit(PCA_consommateurs)

PCA_consommateurs = pd.concat([PCA_consommateurs,pd.DataFrame(km_conso.labels_, columns = ['cluster_consommateur'])], axis = 1)
PCA_consommateurs = PCA_consommateurs.loc[:,['nomen','cluster_consommateur']]

consommation = pd.DataFrame.merge(consommation, PCA_consommateurs, on = 'nomen')

consommation['contexte'] = consommation.groupby(['tyrep','cluster_consommateur']).grouper.group_info[0]

consommation.to_csv('consommation.csv', index=False)
