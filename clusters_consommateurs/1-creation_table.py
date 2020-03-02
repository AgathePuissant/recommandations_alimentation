# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 17:08:50 2020

@author: lili-

"""


import pandas as pd
# import numpy as np
# import mca as mca

# Fonction de catégorisation pour les bases

def categorisation(df, caracteristique, liste_cat, liste_seuils):
    """
    df : data frame à modifier
    caracteristique: str nom de la variable à modifier
    liste_cat : liste avec les noms des catégories
    liste_seuils : liste avec les seuils a prendre en compte de la façon suivante
    
    /!\ len(liste_seuils) == len(liste_cat)+1
    
    caracteristique < liste_seuils[0] --> liste_cat[0]
    for i in range(1,n-1) :
        liste_seuils[i-1]< caracteristique < liste_seuils[i] --> liste_cat[i])
    caracteristique > liste_seuils[n] --> liste_cat[n-1])
    """
    n = len(liste_cat)
    df.loc[(df[caracteristique]<liste_seuils[0])|(df[caracteristique]==liste_seuils[0]), caracteristique] = liste_cat[0]
    for i in range(1,n-1):
        df.loc[(df[caracteristique]>liste_seuils[i-1])&(df[caracteristique]<liste_seuils[i])|(df[caracteristique]==liste_seuils[i]), caracteristique] = liste_cat[i]
    df.loc[df[caracteristique]>liste_seuils[n-2], caracteristique] = liste_cat[n-1]
    
def listes_cat_seuil (df, liste_var, quantiles) :
    liste_seuils = []
    for i in liste_var :
        liste_seuils+=[(i,[df[i].describe()[j] for j in quantiles])]
    return(liste_seuils)


file = 'C:/Users/lili-/Desktop/PROJET_FIL_ROUGE/tables/Base_brute/Table_indiv.csv'
file_conso = 'C:/Users/lili-/Desktop/PROJET_FIL_ROUGE/tables/comportement_consommateur.csv'

df_consommateurs = pd.read_csv(file, sep = ";", encoding = 'latin-1')
df_consommations = pd.read_csv(file_conso, sep = ";", encoding = 'latin-1')

df_18=pd.DataFrame(df_consommateurs[['nomen','sexeps','tage','bmi']]) #.loc[df_consommateurs['tage']>3]

#sexeps : 1, 2, nan --> nan = 0 

df_18['sexeps'] = df_18['sexeps'].fillna(0)

    # moins de 16,5   dénutrition ou anorexie       0
    #   16,5 à 18,5   maigreur                      1 --> 0
    #     18,5 à 25   poids normal                  2 --> 1
    #       25 à 30   surpoids                      3 --> 1
    #       30 à 35   obésité modérée               4 --> 2
    #       35 à 40   obésité sévère                5 --> 2
    #    plus de 40   obésité morbide ou massive    6 --> 2

categorisation(df_18, 'bmi', [0,1,2], [18.5, 25, 30])


liste_caract = ['nomen' ,'fromages','fruits','légumes (hors pommes de terre)', 'poissons', 'ultra-frais laitier', 'viande', 'volaille et gibier']
df_preferences = pd.DataFrame(df_consommations[liste_caract]) #.loc[df_consommations['v2_age']>17]
        
liste_variables = ['fromages','fruits','légumes (hors pommes de terre)', 'poissons', 'ultra-frais laitier', 'viande', 'volaille et gibier']

liste_seuils_alim = listes_cat_seuil(df_preferences, liste_variables, ['50%'])

for i in liste_seuils_alim :
    categorisation(df_preferences, i[0], [0,1], i[1])
    
df_18['bmi'] = df_18['bmi'].fillna(1)

#df_18 = df_18.drop(columns=['tage'])
#df_preferences = df_preferences.drop(columns=['v2_age'])
    
table_analyse_acm = pd.DataFrame.merge(df_18,df_preferences, on = 'nomen')

table_analyse_acm.to_csv('table_analyse_3.csv', index=False)


