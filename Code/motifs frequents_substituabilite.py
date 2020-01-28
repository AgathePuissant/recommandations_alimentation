# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""
import numpy as np
import pandas as pd
import itertools
from mlxtend.frequent_patterns import apriori, fpgrowth, fpmax
from mlxtend.frequent_patterns import association_rules

    

def find_frequent(conso_data, seuil_support = 0.05, algo = apriori) :
    """
    La fonction qui à partir de la base conso_pattern préparée par R, retourne la base de motif fréquent avec le support
    
    1, data : conso_pattern -- data.frame
    2, type_repas :
        0 on prend tous les repas ; 1 petit-déjeuner ; 2 collation matin
        3 déjeuner ; 4 collation après-midi ; 5 diner ; 6 collation soir -- list
    3, seuil_support : la valeur minimale du support à passer dans la fonction mlxtend.frequent_patterns.apriori -- float
    """
            
    frequent_itemsets = algo(conso_data.drop(['tyrep', 'nomen', 'avecqui', 'nojour', 'cluster_consommateur'], axis = 1),
                             min_support = seuil_support, use_colnames = True)
    
    return frequent_itemsets


def regles_association(d, confiance=0.5, support_only=False, support=0.1, contexte_maximaux=True) :
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
    
    #Si on a décidé support only, le support uniquement éest utilisé comme métrique pour trouvers les règles sinon c'est la confiance
    if support_only == False :
        rules=association_rules(d, metric="confidence", min_threshold = confiance)
    else :
        rules=association_rules(d, support_only = True, min_threshold = 0.01)
    
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
                
                #si le conséquent est pas un aliment, on filtre les valeurs du tableau qui ont des conséquents similaires
                if (rules['consequents'][i].intersection(liste_pas_class)!=frozenset()) :
                    
                    rules=rules[rules['consequents']!=rules['consequents'][i]]
                    print('conséquent erronné')
                            
                else :
                    #si le conséquent est un aliment, on filtre les règles qui ont le même conséquent et un antécédent inclus dans l'antécédent original
                    rules=rules[~((rules['consequents']==rules['consequents'][i]) & (rules['antecedents'].apply(lambda x: x.issubset(rules['antecedents'][i]))) & (rules['consequents'].index!=i))]
#                    (rules.index.get_loc(rules['consequents']==rules['consequents'][i])!=i)
                    print('contexte non maximal')
#                rules=rules.set_index(pd.Index([i for i in range(len(rules))]))
                
    else : # Si on ne filtre pas les contextes maximaux, on filtre juste les conséquents qui ne sont pas des aliments
        # Parcours de la base
        for i in range(N) :
            # La condition est nécessaire car c'est possible que les index soient modifiés au cours du lancement
            if i in rules.index :
                # On enlève les conséquents dans lesquels il existe les éléments de contexte
                if (rules['consequents'][i].intersection(liste_pas_class)!=frozenset()) :
                    rules=rules[rules['consequents']!=rules['consequents'][i]]
#                    rules=rules.set_index(pd.Index([i for i in range(len(rules))]))
    rules=rules.set_index(pd.Index([i for i in range(len(rules))]))
    return rules

def regles_association2(d, confiance=0.5, support_only=False, support=0.1, contexte_maximaux=True) :
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
    global test_rules
    
    #Si on a décidé support only, le support uniquement éest utilisé comme métrique pour trouvers les règles...
    if support_only :
        rules = association_rules(d, support_only = True, min_threshold=0.01)
    # ...sinon c'est la confiance
    else :
        rules = association_rules(d, metric = "confidence", min_threshold=confiance)
    
    #Liste qui permet de vérifier qu'on a pas un élément autre qu'alimentaire dans les conséquents
    liste_contexte = ['seul','amis','famille','autre','cluster_0','cluster_1','cluster_2','petit-dejeuner','dejeuner','gouter','diner']
    
    #On ne garde que les règles à un conséquent et...
    rules = rules[rules['consequents'].str.len() == 1]
    rules['consequents'] = rules['consequents'].apply(lambda con : list(con)[0])
    # ...appartient pas dans la liste des contextes
    rules =  rules[~rules['consequents'].isin(liste_contexte)].reset_index(drop = True)

    # on enlève les règles qui ont le même conséquent et un antécédent inclus dans l'antécédent original
    # à tester si c'est plus rapide si c'est fait directement sur les frozensets puis convertir à tuples ou si c'est en inverse
    if contexte_maximaux :

        # add a new column test si [ante inclus dans (groupby(ante) unique)]
        #...
        # drop True
        #...
        
        pass

    return rules


#test = regles_association2(motifs,confiance = conf, contexte_maximaux=False)
#regles = regles_association(motifs,confiance = conf, contexte_maximaux=False)
#regles['consequents'] = regles['consequents'].apply(lambda con : list(con)[0])

# =============================================================================
# import timeit
# liste_par_class =frozenset(['seul','amis','famille','autre','cluster_0','cluster_1','cluster_2','petit-dejeuner','dejeuner','gouter','diner'])
# liste = ['seul','amis','famille','autre','cluster_0','cluster_1','cluster_2','petit-dejeuner','dejeuner','gouter','diner']
# def datafilter1(data) :
#     data = data.copy()
#     data['consequents'] = data['consequents'].apply(lambda con : list(con)[0])
#     data =  data[data['consequents'].isin(liste)]
#     return data 
# 
# def datafilter2(data) :
#     data = data.copy()
#     data['inter'] = data['consequents'].apply(lambda con : con & liste_par_class)
#     data = data[data['inter'].str.len() > 0]
#     return data
# 
# def myfunction() :
#     datafilter1(test)
# 
# def myfunction2() :
#     datafilter2(test)
# 
# print('test1 : ', timeit.timeit(myfunction, number = 100)) #6.075
# print('test2 : ', timeit.timeit(myfunction2, number = 100)) #10.113
# =============================================================================

def tableau_substitution(rules_ori, nomen_ori) :
    
    # data manipulation
    rules = rules_ori.copy()
    rules = rules.loc[:, ['antecedents', 'consequents', 'confidence']]
    
    nomen = nomen_ori.copy()
    nomen = nomen.loc[:,['code_role', 'libsougr']].drop_duplicates()
    
    rules['libsougr'] = [list(x)[0] for x in rules['consequents'].values]
    rules = pd.DataFrame.merge(rules, nomen, on = 'libsougr', how = 'left')
    
    # data sort by values of confidence by group of antecedents
    rules = rules.groupby(['antecedents', 'code_role'])
    rules = rules.apply(lambda df : df.sort_values('confidence')).reset_index(drop = True)
    
    # add two columns of union of sous-groupe and confidence by group of antecedents
    rules = pd.DataFrame.merge(rules.drop('libsougr', axis=1), rules.groupby(['antecedents', 'code_role'])['libsougr'].unique().reset_index())
    rules = pd.DataFrame.merge(rules.drop('confidence', axis=1),rules.groupby(['antecedents', 'code_role'])['confidence'].unique().reset_index())
    
    # remove duplicate rows (transform to tuple...
    rules['consequents'] = rules['libsougr'].apply(lambda con : tuple(con))
    rules['antecedents'] = rules['antecedents'].apply(lambda ant : tuple(sorted(list(ant))))
    rules['confidence'] = rules['confidence'].apply(lambda conf : tuple(conf))
    rules = rules.drop('libsougr', axis = 1)
    
    #... and drop duplicates)
    # tuple / list is better for the rest (frozenset doesn't keep the order) 
    rules = rules.drop_duplicates(['antecedents', 'consequents']).reset_index(drop = True)
    
    return rules
     

def filtrage(data, tyrep, cluster, avecqui) :
    data_filtre = data.loc[data['antecedents'].astype(str).str.contains(tyrep) &
                               data['antecedents'].astype(str).str.contains(cluster) &
                               data['antecedents'].astype(str).str.contains(avecqui)]
    if tyrep == 'dejeuner' :
        data_filtre = data_filtre.loc[~(data_filtre['antecedents'].astype(str).str.contains('petit-dejeuner'))]
    
    data_filtre=data_filtre.set_index(pd.Index([i for i in range(len(data_filtre))]))
    
    return data_filtre


def score_biblio(aliment_1, aliment_2, rules_ori) :
    '''
    Fonction qui prend en entrée les 2 aliments dont on veut trouver le score de substituabilité et les règles d'associations entre aliments,
    et ressort le score de substituabilité calculé selon le score trouvé dans la bibliographie.
    ---------------
    Arguments :
        -aliment_1 : frozenset de longueur 1
        -aliment_2 : frozenset de longueur 1
        -regles_original : dataFrame contenant les règles d'association entre aliments et contextes alimentaires
    '''
    
    rules = rules_ori[(rules_ori["consequents"]==aliment_1) | (rules_ori["consequents"]==aliment_2)].reset_index(drop = True)
    
    # inter : Les contextes dans lesquels aliment_1 ET aliment_2 sont substituables
    inter = (rules.groupby('antecedents').size().values == 2).sum()

    # Somme A = A_alim1_alim2 + A_alim2_alim1
    # A_alim1_alim2 : Nombre de contextes dans lesquels aliment_1 est substituable (trouvé dans la colonne 'conséquents') et aliment_ 2 apparait (trouvé dans la colonne 'antecedents')
    # A_alim1_alim2 : Nombre de contextes dans lesquels aliment_1 est substituable (trouvé dans la colonne 'conséquents') et aliment_ 2 apparait (trouvé dans la colonne 'antecedents')
    A = rules[rules['antecedents'].astype(str).str.contains(list(aliment_1)[0]) | rules['antecedents'].astype(str).str.contains(list(aliment_2)[0])]['antecedents'].nunique()
    
    # union : Les contextes dans lesquels aliment_1 OU aliment_2 sont substituables
    union = len(rules)
    
    return inter / (union + A)

def matrice_scores_diff_moy(tab_subst_ori, tab_reg) :
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
    
    # Nombre d'éléments dans "conséquents" >  1
    tab_subst = tab_subst_ori.copy()
    tab_subst = tab_subst[tab_subst['consequents'].str.len() > 1]
    
    # La liste des paires d'indices (tuple) d'aliments substituables
    tab_subst['pair_index'] = tab_subst['consequents'].str.len()
    tab_subst['pair_index'] = tab_subst['pair_index'].transform(lambda x : [ind for ind in itertools.permutations(range(x), 2)])
    
    # Déplacer chacune des paires d'indices en une ligne séparément 
    lst_col = 'pair_index'
    tab_subst = pd.DataFrame({
          col:np.repeat(tab_subst[col].values, tab_subst[lst_col].str.len())
          for col in tab_subst.columns.drop(lst_col)}
        ).assign(**{lst_col:pd.DataFrame(np.concatenate(tab_subst[lst_col].values)).values.tolist()})

    # Transforer les colonnes 'conséquents' et 'confidence' en extrayant les éléments qui correspondent à des paires d'indices 
    tab_subst['consequents'] = tab_subst.apply(lambda df : (df.consequents[df.pair_index[0]], df.consequents[df.pair_index[1]]), axis = 1)
    tab_subst['confidence'] = tab_subst.apply(lambda df : np.array((df.confidence[df.pair_index[0]], df.confidence[df.pair_index[1]])), axis = 1)
    
    # Calcul du score de confiance comme la différence de la moyenne de la confiance de deux aliments substituables
    tab_subst = tab_subst.groupby('consequents')['confidence'].apply(np.mean).reset_index()
    tab_subst['Score confiance'] = tab_subst.confidence.apply(lambda conf : conf[0] - conf[1])
    
    # Calcul du score de bibliothèque grace à la fonction score_biblio
    tab_subst['Score biblio'] = tab_subst['consequents'].apply(lambda cons : score_biblio(frozenset([cons[0]]), frozenset([cons[1]]), tab_reg))
    
    # Calcul du score combiné
    tab_subst["Score combiné"] = tab_subst["Score biblio"]+(((tab_subst["Score confiance"])/2)+0.5)
    
    return tab_subst


            

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
CODE PRINCIPAL
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# La base conso_pattern est préparée par R à partir de la base brute
conso_pattern_sougr = pd.read_csv("conso_pattern_sougr_transfo.csv",sep = ";", encoding = 'latin-1')
nomenclature = pd.read_csv("nomenclature.csv",sep = ";",encoding = 'latin-1')

supp=0.002
conf=0.01

#---------Méthode avec contexte inclus dans la recherche de motifs fréquents---------------

#Modification pour que les modalités de cluster, type de repas et modalités sociale soient mises sous 
#forme booléenne. Transformation à faire uniquement dans le cas où on veut inclure ces modalités dans
#la recheche de motifs fréquents.
  
motifs = find_frequent(conso_pattern_sougr, seuil_support = supp, algo = fpgrowth)
print("Motifs fréquents trouvés") 
regles = regles_association(motifs,confiance = conf, contexte_maximaux=False)
print("Règles d'association trouvées")
regles_filtre = filtrage(regles, 'dejeuner', 'cluster_1', 'famille')
print("Règles d'association filtrées")
t_subst = tableau_substitution(regles_filtre, nomenclature)
print("Tableau de substitutions fait")
scores = matrice_scores_diff_moy(t_subst,regles_filtre)
print("Tableau de scores fait")

#---------------Code pour test des scores-------------------

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

#----------Code pour test de la distribution des variances--------------------

#import matplotlib.pyplot as plt
#
#plt.figure(figsize=(15,10))
#
#regles_var_pain=regles[regles['consequents']==frozenset(['riz'])]
#
#plt.hist(regles_var_pain['confidence'].values,bins=150)
