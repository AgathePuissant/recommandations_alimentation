# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 14:19:05 2020

@author: ADMIN
"""

import pandas as pd
import motifs_frequents_substituabilite as mf
from mlxtend.frequent_patterns import fpgrowth

conso_pattern_sougr = pd.read_csv("Base_a_analyser/conso_pattern_sougr_transfo.csv",sep = ";", encoding = 'latin-1')
nomenclature = pd.read_csv("Base_a_analyser/nomenclature.csv",sep = ";", encoding = 'latin-1')
sainlim = pd.read_csv('Base_Gestion_Systeme/scores_sainlim_ssgroupes.csv',sep=';',encoding="latin-1")

#global supp, conf
supp = 0.001
conf = 0.001   

motifs = mf.find_frequent(conso_pattern_sougr, seuil_support = supp, algo = fpgrowth)
regles = mf.regles_association(motifs, confiance = conf, support_only = False, support = supp)



def score_contextes() :    
    
    liste_tyrep = ['petit-dejeuner', 'dejeuner', 'gouter', 'diner']
    liste_cluster = ['cluster_1', 'cluster_2', 'cluster_3', 'cluster_4', 'cluster_5', 'cluster_6', 'cluster_7', 'cluster_8']
    liste_avecqui = ['seul', 'accompagne']
    
    colnames = ['cluster', 'tyrep', 'avecqui', 'consequents', 'confidence', 'Score confiance', 'Score biblio', 'Score combiné']
    score_par_contextes = pd.DataFrame(columns = colnames)
    
    for tyrep in liste_tyrep :
        for cluster in liste_cluster :
            for avecqui in liste_avecqui :
                regles_filtre = mf.filtrage(regles, tyrep, cluster, avecqui)
                print(tyrep, cluster, avecqui, len(regles_filtre))
                if regles_filtre.shape[0] > 0 :
                    
                    # Création de la table de substitution
                    t_subst = mf.tableau_substitution(regles_filtre, nomenclature)
                    
                    # Calcul du score de substitution
                    score = mf.matrice_scores_diff_moy(t_subst, regles_filtre)
                    
                    # Ajout des colonnes de cluster, type_rep et avecqui
                    score = pd.concat([pd.DataFrame(columns = colnames[:3]), score], sort = False)
                    score[colnames[:3]] = ['cluster_1', 'petit-dejeuner', 'seul']
                    
                    # Ajout de la table partielle de score dans score_par_contextes
                    score_par_contextes = score_par_contextes.append(score)
    
    # Reset index nécessaire pour la transformation qui suit
    score_par_contextes.reset_index(drop = True, inplace = True)
    
    # Transformation de la colonne conséquents à deux colonnes aliment_1 et aliment_2
    score_par_contextes = pd.concat([score_par_contextes.iloc[:, 0:3], 
                                     pd.DataFrame(score_par_contextes['consequents'].tolist()).rename(
                                             columns = {0 : 'aliment_1', 1 : 'aliment_2'}),
                                     score_par_contextes.iloc[:, -1:].rename(
                                             columns = {'Score combiné' : 'score_substitution'})],
                                     axis = 1)
    
    
    return score_par_contextes

def add_score_sainlim(data, sainlim) :
    
    data = pd.DataFrame.merge(pd.DataFrame.merge(data, sainlim.loc[:,['libsougr', 'distance_origine']],
                                           left_on = 'aliment_1', right_on = 'libsougr', how = 'left').rename(
                                                   columns = {'distance_origine' : 'score_sainlim_1'}),
                                     sainlim.loc[:,['libsougr', 'distance_origine']],
                                     left_on = 'aliment_2', right_on = 'libsougr', how = 'left').rename(
                                                   columns = {'distance_origine' : 'score_sainlim_2'})
test = score_contextes()

d = test





