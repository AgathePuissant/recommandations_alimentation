# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

from motifs_frequents_substituabilite import *

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
CODE PRINCIPAL
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

supp = 0.001
conf = 0.01

cluster_liste = [[0,'cluster_0'],[1,'cluster_1'],[2,'cluster_2']]

avecqui_liste = [[1,'seul'],[2,'famille'],[3,'amis'],[4,'autre'],[9,'pas rep']]

tyrep_liste = [[1,'petit-dejeuner'],[3,'dejeuner'],[4,'gouter'],[5,'diner']]

#---------Méthode avec contexte inclus dans la recherche de motifs fréquents---------------

#Modification pour que les modalités de cluster, type de repas et modalités sociale soient mises sous 
#forme booléenne. Transformation à faire uniquement dans le cas où on veut inclure ces modalités dans
#la recheche de motifs fréquents.

motifs = find_frequent(conso_pattern_sougr, seuil_support = supp, algo = fpgrowth)
print("Motifs fréquents trouvés") 
regles = regles_association(motifs,confiance = conf)
print("Règles d'association trouvées")

print(len(regles))

scores_tous_contextes = pd.DataFrame([])


for tyrep in tyrep_liste :
    
    for cluster in cluster_liste :
        
        for avecqui in avecqui_liste :
            
            print(tyrep)
            print(cluster)
            print(avecqui)
            
            regles_filtre = filtrage(regles, tyrep[1], cluster[1], avecqui[1])
            
            print("Taille des règles filtrées : "+str(len(regles_filtre)))
            
            if len(regles_filtre)>0 :
                
            
                t_subst = tableau_substitution(regles_filtre, nomenclature)
                
                print("Tableau de substitutions fait")
                print("Taille du tableau de substitution : "+str(len(t_subst)))
                
                if (t_subst.drop_duplicates(['consequents'])['code_role'].value_counts()>2).any():
                    
                    scores = matrice_scores_diff_moy(t_subst, regles_filtre)
                    print("Tableau de scores fait")
                    print("Taille des scores : "+str(len(scores)))
                    
                    score_specifique = scores['consequents'].rename(str(tyrep[1])+'-'+str(cluster[1])+'-'+str(avecqui[1])+'-couple')
                    couple_specifique = scores['Score combiné'].rename(str(tyrep[1])+'-'+str(cluster[1])+'-'+str(avecqui[1])+'-score')
                    
                    scores_tous_contextes = pd.concat([scores_tous_contextes,couple_specifique], axis=1)
                    scores_tous_contextes = pd.concat([scores_tous_contextes,score_specifique], axis=1)
                    
                else :
                    print("y'en a pas")
                    score_specifique = pd.Series(['nan' for i in range(len(scores_tous_contextes))]).rename(str(tyrep[1])+'-'+str(cluster[1])+'-'+str(avecqui[1])+'-score')
                    couple_specifique = pd.Series(['nan' for i in range(len(scores_tous_contextes))]).rename(str(tyrep[1])+'-'+str(cluster[1])+'-'+str(avecqui[1])+'-couple')
                    
                    scores_tous_contextes = pd.concat([scores_tous_contextes,couple_specifique], axis=1)
                    scores_tous_contextes = pd.concat([scores_tous_contextes,score_specifique], axis=1)
                    
            else :
                
                print("y'en a pas")
                score_specifique = pd.Series(['nan' for i in range(len(scores_tous_contextes))]).rename(str(tyrep[1])+'-'+str(cluster[1])+'-'+str(avecqui[1])+'-score')
                couple_specifique = pd.Series(['nan' for i in range(len(scores_tous_contextes))]).rename(str(tyrep[1])+'-'+str(cluster[1])+'-'+str(avecqui[1])+'-couple')
                
                scores_tous_contextes = pd.concat([scores_tous_contextes,couple_specifique], axis=1)
                scores_tous_contextes = pd.concat([scores_tous_contextes,score_specifique], axis=1)
                

