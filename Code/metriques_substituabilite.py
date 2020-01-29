# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 10:43:17 2020

@author: agaca
"""
from motifs_frequents_substituabilite import *
import seaborn as sns
import matplotlib.pyplot as plt
import time
import numpy as np

conso_pattern_sougr = pd.read_csv("conso_pattern_sougr_transfo.csv",sep = ";", encoding = 'latin-1')
conso_pattern_sougr = conso_pattern_sougr.rename(columns = {'b\x9cuf en pièces ou haché' : 'boeuf en pièces ou haché'})
nomenclature = pd.read_csv("nomenclature.csv",sep = ";",encoding = 'latin-1')
nomenclature['libsougr'] = nomenclature['libsougr'].replace('b\x9cuf en pièces ou haché', 'boeuf en pièces ou haché')

#--------------Code pour faire une heatmap du nombre de couples en fonction de la confiance et du support---
axe_support=np.geomspace(0.01,0.0005,5)
axe_confiance=np.geomspace(0.1,0.005,5)
#
#matrice_nb_couples = np.zeros((len(axe_support),len(axe_confiance)))
#matrice_time = np.zeros((len(axe_support),len(axe_confiance)))
#
#for i in range (len(axe_support)) :
#    for j in range (len(axe_confiance)) :
#        
#        supp=axe_support[i]
#        conf=axe_confiance[j]
#        print("Support : "+str(supp)+" Confiance : "+str(conf))
#        
#        t0=time.time()
#        
#        motifs = find_frequent(conso_pattern_sougr, seuil_support = supp, algo = fpgrowth)
#        print("Motifs fréquents trouvés") 
#        regles = regles_association(motifs,confiance = conf)
#        print("Règles d'association trouvées")
#        regles_filtre = filtrage(regles, 'dejeuner', 'cluster_1', 'famille')
#        
#        if len(regles) > 1 :
#            t_subst = tableau_substitution(regles_filtre, nomenclature)
#            print("Tableau de substitutions fait")
#            scores = matrice_scores_diff_moy(t_subst,regles_filtre)
#            print("Tableau de scores fait")
#            nb_couples=len(scores)
#        else :
#            nb_couples = 0
#        
#        t1=time.time()-t0
#        
#        matrice_nb_couples[i,j]=nb_couples
#        matrice_time[i,j]=t1
#        
#matrice_nb_couples=np.flip(matrice_nb_couples,axis=1)
#matrice_time=np.flip(matrice_time,axis=1)


matrice_nb_couples=np.array([[384,384,384,232,200],[846,828,608,314,168],[1182,1012,800,464,212],[1310,1148,950,604,282],[1432,1270,1094,742,366]])
matrice_time=np.array([[19,14,14,12,104],[44,40,43,40,30],[101,143,129,116,90],[407,357,342,279,229],[1508,1372,1048,940,1454]])

val=[]
for i in range(len(matrice_nb_couples)) :
    for j in range(len(matrice_nb_couples)) :
        print(str(matrice_nb_couples[i,j])+'\n'+str(matrice_time[i,j]))
        val.append('Couples : '+str(matrice_nb_couples[i,j])+'\n (Durée : '+str(np.round(matrice_time[i,j],0))+')')
        
val=np.array(val)
val=np.reshape(val,(5,5))

plt.cla()
plt.clf()
sns.heatmap(matrice_nb_couples,square=True,annot=val,fmt='',xticklabels=np.round(axe_confiance[::-1],4),yticklabels=np.round(axe_support,4))
plt.xlabel("Seuil de confiance")
plt.ylabel("Seuil de support")

matrice_x=np.zeros((len(matrice_nb_couples),len(matrice_nb_couples)))
matrice_y=np.zeros((len(matrice_nb_couples),len(matrice_nb_couples)))

for i in range(0,len(matrice_nb_couples)) :
    for j in range(0,len(matrice_nb_couples)) :
        if i-1>=0 and 4-j-1>=0 :
            matrice_x[i,j]=matrice_nb_couples[i,4-j]-matrice_nb_couples[i-1,4-j]/matrice_time[i,4-j]-matrice_time[i-1,4-j]
            matrice_y[i,j]=matrice_nb_couples[i,4-j]-matrice_nb_couples[i,4-j-1]/matrice_time[i,4-j]-matrice_time[i,4-j-1]
        else :
            matrice_x[i,j]=0
            matrice_y[i,j]=0
            
matrice_grad=np.sqrt(matrice_x**2+matrice_y**2)

plt.cla()
plt.clf()
sns.heatmap(np.round(matrice_grad,3),square=True,annot=True,fmt='',xticklabels=np.round(axe_confiance[::-1],4),yticklabels=np.round(axe_support,4))
plt.xlabel("Seuil de confiance")
plt.ylabel("Seuil de support")

#matrice_ratio=(matrice_nb_couples/np.max(matrice_nb_couples))/(matrice_time/np.max(matrice_time))
#        
#plt.cla()
#plt.clf()
#sns.heatmap(np.round(matrice_ratio,3),square=True,annot=True,fmt='',xticklabels=np.round(axe_confiance[::-1],4),yticklabels=np.round(axe_support,4))
#plt.xlabel("Seuil de confiance")
#plt.ylabel("Seuil de support")


#---------------Code pour test des scores-----------------------------------------------------

#def matrice_scores_diff_med(tableau,regles) :
#    
#    '''Fonction qui à partir du tableau des aliments substituables dans un contexte donné et des règles 
#    d'association, va renvoyer un tableau des scores de substituabilité associés aux couples d'aliments 
#    substituables.
#    Méthode : différence des médianes
#    ---------------
#    Arguments :
#        - tableau : pandas DataFrame contenant les contextes de repas, les aliments substituables 
#        et les métriques associées.
#        -regles : pandas DataFrame contenant les règles d'association et permettant de calculer le score
#        de substituabilité trouvé dans la bibliographie.
#    '''
#
#    t_scores=pd.DataFrame(columns=["Couples","Score confiance","Score biblio"])
#    
#    #On parcoure le tableau des aliments sustituables
#    
#    for i in range(len(tableau)) :
#        
#        print(i)
#        
#        #Si il y'a plusieurs aliments substituables
#        if len(tableau["consequents"][i])>1 :
#            
#            #On compare chaque élément substituable avec les autres
#            for j in range(len(tableau["consequents"][i])) :
#            
#                
#                aliment_1=list(tableau["consequents"][i])[j]
#                
#                for k in range(len(tableau["consequents"][i])) :
#                    
#                    if j!=k :
#                        aliment_2=list(tableau["consequents"][i])[k]
#                        
#                        #Si on a pas déjà mis ce couple dans le tableau des scores, on le met dedans
#                        #Ainsi que les scores associés
#                        
#                        if len(t_scores[t_scores["Couples"]== aliment_1+" vers "+aliment_2])==0:
#                            t_scores.loc[i]=[aliment_1+" vers "+aliment_2,[[tableau["confidence"][i][j]],[tableau["confidence"][i][k]]],score_biblio(frozenset([aliment_1]),frozenset([aliment_2]),regles)]
#                        else :
#                            t_scores.loc[t_scores["Couples"] == aliment_1+" vers "+aliment_2]["Score confiance"].values[0][0].append(tableau["confidence"][i][j])
#                            t_scores.loc[t_scores["Couples"] == aliment_1+" vers "+aliment_2]["Score confiance"].values[0][1].append(tableau["confidence"][i][k])
#    
#    #On construit la moyenne des scores calculé par différence de confiances
#    t_scores["Score confiance"]=t_scores["Score confiance"].apply(lambda x : np.median(x[0])-np.median(x[1]))
#    
#    #On construit le score combiné
#    t_scores["Score combiné"]=t_scores["Score biblio"]+(((t_scores["Score confiance"])/2)+0.5)
#    
#    return t_scores
#

#
#def matrice_scores_med_diff(tableau,regles) :
#    
#    '''Fonction qui à partir du tableau des aliments substituables dans un contexte donné et des règles 
#    d'association, va renvoyer un tableau des scores de substituabilité associés aux couples d'aliments 
#    substituables.
#    Méthode : médiane des différences
#    ---------------
#    Arguments :
#        - tableau : pandas DataFrame contenant les contextes de repas, les aliments substituables 
#        et les métriques associées.
#        -regles : pandas DataFrame contenant les règles d'association et permettant de calculer le score
#        de substituabilité trouvé dans la bibliographie.
#    '''
#
#    t_scores=pd.DataFrame(columns=["Couples","Score confiance","Score biblio"])
#    
#    #On parcoure le tableau des aliments sustituables
#    
#    for i in range(len(tableau)) :
#        
#        print(i)
#        
#        #Si il y'a plusieurs aliments substituables
#        if len(tableau["consequents"][i])>1 :
#            
#            #On compare chaque élément substituable avec les autres
#            for j in range(len(tableau["consequents"][i])) :
#                aliment_1=list(tableau["consequents"][i])[j]
#                
#                for k in range(len(tableau["consequents"][i])) :
#                    if j!=k :
#                        aliment_2=list(tableau["consequents"][i])[k]
#                        
#                        #Si on a pas déjà mis ce couple dans le tableau des scores, on le met dedans
#                        #Ainsi que les scores associés
#                        
#                        if len(t_scores[t_scores["Couples"]== aliment_1+" vers "+aliment_2])==0:
#                            t_scores.loc[i]=[aliment_1+" vers "+aliment_2,[tableau["confidence"][i][j]-tableau["confidence"][i][k]],score_biblio(frozenset([aliment_1]),frozenset([aliment_2]),regles)]
#                        else :
#                            t_scores.loc[t_scores["Couples"] == aliment_1+" vers "+aliment_2]["Score confiance"].values[0].append(tableau["confidence"][i][j]-tableau["confidence"][i][k])
#    
#    #On construit la moyenne des scores calculé par différence de confiances
#    t_scores["Score confiance"]=t_scores["Score confiance"].apply(lambda x : np.median(x))
#    
#    #On construit le score combiné
#    t_scores["Score combiné"]=t_scores["Score biblio"]+(((t_scores["Score confiance"])/2)+0.5)
#    
#    return t_scores

#scores_dmoy = scores
#scores_moyd = scores # (différence de la moyenne = moyenne des différences)
#scores_dmed = scores = matrice_scores_diff_med(t_subst,regles_filtre)
#scores_medd = matrice_scores_med_diff(t_subst,regles_filtre)
#
#scores_conf=pd.DataFrame(columns=['Différence des moyennes','Moyenne des différences','Différence des médianes','Médiane des différences'])
#scores_conf['Différence des moyennes']=scores_dmoy['Score confiance']
#scores_conf['Différence des médianes']=scores_dmed['Score confiance']
#scores_conf['Moyenne des différences']=scores_moyd['Score confiance']
#scores_conf['Médiane des différences']=scores_medd['Score confiance']
#
#import matplotlib.pyplot as plt
#
#plt.figure(figsize=(15,10))
#
#scores_conf.boxplot().set_xticklabels(scores_conf.boxplot().get_xticklabels(),rotation=45)
#
#plt.show()

#----------Code pour test de la distribution des variances---------------------------------------------

#import matplotlib.pyplot as plt
#
#plt.figure(figsize=(15,10))
#
#regles_var_pain=regles[regles['consequents']==frozenset(['riz'])]
#
#plt.hist(regles_var_pain['confidence'].values,bins=150)
