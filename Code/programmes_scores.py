# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

from motifs_frequents_substituabilite import *

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
CODE PRINCIPAL
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
conso_pattern_sougr = pd.read_csv("conso_pattern_sougr_transfo.csv",sep = ";", encoding = 'latin-1')
nomenclature = pd.read_csv("nomenclature.csv",sep = ";",encoding = 'latin-1')

conso_pattern_sougr['accompagne']=conso_pattern_sougr['famille'] & conso_pattern_sougr['amis']
del conso_pattern_sougr['autre'], conso_pattern_sougr['famille'], conso_pattern_sougr['amis']

supp = 0.001
conf = 0.001

cluster_liste = [[1,'cluster_1'],[2,'cluster_2'],[3,'cluster_3'],[4,'cluster_4'],[5,'cluster_5'],[6,'cluster_6'],[7,'cluster_7'],[8,'cluster_8'],[9,'cluster_9'],[10,'cluster_10']]

avecqui_liste = [[1,'seul'],[2,'accompagne']]

tyrep_liste = [[1,'petit-dejeuner'],[3,'dejeuner'],[4,'gouter'],[5,'diner']]

#---------Méthode avec contexte inclus dans la recherche de motifs fréquents---------------

#Modification pour que les modalités de cluster, type de repas et modalités sociale soient mises sous 
#forme booléenne. Transformation à faire uniquement dans le cas où on veut inclure ces modalités dans
#la recheche de motifs fréquents.
#
#motifs = find_frequent(conso_pattern_sougr, seuil_support = supp, algo = fpgrowth)
#print("Motifs fréquents trouvés") 
#regles = regles_association(motifs,confiance = conf)
#print("Règles d'association trouvées")

#print(len(regles))

scores_tous_contextes = pd.DataFrame([],columns = ['cluster','repas','compagnie','malus','aliment_1','aliment_2','score'])


for tyrep in tyrep_liste :
    
    for cluster in cluster_liste :
        
        for avecqui in avecqui_liste :
            
            print(tyrep)
            print(cluster)
            print(avecqui)
            
            conso_pattern_sougr_subset = conso_pattern_sougr[(conso_pattern_sougr[tyrep[1]]==1) & (conso_pattern_sougr[cluster[1]]==1) & (conso_pattern_sougr[avecqui[1]]==1)]
            
            if len(conso_pattern_sougr_subset)==0:
                print("y'en a pas")
            else :
                supp = 50/len(conso_pattern_sougr_subset)
                conf = supp
            
            
            
                motifs = find_frequent(conso_pattern_sougr_subset, seuil_support = supp, algo = fpgrowth)
                print("Motifs fréquents trouvés") 
                regles = regles_association(motifs,confiance = conf)
                print("Règles d'association trouvées")
    #            regles_filtre = filtrage(regles, tyrep[1], cluster[1], avecqui[1])
                
    #            print("Taille des règles filtrées : "+str(len(regles_filtre)))
                
                if len(regles)>0 :
                    
                
                    t_subst = tableau_substitution(regles, nomenclature)
                    
                    print("Tableau de substitutions fait")
                    print("Taille du tableau de substitution : "+str(len(t_subst)))
                    
                    if (t_subst.drop_duplicates(['consequents'])['code_role'].value_counts()>2).any():
                        
                        scores = matrice_scores_diff_moy(t_subst, regles)
                        print("Tableau de scores fait")
                        print("Taille des scores : "+str(len(scores)))
                        
                        al1 = scores['consequents'].apply(lambda x: x[0]).rename('aliment_1')
                        al2 = scores['consequents'].apply(lambda x: x[1]).rename('aliment_2')
                        
                        sco = scores['Score combiné'].rename('score')
                        
                        data = np.array([[cluster[1]]*len(sco),[tyrep[1]]*len(sco),[avecqui[1]]*len(sco),[False]*len(sco),al1.tolist(),al2.tolist(),sco.tolist()])
                        
                        data = data.transpose()               
                        suite = pd.DataFrame(data,columns=['cluster','repas','compagnie','malus','aliment_1','aliment_2','score'])                    
                        
                        scores_tous_contextes = pd.concat([scores_tous_contextes,suite])
    
                        
                    else :
                        print("y'en a pas")
                else :
                    
                    print("y'en a pas")
