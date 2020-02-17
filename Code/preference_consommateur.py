# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 11:50:29 2020

@author: ADMIN
"""

import pandas as pd
import matplotlib.pyplot as plt
from copy import deepcopy


def construct_table_preference(data_conso, data_nomen) :
    
    # Input base de preference
    pref = data_conso.drop(['avecqui', 'petit-dejeuner', 'dejeuner', 'gouter', 'diner',
                      'seul', 'accompagne', 'autre', 'cluster_1', 'cluster_2','cluster_3','cluster_4','cluster_5','cluster_6','cluster_7','cluster_8'], axis = 1)
    
    
    # Transformation de colonne à ligne
    pref = pref.melt(id_vars = ['cluster_consommateur', 'nomen', 'nojour', 'tyrep'],
                     var_name = 'libsougr',
                     value_name = 'consommation')
    pref = pref[pref.consommation == 1]
    
    # Merge conso_pattern et nomenclature
    pref = pd.DataFrame.merge(pref, data_nomen.loc[:,['code_role', 'libsougr']].drop_duplicates(), on = 'libsougr', how = 'left')
    
    # Nbre de repas par cluster de consommateur et par type de repas : nbre_repas_grp
    conso_by_grp = pref.groupby(['cluster_consommateur', 'nojour', 'tyrep'])['nomen'].nunique().reset_index().rename(
            columns = {'nomen' : 'nbre_repas_grp'})
    conso_by_grp = conso_by_grp.groupby(['cluster_consommateur', 'tyrep'])['nbre_repas_grp'].apply(sum).reset_index()
    
    # Nombre de repas qui ont les aliments de chaque code_role par cluster de consommateur et par type de repas : nbre_repas_code
    conso_by_code = pref.groupby(['cluster_consommateur', 'nojour', 'tyrep', 'code_role'])['nomen'].nunique().reset_index().rename(
        columns = {'nomen' : 'nbre_repas_code'})
    conso_by_code = conso_by_code.groupby(['cluster_consommateur', 'tyrep', 'code_role'])['nbre_repas_code'].apply(sum).reset_index()
    
    # Taux_code_apparaitre = nombre de repas qui contient chaque code de role divisé par nombre de repas par groupe de cluster + type de repas
    conso_by_code = pd.DataFrame.merge(conso_by_code, conso_by_grp, on = ['cluster_consommateur', 'tyrep'])
    conso_by_code['taux_code_apparaitre'] = round(100*conso_by_code['nbre_repas_code']/conso_by_code['nbre_repas_grp'], 2)
    
    # Ajout des nouvelles colonnes dans la table
    pref = pd.DataFrame.merge(pref.drop(['nomen', 'nojour'], axis = 1), 
                              conso_by_code, 
                              on = ['cluster_consommateur', 'tyrep', 'code_role'] )
    
    # Nombre de repas qui contient chaque sous-groupe d'aliments par cluster de consommateur, type de repas, code de role
    pref = pref.groupby(['cluster_consommateur', 'tyrep', 'nbre_repas_grp', 'code_role',
                         'nbre_repas_code', 'taux_code_apparaitre', 'libsougr'])['consommation'].apply(sum).reset_index()
    
    # Taux_conso_par_code : nombre de repas qui contient chaque sous-groupe d'aliments divisé par nombre de repas de chaque code de role
    pref['taux_conso_par_code'] = round(100*pref['consommation']/pref['nbre_repas_code'], 2)
    #pref['taux_conso_par_grp'] = round(100*pref['consommation']/pref['nbre_repas_grp'], 2)
    
    return pref


## DONNÉES
#conso_pattern_sougr = pd.read_csv('Base_a_analyser/conso_pattern_sougr_transfo.csv',sep = ";",encoding = 'latin-1')
#nomenclature = pd.read_csv("Base_a_analyser/nomenclature.csv",sep = ";",encoding = 'latin-1')

# TEST DE FONCTION
#table_preference = construct_table_preference(conso_pattern_sougr, nomenclature)
#table_preference.to_csv('Base_Gestion_Systeme/preference_consommation.csv', sep = ";", encoding = 'latin-1', index = False)

def diversite(pref):
    
    pourc = [90,80,70,60,50,40,30,20,10,5,2,1]
    init = [0 for i in range(len(pourc))]
    init1 = [1 for i in range(len(pourc))]
    dico_frq = {1:init1,2:init,3:deepcopy(init),4:deepcopy(init),5:deepcopy(init),6:deepcopy(init),7:deepcopy(init),8:deepcopy(init)}
    
    for k in range(len(pourc)):
        j=1
        for i in range(1,len(pref)):
            
            if pref.iloc[i,8] >= pourc[k]:
                dico_frq[pref.iloc[i,0]][k] += 1
        
            if pref.iloc[i,0] != pref.iloc[i-1,0] or i == len(pref)-1:
                dico_frq[pref.iloc[i-1,0]][k] = dico_frq[pref.iloc[i-1,0]][k]/j
                j = 0     
                
            j += 1   
    
    return dico_frq


def trace_diversite(div):
    pourc = [90,80,70,60,50,40,30,20,10,5,2,1]
    for i in div.keys():
        print(i,div[i])
        plt.plot(pourc,div[i],label='cluster_'+str(i))
    
    plt.xlabel('fréquence minimale de consommation')
    plt.ylabel("Pourcentage d'aliments consommés à une fréquence supérieure à la fréquence minimale")
    plt.legend()
    plt.show()

#div = diversite(table_preference)
#print(div)
#trace_diversite(div)