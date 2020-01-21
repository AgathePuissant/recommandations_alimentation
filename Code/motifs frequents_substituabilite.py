# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""
import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import apriori, fpgrowth, fpmax
from mlxtend.frequent_patterns import association_rules

    

def find_frequent(conso_data, type_repas = 0, avec_qui = 0, cluster = 0, seuil_support = 0.05, algo = apriori) :
    """
    La fonction qui à partir de la base conso_pattern préparée par R, retourne la base de motif fréquent avec le support
    
    1, data : conso_pattern -- data.frame
    2, type_repas :
        0 on prend tous les repas ; 1 petit-déjeuner ; 2 collation matin
        3 déjeuner ; 4 collation après-midi ; 5 diner ; 6 collation soir -- list
    3, seuil_support : la valeur minimale du support à passer dans la fonction mlxtend.frequent_patterns.apriori -- float

    """
    
    data=conso_data.copy()
    
    if type_repas != 0 :
        #data = data[data.tyrep == type_repas]
        data = data[data['tyrep'].isin(type_repas)]
        
    if avec_qui != 0 :
        data = data[data['avecqui'].isin(avec_qui)]
        
    if cluster != 0 :
        data = data[data['cluster_consommateur'].isin(cluster)]
        
    del data['tyrep']
    del data['nomen']
    del data['avecqui']
    del data['nojour']
    del data['cluster_consommateur']
            
    frequent_itemsets = algo(data, min_support = seuil_support, use_colnames = True).assign(
        length_item = lambda dataframe: dataframe['itemsets'].map(lambda item: len(item)))
    
    return frequent_itemsets.sort_values('support', ascending = False)



def regles_association(d,confiance=0.5,support_only=False,support=0.1,contexte_maximaux=True) :
    """
    Prend en entrée un dataframe de motifs fréquents et renvoie un dataframe des
    règles d'association à un conséquent et qui supprime les motifs inclus.
    ------------
    Arguments : 
        - d : pandas DataFrame contenant les motifs fréquents
        - confiance : float. le seuil de confiance minimum si support only est False
        - support_only : booléen. on utilise que le support comme métrique
        - support : float. le seuil de support minimum si support only est True
        - contexte maximaux : booléen. Si True, on ne garde que les contextes maximaux.
    """
    
    if support_only == False :
        rules=association_rules(d, metric="confidence", min_threshold=confiance)
    else :
        rules=association_rules(d, support_only=True, min_threshold=0.01)
    
    #On ne garde que les règles à un conséquent et...
    rules = rules[rules['consequents'].str.len() == 1]
    
    # ...on trie le dataframe avec les antécédents les plus long en haut
    # dans le but d'accélérer la recherche de contextes maximaux par la suite
    rules.index = rules['antecedents'].str.len()
    rules = rules.sort_index(ascending=False).reset_index(drop=True)
    
     #Liste qui permet de vérifier qu'on a pas un élément autre qu'alimentaire dans les conséquents
    liste_pas_class=frozenset(['seul','amis','famille','autre','cluster_0','cluster_1','cluster_2','petit-dejeuner','dejeuner','gouter','diner'])
    
    N=len(rules)
            
    #C'est ça qui prend du temps
   
    #Recherche de contextes maximaux
    if contexte_maximaux==True :
             
        #On parcoure le dataframe des règles d'association
        for i in range(N) :
            
            if i%100==0 :
                print(i)
                print(len(rules))
            
            if i in rules.index :
                
                if (rules['consequents'][i].intersection(liste_pas_class)!=frozenset()) :
                    
                    rules=rules[rules['consequents']!=rules['consequents'][i]]
                    print('conséquent erronné')
                            
                else :
                    
                    rules=rules[~((rules['consequents']==rules['consequents'][i]) & (rules['antecedents'].apply(lambda x: x.issubset(rules['antecedents'][i]))) & (rules['consequents'].index!=i))]
#                    (rules.index.get_loc(rules['consequents']==rules['consequents'][i])!=i)
                    print('contexte non maximal')
#                rules=rules.set_index(pd.Index([i for i in range(len(rules))]))
                
    else :
        
        for i in range(N) :

            
            if i in rules.index :
                
                if (rules['consequents'][i].intersection(liste_pas_class)!=frozenset()) :
                    rules=rules[rules['consequents']!=rules['consequents'][i]]
#                    rules=rules.set_index(pd.Index([i for i in range(len(rules))]))
    rules=rules.set_index(pd.Index([i for i in range(len(rules))]))
    return rules

def tableau_substitution(rules_original) :
    """
    Prend en entrée un dataframe des règles d'association et ressort
    le tableau des aliments sustituables en fonction du contexte alimentaire
    """
    
    rules = rules_original.copy()
    rules['consequents_len'] = 1
    
    N=len(rules)
     
    #on parcoure le dataframe des règles d'association
    for i in range(N) :
        
        if i%100==0 :
            print(i)
            print(len(rules))
            
        if i in rules.index :
            
            liste_supp=[]
            
            
            for j in range(len(rules)) :
                
                #Si le contexte alimenaire est le même, soit on unit les éléments conséquents si ils ont le même rôle
                #Soit on ne touche à rien
                if rules["antecedents"][i]==rules["antecedents"][j] and i!=j :
                    
                    if (nomenclature[(nomenclature["libsougr"]==list(rules["consequents"][i])[0])]["code_role"]).all()==(nomenclature[(nomenclature["libsougr"]==list(rules["consequents"][j])[0])]["codrole"]).all() :
                    
                        #On supprime alors la règle d'association qui va être unie
                        liste_supp.append(j)
                    
                        rules["consequents"][i]=rules["consequents"][i].union(rules["consequents"][j])
                        
                        #Mise à jour des confiances sous forme de listes
                        if type(rules["confidence"][i])==list :
                            rules["confidence"][i].append(rules["confidence"][j])
                        else :
                            liste=rules['confidence'].values.tolist()
                            liste[i]=[rules["confidence"][i],rules["confidence"][j]]
                            rules["confidence"]=liste
                        
                        rules['consequents_len'][i]+=1
                
                
            #Mise à jour du dataframe qui va être moins long et accélèrera donc la recherche suivante
            rules.drop(liste_supp, inplace=True)
            
            rules=rules.set_index(pd.Index([i for i in range(len(rules))]))
            
    return rules


def tableau_sub2(rules_ori, nomen_ori) :
    global test1
    rules = rules_ori.copy()
    nomen = nomen_ori.copy()
    nomen = nomen.loc[:,['code_role', 'libsougr']].drop_duplicates()
    rules['consequents2'] = [list(x)[0] for x in rules['consequents'].values]
    test1 = rules
    rules = pd.DataFrame.merge(rules, nomen, left_on = 'consequents2', right_on = 'libsougr', how = 'left')
    
    #rules['union'] = rules.groupby(['antecedents', 'codrole']).count()
    #agg(lambda col : ''.join(col))
    #apply(lambda x: "{%s}" % ', '.join(x))
    
    return rules

test = tableau_sub2(regles, nomenclature)
test = nomenclature.loc[:,['code_role', 'libsougr']].drop_duplicates()

        
def score_biblio(aliment_1,aliment_2,regles_original) :
    '''
    Fonction qui prend en entrée les 2 aliments dont on veut trouver le score de substituabilité et les règles d'associations entre aliments,
    et ressort le score de substituabilité calculé selon le score trouvé dans la bibliographie.
    ---------------
    Arguments :
        -aliment_1 : frozenset de longueur 1
        -aliment_2 : frozenset de longueur 1
        -regles_original : dataFrame contenant les règles d'association entre aliments et contextes alimentaires
    '''
    
    regles=regles_original[(regles_original["consequents"]==aliment_1) | (regles_original["consequents"]==aliment_2)]
    regles=regles.set_index(pd.Index([i for i in range(len(regles))]))
    
    
    x_inter_y=0
    x_union_y=len(regles)
    A_x_y=0
    A_y_x=0
    
    
    
    for i in range(len(regles["antecedents"])) :
        
        
        if regles["consequents"][i]==aliment_1 :
            
            contexte_1=regles["antecedents"][i]
            
            if aliment_2 in contexte_1 :
                A_x_y+=1
            
            for j in range(len(regles["antecedents"])) :
                
                if i!=j and regles["consequents"][j]==aliment_2 :
                    contexte_2=regles["antecedents"][j]
                    
                    if aliment_1 in contexte_2 :
                        A_y_x+=1
                        
                    if contexte_1==contexte_2 :
                        x_inter_y+=1
                    
    return(x_inter_y/(x_union_y+A_x_y+A_y_x))
    
def filtrage(data, tyrep, cluster, avecqui) :
    data_filtre = data.loc[t_subst['antecedents'].astype(str).str.contains(tyrep) &
                               t_subst['antecedents'].astype(str).str.contains(cluster) &
                               t_subst['antecedents'].astype(str).str.contains(avecqui)]
    if tyrep == 'dejeuner' :
        data_filtre = data_filtre.loc[~(data_filtre['antecedents'].astype(str).str.contains('petit-dejeuner'))]
    
    data_filtre=data_filtre.set_index(pd.Index([i for i in range(len(data_filtre))]))
    
    return data_filtre



def matrice_scores_diff_moy(tableau,regles) :
    
    '''Fonction qui à partir du tableau des aliments substituables dans un contexte donné et des règles 
    d'association, va renvoyer un tableau des scores de substituabilité associés aux couples d'aliments 
    substituables.
    Méthode : différence des moyennes
    ---------------
    Arguments :
        - tableau : pandas DataFrame contenant les contextes de repas, les aliments substituables 
        et les métriques associées.
        -regles : pandas DataFrame contenant les règles d'association et permettant de calculer le score
        de substituabilité trouvé dans la bibliographie.
    '''

    t_scores=pd.DataFrame(columns=["Couples","Score confiance","Score biblio"])
    
    #On parcoure le tableau des aliments sustituables
    
    for i in range(len(tableau)) :
        
        print(i)
        
        #Si il y'a plusieurs aliments substituables
        if len(tableau["consequents"][i])>1 :
            
            #On compare chaque élément substituable avec les autres
            for j in range(len(tableau["consequents"][i])) :
            
                
                aliment_1=list(tableau["consequents"][i])[j]
                
                for k in range(len(tableau["consequents"][i])) :
                    
                    if j!=k :
                        aliment_2=list(tableau["consequents"][i])[k]
                        
                        #Si on a pas déjà mis ce couple dans le tableau des scores, on le met dedans
                        #Ainsi que les scores associés
                        
                        if len(t_scores[t_scores["Couples"]== aliment_1+" vers "+aliment_2])==0:
                            t_scores.loc[i]=[aliment_1+" vers "+aliment_2,[[tableau["confidence"][i][j]],[tableau["confidence"][i][k]]],score_biblio(frozenset([aliment_1]),frozenset([aliment_2]),regles)]
                        else :
                            t_scores.loc[t_scores["Couples"] == aliment_1+" vers "+aliment_2]["Score confiance"].values[0][0].append(tableau["confidence"][i][j])
                            t_scores.loc[t_scores["Couples"] == aliment_1+" vers "+aliment_2]["Score confiance"].values[0][1].append(tableau["confidence"][i][k])
    
    #On construit la moyenne des scores calculé par différence de confiances
    t_scores["Score confiance"]=t_scores["Score confiance"].apply(lambda x : np.mean(x[0])-np.mean(x[1]))
    
    #On construit le score combiné
    t_scores["Score combiné"]=t_scores["Score biblio"]+(((t_scores["Score confiance"])/2)+0.5)
    
    return t_scores


def matrice_scores_moy_diff(tableau,regles) :
    
    '''Fonction qui à partir du tableau des aliments substituables dans un contexte donné et des règles 
    d'association, va renvoyer un tableau des scores de substituabilité associés aux couples d'aliments 
    substituables.
    Méthode : moyenne des différences
    ---------------
    Arguments :
        - tableau : pandas DataFrame contenant les contextes de repas, les aliments substituables 
        et les métriques associées.
        -regles : pandas DataFrame contenant les règles d'association et permettant de calculer le score
        de substituabilité trouvé dans la bibliographie.
    '''

    t_scores=pd.DataFrame(columns=["Couples","Score confiance","Score biblio"])
    
    #On parcoure le tableau des aliments sustituables
    
    for i in range(len(tableau)) :
        
        print(i)
        
        #Si il y'a plusieurs aliments substituables
        if len(tableau["consequents"][i])>1 :
            
            #On compare chaque élément substituable avec les autres
            for j in range(len(tableau["consequents"][i])) :
                aliment_1=list(tableau["consequents"][i])[j]
                
                for k in range(len(tableau["consequents"][i])) :
                    if j!=k :
                        aliment_2=list(tableau["consequents"][i])[k]
                        
                        #Si on a pas déjà mis ce couple dans le tableau des scores, on le met dedans
                        #Ainsi que les scores associés
                        
                        if len(t_scores[t_scores["Couples"]== aliment_1+" vers "+aliment_2])==0:
                            t_scores.loc[i]=[aliment_1+" vers "+aliment_2,[tableau["confidence"][i][j]-tableau["confidence"][i][k]],score_biblio(frozenset([aliment_1]),frozenset([aliment_2]),regles)]
                        else :
                            t_scores.loc[t_scores["Couples"] == aliment_1+" vers "+aliment_2]["Score confiance"].values[0].append(tableau["confidence"][i][j]-tableau["confidence"][i][k])
    
    #On construit la moyenne des scores calculé par différence de confiances
    t_scores["Score confiance"]=t_scores["Score confiance"].apply(lambda x : np.mean(x))
    
    #On construit le score combiné
    t_scores["Score combiné"]=t_scores["Score biblio"]+(((t_scores["Score confiance"])/2)+0.5)
    
    return t_scores
            

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
CODE PRINCIPAL
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# La base conso_pattern est préparée par R à partir de la base brute
#conso_pattern_grp = pd.read_csv("conso_pattern_grp.csv", sep = ";", encoding = 'latin-1')
conso_pattern_sougr = pd.read_csv("conso_pattern_sougr_transfo.csv",sep = ";", encoding = 'latin-1')
nomenclature = pd.read_csv("nomenclature.csv",sep = ";",encoding = 'latin-1')
#nomenclature.head(3)

repas=0
avecqui=0
consommateur=0
supp=0.005
conf=0.1

#---------Méthode avec contexte inclus dans la recherche de motifs fréquents---------------

#Modification pour que les modalités de cluster, type de repas et modalités sociale soient mises sous 
#forme booléenne. Transformation à faire uniquement dans le cas où on veut inclure ces modalités dans
#la recheche de motifs fréquents.
  
motifs = find_frequent(conso_pattern_sougr,repas,avecqui,consommateur,seuil_support=supp, algo= fpgrowth)

regles = regles_association(motifs,confiance = conf, contexte_maximaux=False)

regles_filtre = filtrage(regles, 'dejeuner', 'cluster_1', 'famille')

t_subst = tableau_substitution(regles_filtre)
 
scores = matrice_scores_diff_moy(t_subst,regles_filtre)


#--------------Méthode en subdivisant le dataframe de base---------------------------
#
#modalites_avecqui = np.unique(conso_pattern_sougr["avecqui"].dropna())
#modalites_tyrep = np.unique(conso_pattern_sougr["tyrep"].dropna())
#modalites_cluster = np.unique(conso_pattern_sougr["cluster_consommateur"].dropna())
#
#for repas in modalites_tyrep :
#    
#    for avecqui in modalites_avecqui :
#        
#        for cluster in modalites_cluster :
#        
#            motifs = find_frequent(conso_pattern_sougr, repas, avecqui, cluster, [1,3,4,5,7,8], seuil_support=supp, algo='fpgrowth')
#            print("Motifs fréquents trouvés")
#            
#            regles = regles_association(motifs, confiance = conf)
#            print("Règles d'association trouvées")
#            
#            t_subst = tableau_substitution(regles)
#            print("tableau de substitutions fait")
#            
#            scores = matrice_scores(t_subst,regles)
#            print("tableau de scores fait")
#                
#            pickle.dump(scores,open("scores_"+str(repas)+"_"+str(avecqui)+"_supp=0,5_conf=0,5","wb"))
#            print("scores_"+str(repas)+"_"+str(avecqui)+"_"+str(cluster)+"_supp=0,5_conf=0,5")
#                



