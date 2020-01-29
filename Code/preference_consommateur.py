# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 11:50:29 2020

@author: ADMIN
"""

import pandas as pd


def construct_table_preference(data_conso, data_nomen) :
    
    # Input base de preference
    pref = data_conso.copy()
    pref = pref.drop(['avecqui', 'petit-dejeuner', 'dejeuner', 'gouter', 'diner',
                      'seul', 'amis', 'famille', 'autre', 'cluster_0', 'cluster_1', 'cluster_2'], axis = 1)
    
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
    
    # Taux_apparaitre = nombre de repas qui contient chaque code de role divisé par nombre de repas par groupe de cluster + type de repas
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
    
    return pref


## DONNÉES
conso_pattern_sougr = pd.read_csv('conso_pattern_sougr_transfo.csv',sep = ";",encoding = 'latin-1')
conso_pattern_sougr = conso_pattern_sougr.rename(columns = {'b\x9cuf en pièces ou haché' : 'boeuf en pièces ou haché'})

nomenclature = pd.read_csv("nomenclature.csv",sep = ",",encoding = 'latin-1')
nomenclature['libsougr'] = nomenclature['libsougr'].replace('b\x9cuf en pièces ou haché', 'boeuf en pièces ou haché')

# TEST DE FONCTION
table_preference = construct_table_preference(conso_pattern_sougr, nomenclature)