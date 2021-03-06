# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 14:19:05 2020

@author: chulai
"""
# =============================================================================
# IMPORT LIBRARY

import pandas as pd
import motifs_frequents_substituabilite as mf
from mlxtend.frequent_patterns import fpgrowth

# =============================================================================


# =============================================================================
# FUNCTIONS

def score_substitution_contextes(regles_global) :    
    
    """
    La fonction qui à partir de la table des règles d'association globale calcule le score de substitutiabilité pour toutes les substitutions par contexte.
    
    INPUT :
        1, regles_globale: table des règles d'association globale qui résulte des fonctions du module motifs_frequents_substituabilite -- df
    
    OUTPUT :
        1, score_sub_contextes : table de score de substitutiabilité des substitutions par contexte de consommation -- df
    """
    
    liste_tyrep = ['petit-dejeuner', 'dejeuner', 'gouter', 'diner']
    liste_cluster = ['cluster_1', 'cluster_2', 'cluster_3', 'cluster_4', 'cluster_5', 'cluster_6', 'cluster_7', 'cluster_8']
    liste_avecqui = ['seul', 'accompagne']
    
    colnames = ['cluster', 'tyrep', 'avecqui', 'couples_alim', 'score']
    score_sub_contextes = pd.DataFrame(columns = colnames)
    score_sub_contextes_ssavecqui = pd.DataFrame(columns = colnames)
    score_sub_contextes_ssavecquicluster = pd.DataFrame(columns = colnames)
    
    for tyrep in liste_tyrep :
        
        regles_filtre_ssavecquicluster = mf.filtrage(regles_global, tyrep, '', '')
        print(tyrep, '', '', len(regles_filtre_ssavecquicluster))    
        if len(regles_filtre_ssavecquicluster) > 0 :
                
                # Création de la table des couples
                couples_ssavecquicluster = mf.creation_couples(regles_filtre_ssavecquicluster, nomenclature)
                
                # Calcul du score de substitution
                score_contexte_ssavecquicluster = mf.score_substitution(couples_ssavecquicluster, regles_filtre_ssavecquicluster)
                
                # Ajout des colonnes de cluster, type_rep et avecqui
                score_contexte_ssavecquicluster = pd.concat([pd.DataFrame(columns = colnames[:3]), score_contexte_ssavecquicluster], sort = False)
                score_contexte_ssavecquicluster[colnames[:3]] = ['all' , tyrep, 'all']
                
                # Ajout de la table partielle de score dans score_par_contextes 
                score_sub_contextes_ssavecquicluster = score_sub_contextes_ssavecquicluster.append(score_contexte_ssavecquicluster)
        
        for cluster in liste_cluster :
            
            regles_filtre_ssavecqui = mf.filtrage(regles_global, tyrep, cluster, '')
            print(tyrep, cluster, '', len(regles_filtre_ssavecqui))
            if len(regles_filtre_ssavecqui) > 0 :
                    
                    # Création de la table des couples
                    couples_ssavecqui = mf.creation_couples(regles_filtre_ssavecqui, nomenclature)
                    
                    # Calcul du score de substitution
                    score_contexte_ssavecqui = mf.score_substitution(couples_ssavecqui, regles_filtre_ssavecqui)
                    
                    # Ajout des colonnes de cluster, type_rep et avecqui
                    score_contexte_ssavecqui = pd.concat([pd.DataFrame(columns = colnames[:3]), score_contexte_ssavecqui], sort = False)
                    score_contexte_ssavecqui[colnames[:3]] = [cluster, tyrep, 'all']
                    
                    # Ajout de la table partielle de score dans score_par_contextes 
                    score_sub_contextes_ssavecqui = score_sub_contextes_ssavecqui.append(score_contexte_ssavecqui)
            
            for avecqui in liste_avecqui :
                regles_filtre = mf.filtrage(regles_global, tyrep, cluster, avecqui)
                print(tyrep, cluster, avecqui, len(regles_filtre))
                if len(regles_filtre) > 0 :
                    
                    # Création de la table des couples
                    couples = mf.creation_couples(regles_filtre, nomenclature)
                    
                    # Calcul du score de substitution
                    score_contexte = mf.score_substitution(couples, regles_filtre)
                    
                    # Ajout des colonnes de cluster, type_rep et avecqui
                    score_contexte = pd.concat([pd.DataFrame(columns = colnames[:3]), score_contexte], sort = False)
                    score_contexte[colnames[:3]] = [cluster, tyrep, avecqui]
                    
                    # Ajout de la table partielle de score dans score_par_contextes 
                    score_sub_contextes = score_sub_contextes.append(score_contexte)
    
    # Reset index nécessaire pour la transformation qui suit
    score_sub_contextes.reset_index(drop = True, inplace = True)
    
    # Transformation de la colonne conséquents à deux colonnes aliment_1 et aliment_2
    score_sub_contextes = pd.concat([score_sub_contextes.iloc[:, 0:3], 
                                     pd.DataFrame(score_sub_contextes['couples_alim'].tolist()).rename(
                                             columns = {0 : 'aliment_1', 1 : 'aliment_2'}),
                                     score_sub_contextes.iloc[:, -1:].rename(
                                             columns = {'score' : 'score_substitution'})],
                                     axis = 1)
                                     
    # Reset index nécessaire pour la transformation qui suit
    score_sub_contextes_ssavecqui.reset_index(drop = True, inplace = True)
    
    # Transformation de la colonne conséquents à deux colonnes aliment_1 et aliment_2
    score_sub_contextes_ssavecqui = pd.concat([score_sub_contextes_ssavecqui.iloc[:, 0:3], 
                                     pd.DataFrame(score_sub_contextes_ssavecqui['couples_alim'].tolist()).rename(
                                             columns = {0 : 'aliment_1', 1 : 'aliment_2'}),
                                     score_sub_contextes_ssavecqui.iloc[:, -1:].rename(
                                             columns = {'score' : 'score_substitution'})],
                                     axis = 1)
                                     
                                     
    # Reset index nécessaire pour la transformation qui suit
    score_sub_contextes_ssavecquicluster.reset_index(drop = True, inplace = True)
    
    # Transformation de la colonne conséquents à deux colonnes aliment_1 et aliment_2
    score_sub_contextes_ssavecquicluster = pd.concat([score_sub_contextes_ssavecquicluster.iloc[:, 0:3], 
                                     pd.DataFrame(score_sub_contextes_ssavecquicluster['couples_alim'].tolist()).rename(
                                             columns = {0 : 'aliment_1', 1 : 'aliment_2'}),
                                     score_sub_contextes_ssavecquicluster.iloc[:, -1:].rename(
                                             columns = {'score' : 'score_substitution'})],
                                     axis = 1)
                                     
    scores = pd.concat(score_sub_contextes,score_sub_contextes_ssavecqui,score_sub_contextes_ssavecquicluster)
    
    return scores


def add_score_sainlim(score_sub_ori, sainlim) :
    
    """
    La fonction qui à partir de la table des scores de substitutiabilité calcule le score SAINLIM pour toutes les substitutions.
    
    INPUT :
        1, data : table qui résulte de la fonction score_substitution_contextes -- df
        2, sailim : table du score SAINLIM de tous les sous-groupes d'aliments -- df
    
    OUTPUT :
        1, score_par_contextes : table finale de score de substitutiabilité et de score SAINLIM des substitutions par contexte de consommation-- df
    """
    
    # Ajout du score sainlim de aliment_1 dans la table
    score_par_contextes = pd.DataFrame.merge(score_sub_ori, sainlim.loc[:,['libsougr', 'distance_origine']].rename(
            columns = {'distance_origine' : 'score_sainlim_1'}),
            left_on = 'aliment_1', right_on = 'libsougr', how = 'left').drop(
                    'libsougr', axis = 1)
    
    # Ajout du score sainlim de aliment_2 dans la table
    score_par_contextes = pd.DataFrame.merge(score_par_contextes, sainlim.loc[:,['libsougr', 'distance_origine']].rename(
            columns = {'distance_origine' : 'score_sainlim_2'}),
            left_on = 'aliment_2', right_on = 'libsougr', how = 'left').drop(
                    'libsougr', axis = 1)
                                         
    # Ajout du score sainlim de la substitution
    score_par_contextes['score_sainlim'] = score_par_contextes['score_sainlim_2'] - score_par_contextes['score_sainlim_1']
    
    # Normalisation du score sainlim à [0, 1]
    score_par_contextes = score_par_contextes[score_par_contextes['score_sainlim'] >= 0]
    score_par_contextes['score_sainlim_nor'] = (score_par_contextes['score_sainlim'] - score_par_contextes['score_sainlim'].min()) / (score_par_contextes['score_sainlim'].max() - score_par_contextes['score_sainlim'].min())
    
    return score_par_contextes



def main() :
    
    """
    La fonction qui importe les bases de données en globale puis lance deux fonctions score_substitution_contextes et add_score_sainlim.
    Cela est pour économiser le temps en important ce module dans d'autres fichier Python
    """
    
    global conso_pattern_sougr, nomenclature, sainlim_df, supp, conf
    
    # Load data
    conso_pattern_sougr = pd.read_csv("Base_a_analyser/conso_pattern_sougr_transfo.csv",sep = ";", encoding = 'latin-1')
    nomenclature = pd.read_csv("Base_a_analyser/nomenclature.csv",sep = ";", encoding = 'latin-1')
    sainlim_df = pd.read_csv('Base_Gestion_Systeme/scores_sainlim_ssgroupes.csv',sep=';',encoding="latin-1")
    
    # constant
    supp = 0.001
    conf = 0.001   
    
    # data preparation
    motifs = mf.find_frequent(conso_pattern_sougr, seuil_support = supp, algo = fpgrowth)
    regles = mf.regles_association(motifs, confiance = conf, support_only = False, support = supp)
    
    score_sub_contextes = score_substitution_contextes(regles)

    score_par_contextes = add_score_sainlim(score_sub_contextes, sainlim_df)
    
    
    return score_par_contextes

# =============================================================================

#score_par_contextes = main()
#score_par_contextes.to_csv("Base_Gestion_Systeme/score_par_contextes.csv", sep = ";", encoding = "latin-1", index = False)


