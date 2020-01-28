# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 11:50:29 2020

@author: eloda
"""

import pandas as pd
from copy import deepcopy

def dico_nomenclature(nom):
    """
    Prend en entrée la table nomenclature et retourne un dictionnaire dont les
    clés sont les sous-groupes d'aliments et les valeurs leur rôle
    """
    
    dico_nom = {list(nom.iloc[[0],3])[0]:list(nom.iloc[[0],7])[0]}

    for i in range(1,len(nom)):
        #Si on passe à un nouveau sous-groupe, on créé une nouvelle clé dans le dico
        if list(nom.iloc[[i],3])[0] != list(nom.iloc[[i-1],3])[0]:
            dico_nom[list(nom.iloc[[i],3])[0]] = list(nom.iloc[[i],7])[0]
            
    return dico_nom
        



def preferences_conso(data, dico_nom, cluster, rang_ini):
    """
    Prend en entrée :
         - data : la table consommation avec sous-groupes et clusters (dataframe)
         - dico_nom : dictionnaire de sortie de dico_nomenclature (dictionnaire)
         - cluster : le numéro du cluster considéré (int)
         - rang_ini : le rang dans la dataframe data à partir duquel le cluster
         commence (int)
         
    Renvoie dico_cluster un dictionnaire composé comme suit :
    On créé des dictionnaires avec les aliments en clés et leur fréquence d'apparition
    en valeur pour chaque rôle dans le repas, et ces dictionnaires sont eux-mêmes
    les composants de dictionnaires pour chaque type de repas (petit-déjeuner,
    déjeuner, collation, dîner). 
    """
    
    #dico permettant d'initialiser les dictionnaires de repas
    #Contient tous les rôles au sein d'un repas en clé et un dictionnaire en valeur,
    #pour le moment composé uniquement d'un compteur initialisé à 0 et de la clé
    #aucun qui compte le nombre de repas pour lequel ce role n'est pas représenté.
    dico_repas_init = {'compteur':0} 
    #Dico avec les roles en clés et des 0 en valeurs permettant de stocker quel
    #role a été vu pour une obervation donnée
    stock_roles = {} 
    for role in dico_nom.values():
        dico_repas_init[role] = {'aucun':0} 
        stock_roles[role] = 0

    
    #Ancienne implémentation, plus générale mais trop longue
    
#    dico_general = {}
#
#    for i in range(1000):
#        print(i)
#        
#        if int(data.iloc[[i],0]) not in dico_general.keys():
#            dico_general[int(data.iloc[[i],0])] = {}
#        
#        dico_cluster = dico_general[int(data.iloc[[i],0])]
    
#
#        if int(data.iloc[[i],3]) == 1 or int(data.iloc[[i],3]) == 3 or int(data.iloc[[i],3]) == 5:
#            if int(data.iloc[[i],3]) not in dico_cluster.keys():
#                dico_cluster[int(data.iloc[[i],3])] = dico_role
#            
#            dico_repas = dico_cluster[int(data.iloc[[i],3])]
#            
#        #On regroupe toutes les collations dans le même type de repas
#        else :
#            if 4 not in dico_cluster.keys():
#                dico_cluster[4] = dico_role
#            
#            dico_repas = dico_cluster[4]
#            
#   
    dico_cluster = {1:deepcopy(dico_repas_init),3:deepcopy(dico_repas_init),4:deepcopy(dico_repas_init),5:deepcopy(dico_repas_init)}
    
    i = rang_ini
    #Tant qu'on est dans le bon cluster et mais à la fin du dataframe
    while int(data.iloc[[i],0]) == cluster and i < 500 :
        print(i)
        
        #On trouve le dictionnaire correspondant au type de repas de l'observation i
#        if int(data.iloc[[i],3]) in dico_cluster.keys():
        dico_repas = dico_cluster[int(data.iloc[[i],3])]
        dico_repas['compteur'] += 1
        
#        else:
#            #On regroupe toutes les collations dans le même type de repas
#            dico_repas = dico_cluster[4]
            
        #On parcourt la ligne pour trouver les aliments consommés dans cette observation    
        for k in range(len(list(data.iloc[i,4:126]))):
            
            if list(data.iloc[i,4:126])[k] == 1:
                aliment = data.columns[k+4]
                role = dico_nom[aliment]
                stock_roles[role] += 1
#                if role not in dico_repas.keys():
#                    dico_repas[role] = {}
                
                #On trouve le dictionnaire qui correspond au rôle de l'aliment trouvé
                dico_role = dico_repas[role]
                                       
#                if 'compteur' not in dico_role.keys():
#                    dico_role['compteur']  = 1
#                else:
#                    dico_role['compteur']  += 1
#                
                #dico_role['compteur']  += 1
                #Si l'aliment n'est pas encore présent dans le dictionnaire, on créé la clé
                #correspondre
                if aliment not in dico_role.keys():
                    dico_role[aliment] = 1
                #Sinon on incrémente de 1
                else:
                    dico_role[aliment] += 1
                    
        #On trouve les rôles qui ne sont pas représentés dans ce repas et on
        #incrémente de 1 la variable aucun de ces rôles
        for role in stock_roles.keys():
            if stock_roles[role] == 0:
                dico_repas[role]['aucun'] += 1
            else:
                stock_roles[role] = 0

        i += 1                
                
    return dico_cluster
        


def dico_frequence(dico_cluster):
    """
    Transforme dans le dictionnaire généré par preferences_conso les nombres de
    consommation de chaque aliment en pourcentage de consommation pour le role donné
    """
    for repas in dico_cluster.keys():
        for role in dico_cluster[repas].keys():
            if role != 'compteur':
                for aliment in dico_cluster[repas][role].keys():
                    print(dico_cluster[repas]['compteur'])
                    dico_cluster[repas][role][aliment] = dico_cluster[repas][role][aliment]/dico_cluster[repas]['compteur']
    
    return dico_cluster
        

 
 

data = pd.read_csv('conso_pattern_sougr_transfo.csv',sep = ";",encoding = 'latin-1')
nomenclature = pd.read_csv('nomenclature.csv',sep = ";",encoding = 'latin-1')
#print(nomenclature.head())
#i = 0
#for col in data.columns: 
#    print(i,col)
#    i += 1
    
dico_nom = dico_nomenclature(nomenclature)
pref = preferences_conso(data, dico_nom, 0,0)
pref_frequence = dico_frequence(pref)