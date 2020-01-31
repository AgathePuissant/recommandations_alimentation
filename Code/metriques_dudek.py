# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 11:21:31 2020

@author: agaca
"""

import numpy as np
from motifs_frequents_substituabilite import *

'''
               ###########################################################
               #                                                         #
               #                   Fonctions de métriques                #
               #                                                         #
               ###########################################################
'''


def basic_dudek(R1,R2) :
    '''
    Fonction qui renvoie un dictionnaire contenant :  
        - la métrique de recouvrement entre deux sets de règles d'association : rules_overlap
        - la différence moyenne de support entre ces deux sets : supp_diff
        - la différence moyenne de confiance entre ces deux sets : con_diff
    --------------
        - R1, R2 : DataFrame de règles d'association obtenus avec le module mlxtend
    '''
    R1_inter_R2 = pd.merge(R1, R2, how='inner', on=['antecedents','consequents'])
    
    R1_union_R2 = pd.merge(R1, R2, how='outer', on=['antecedents','consequents'])
    
    card_R1_union_R2=len(R1_union_R2)
    print(card_R1_union_R2)
    card_R1_inter_R2 = len(R1_inter_R2)
    print(card_R1_inter_R2)
    
    sum_diff_supp = (abs(R1_inter_R2['support_x']-R1_inter_R2['support_y'])).sum()
    sum_diff_con = (abs(R1_inter_R2['confidence_x']-R1_inter_R2['confidence_y'])).sum()
    
    rules_overlap = card_R1_inter_R2 /card_R1_union_R2
    supp_diff = (sum_diff_supp + card_R1_union_R2 - card_R1_inter_R2)/card_R1_union_R2
    con_diff = (sum_diff_con + card_R1_union_R2 - card_R1_inter_R2)/card_R1_union_R2
    
    return {"rules_overlap" : rules_overlap, "supp_diff" : supp_diff, "con_diff" : con_diff}


def MRC(D,s,g,bs) :
    '''
    Fonction qui renvoie la matrice de comparaison des règles d'un dataset,
    qui permet d'étudier l'uniformité du dataset et donc qui permet de savoir 
    s'il est pertinent de séparer ce dataset en sous-datasets. Pour ce faire, on regarde 
    le recouvrement des règles d'associations sur des sous blocs de transactions du datasets
    de base.
    -----------------
        - D : datasets de transactions
        - s : seuil de support choisi
        - g : seuil de confiance choisi
        - bs : taille des blocs
    '''
    
    mrc=np.zeros((len(D)//bs,len(D)//bs))
    
    for i in range(len(D)//bs) :
        pi=D.loc[i*bs:i*bs+bs+1]
    
        for j in range(len(D)//bs) :
            
            print(i,j)
            
            pj=D.loc[j*bs:j*bs+bs+1]
            
            if i>=j :
                
                motifs_pi = find_frequent(pi, seuil_support = s, algo = fpgrowth)
                print("Motifs_1 trouvés")
                regles_pi = regles_association(motifs_pi,confiance = g)
                print("Règles_1 trouvées")
                
                motifs_pj = find_frequent(pj, seuil_support = s, algo = fpgrowth)
                print("Motifs_2 trouvés")
                regles_pj = regles_association(motifs_pj,confiance = g)
                print("Règles_2 trouvées")
                
                mrc[i,j]=basic_dudek(regles_pi,regles_pj)["rules_overlap"]
            
    return mrc
            

def RDU(D,mrc) :
    '''
    Fonction qui renvoie la Rule Distribution Uniformity (RDU) pour le dataset de transaction
    donné, qui est une métrique de l'uniformité du dataset.
    ----------
        - D : dataset de transaction
        - mrc : matrice de comparaison des règles
    '''
    
    m = (len(D)/(2*(1/len(mrc))*len(D)))*((len(D)/((1/len(mrc))*len(D)))-1)
    
    return (1/m)*np.sum(mrc)

'''
               ###########################################################
               #                                                         #
               #                      Code Principal                     #
               #                                                         #
               ###########################################################
'''

tyrep = 3
cluster = 1
avecqui = 2
tyrep_str='dejeuner'
cluster_str='cluster_1'
avecqui_str='famille'

supp = 0.001
conf = 0.01

#Méthode 1

motifs_1 = find_frequent(conso_pattern_sougr, seuil_support = supp, algo = fpgrowth)
print("Motifs fréquents trouvés") 
regles_1 = regles_association(motifs_1,confiance = conf)
print("Règles d'association trouvées")
regles_filtre_1 = filtrage(regles_1, tyrep_str, cluster_str, avecqui_str)
print("Règles d'association filtrées")

R1=regles_filtre_1
R1=R1[R1['antecedents']!=(tyrep_str,tyrep_str,avecqui_str)]
R1['antecedents'] = R1['antecedents'].apply(lambda y : tuple(x for x in y if (x!= tyrep_str and x!=cluster_str and x!=avecqui_str)))

#Méthode 2

cols = [i for i in range(127,138)]

conso_pattern_sougr_2=conso_pattern_sougr[(conso_pattern_sougr['tyrep']==tyrep) & (conso_pattern_sougr['cluster_consommateur']==cluster) & (conso_pattern_sougr['avecqui']==avecqui)]
conso_pattern_sougr_2.drop(conso_pattern_sougr_2.columns[cols],axis=1,inplace=True)
motifs_2 = find_frequent(conso_pattern_sougr_2, seuil_support = supp, algo = fpgrowth)
print("Motifs fréquents trouvés") 
regles_2 = regles_association(motifs_2,confiance = conf)
print("Règles d'association trouvées")

R2=regles_2

#Méthode 3

conso_pattern_sougr_3 = conso_pattern_sougr.drop(conso_pattern_sougr.columns[cols],axis=1)
motifs_3 = find_frequent(conso_pattern_sougr_3, seuil_support = supp, algo = fpgrowth)
print("Motifs fréquents trouvés") 
regles_3 = regles_association(motifs_3,confiance = conf)
print("Règles d'association trouvées")

conso_pattern_sougr_subset = conso_pattern_sougr[(conso_pattern_sougr[tyrep_str]==1) & (conso_pattern_sougr[cluster_str]==1) & (conso_pattern_sougr[avecqui_str]==1)]

regles_3['union'] = regles_3['antecedents']+regles_3['consequents']

regles_3['supp_union'] = regles_3['union'].apply(lambda x: np.sum(conso_pattern_sougr_subset[list(x)].all(axis=1)))
regles_3['supp_x'] = regles_3['antecedents'].apply(lambda x: np.sum(conso_pattern_sougr_subset[list(x)].all(axis=1)))
#regles_3['supp_y'] = regles_3['consequents'].apply(lambda x: np.sum(conso_pattern_sougr_subset[list(x)].all(axis=1)))

regles_3=regles_3[~((regles_3['supp_union']==0) | (regles_3['supp_x']==0))]

regles_3['confidence'] = regles_3['supp_union']/regles_3['supp_x']

regles_3['support'] = regles_3['supp_union']/len(regles_3)

R3=regles_3[(regles_3['support']>supp) & (regles_3['confidence']>conf)]

res12=basic_dudek(R1,R2)
res13=basic_dudek(R1,R3)
res23=basic_dudek(R2,R3)

#
#supp=0.01
#conf=0.01
#
#res_mrc=MRC(conso_pattern_sougr,supp,conf,2677)
#rdu=RDU(conso_pattern_sougr,res_mrc)
#
#res_mrc[res_mrc==0]=1
#
#import seaborn as sns
#
#mask = np.triu(np.ones_like(res_mrc, dtype=np.bool))


#sns.heatmap(res_mrc,mask=mask,cmap='Blues_r',annot=True)
