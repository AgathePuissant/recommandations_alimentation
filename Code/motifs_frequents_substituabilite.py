# -*- coding: utf-8 -*-
"""
Created on Mon Jan 6 10:25:19 2020

@author: ADMIN
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
            
    frequent_itemsets = algo(conso_data.drop(['tyrep', 'nomen', 'avecqui', 'nojour', 'cluster_consommateur', 'autre'], axis = 1),
                             min_support = seuil_support, use_colnames = True)
    
    return frequent_itemsets


def regles_association(d, confiance=0.5, support_only=False, support=0.1) :
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
        rules = association_rules(d, support_only = True, min_threshold = support)
    # ...sinon c'est la confiance
    else :
        rules = association_rules(d, metric = "confidence", min_threshold = confiance)
    
    #Liste qui permet de vérifier qu'on a pas un élément autre qu'alimentaire dans les conséquents

    liste_contexte = ['seul','accompagne',
                      'cluster_1','cluster_2','cluster_3','cluster_4','cluster_5','cluster_6','cluster_7','cluster_8',
                      'petit-dejeuner','dejeuner','gouter','diner']
    
    #On ne garde que les règles à un conséquent et...
    rules = rules[rules['consequents'].str.len() == 1]
    rules['consequents'] = rules['consequents'].apply(lambda con : list(con)[0])
    # ...appartient pas dans la liste des contextes
    rules =  rules[~rules['consequents'].isin(liste_contexte)].reset_index(drop = True)
    
    rules['consequents'] = rules['consequents'].apply(lambda con : tuple([con]))
    rules['antecedents'] = rules['antecedents'].apply(lambda ant : tuple(sorted(list(ant))))
    
    return rules


def filtrage(data, tyrep, cluster, avecqui) :
    
    data_filtre = data.loc[(data['antecedents'].astype(str).str.contains(tyrep) &
                               data['antecedents'].astype(str).str.contains(cluster) &
                               data['antecedents'].astype(str).str.contains(avecqui))]
                               
    if tyrep == 'dejeuner' :
        data_filtre = data_filtre.loc[~(data_filtre['antecedents'].astype(str).str.contains('petit-dejeuner'))]
    
    data_filtre=data_filtre.set_index(pd.Index([i for i in range(len(data_filtre))]))
    
    return data_filtre

#def tableau_substitution(rules_ori, nomen_ori) :
#    
#    # data manipulation
#    rules = rules_ori.copy()
#    rules = rules.loc[:, ['antecedents', 'consequents', 'confidence']]
#    
#    nomen = nomen_ori.copy()
#    nomen = nomen.loc[:,['code_role', 'libsougr']].drop_duplicates()
#    
#    #rules['libsougr'] = [x[0] for x in rules['consequents'].values]
#    rules['libsougr'] = [x[0] for x in rules['consequents']]
#    rules = pd.DataFrame.merge(rules, nomen, on = 'libsougr', how = 'left')
#    
#    # data sort by values of confidence by group of antecedents
#    rules = rules.groupby(['antecedents', 'code_role'])
#    rules = rules.apply(lambda df : df.sort_values('confidence')).reset_index(drop = True)
#    
#    # add two columns of union of sous-groupe and confidence by group of antecedents
#    rules = pd.DataFrame.merge(rules.drop('libsougr', axis=1), rules.groupby(['antecedents', 'code_role'])['libsougr'].apply(tuple).reset_index())
#    rules = pd.DataFrame.merge(rules.drop('confidence', axis=1),rules.groupby(['antecedents', 'code_role'])['confidence'].apply(tuple).reset_index())
#    
#    # remove duplicate rows (transform to tuple...
#    rules['consequents'] = rules['libsougr'].apply(lambda con : tuple(con))
#    rules = rules.drop('libsougr', axis = 1)
#    
#    #... and drop duplicates)
#    rules = rules.drop_duplicates(['antecedents', 'consequents'])
#    #.reset_index(drop = True)
#    
#    return rules
#
#def score_biblio(aliment_1, aliment_2, rules_ori) :
#    '''
#    Fonction qui prend en entrée les 2 aliments dont on veut trouver le score de substituabilité et les règles d'associations entre aliments,
#    et ressort le score de substituabilité calculé selon le score trouvé dans la bibliographie.
#    ---------------
#    Arguments :
#        -aliment_1 : frozenset de longueur 1
#        -aliment_2 : frozenset de longueur 1
#        -regles_original : dataFrame contenant les règles d'association entre aliments et contextes alimentaires
#    '''
#    rules = rules_ori[[aliment_1 in x or aliment_2 in x for x in rules_ori['consequents']]]
#    
#    # inter : Les contextes dans lesquels aliment_1 ET aliment_2 sont substituables
#    inter = (rules.groupby('antecedents').size().values == 2).sum()
#
#    # union : Les contextes dans lesquels aliment_1 OU aliment_2 sont substituables
#    union = len(rules)
#    
#    # Somme A = A_alim1_alim2 + A_alim2_alim1
#    # A_alim1_alim2 : Nombre de contextes dans lesquels aliment_1 est substituable (trouvé dans la colonne 'conséquents') et aliment_ 2 apparait (trouvé dans la colonne 'antecedents')
#    # A_alim1_alim2 : Nombre de contextes dans lesquels aliment_1 est substituable (trouvé dans la colonne 'conséquents') et aliment_ 2 apparait (trouvé dans la colonne 'antecedents')
#    A = rules[[aliment_1 in x or aliment_2 in x for x in rules['antecedents']]]['antecedents'].nunique()
#    
#    return inter / (union + A)
#
#def matrice_scores_diff_moy(tab_subst_ori, tab_reg) :
#    '''Fonction qui à partir du tableau des aliments substituables dans un contexte donné et des règles 
#    d'association, va renvoyer un tableau des scores de substituabilité associés aux couples d'aliments 
#    substituables.
#    Méthode : différence des moyennes
#    ---------------
#    Arguments :
#        - tableau : pandas DataFrame contenant les contextes de repas, les aliments substituables 
#        et les métriques associées.
#        -regles : pandas DataFrame contenant les règles d'association et permettant de calculer le score
#        de substituabilité trouvé dans la bibliographie.
#    '''
#    
#    # Nombre d'éléments dans "conséquents" >  1
#    tab_subst = tab_subst_ori.copy()
#    tab_subst['pair_index'] = tab_subst['consequents'].str.len()
#    tab_subst = tab_subst[tab_subst['pair_index'] > 1]
#    
#    # La liste des paires d'indices (tuple) d'aliments substituables
#    tab_subst['pair_index'] = tab_subst['pair_index'].transform(lambda x : [ind for ind in itertools.permutations(range(x), 2)])
#    
#    # Déplacer chacune des paires d'indices en une ligne séparément 
#    lst_col = 'pair_index'
#    tab_subst = pd.DataFrame({
#          col:np.repeat(tab_subst[col].values, tab_subst[lst_col].str.len())
#          for col in tab_subst.columns.drop(lst_col)}
#        ).assign(**{lst_col:pd.DataFrame(np.concatenate(tab_subst[lst_col].values)).values.tolist()})
#
#    # Transforer les colonnes 'conséquents' et 'confidence' en extrayant les éléments qui correspondent à des paires d'indices 
#    tab_subst['consequents'] = tab_subst.apply(lambda df : (df.consequents[df.pair_index[0]], df.consequents[df.pair_index[1]]), axis = 1)
#    tab_subst['confidence'] = tab_subst.apply(lambda df : np.array((df.confidence[df.pair_index[0]], df.confidence[df.pair_index[1]])), axis = 1)
#    
#    # Calcul du score de confiance comme la différence de la moyenne de la confiance de deux aliments substituables
#    tab_subst = tab_subst.groupby('consequents')['confidence'].apply(np.mean).reset_index()
#    tab_subst['Score confiance'] = tab_subst.confidence.apply(lambda conf : conf[0] - conf[1])
#
#    # Calcul du score de bibliothèque grace à la fonction score_biblio
#    tab_subst['Score biblio'] = tab_subst['consequents'].apply(lambda cons : score_biblio(cons[0], cons[1], tab_reg))
#    
#    # Calcul du score combiné
#    tab_subst["Score combiné"] = tab_subst["Score biblio"]+(((tab_subst["Score confiance"])/2)+0.5)
#    
#    return tab_subst


def creation_couples(rules_ori, nomen_ori) :
    
    # data manipulation
    couples = rules_ori.copy()
    
    nomen = nomen_ori.copy()
    nomen = nomen.loc[:,['code_role', 'libsougr']].drop_duplicates()
    
    #rules['libsougr'] = [x[0] for x in rules['consequents'].values]
    couples['libsougr'] = [x[0] for x in couples['consequents']]
    couples = pd.DataFrame.merge(couples, nomen, on = 'libsougr', how = 'left').drop(
            'consequents', axis = 1).rename(
                    columns = {'libsougr' : 'couples_alim'})
    
    couples = pd.DataFrame.merge(couples.drop('couples_alim', axis=1), couples.groupby(['code_role'])['couples_alim'].unique().apply(tuple).reset_index())
    couples = couples[couples['couples_alim'].str.len() > 1]
    couples = couples.loc[:, ['code_role', 'couples_alim']].drop_duplicates()
    
    # La liste des paires d'indices (tuple) d'aliments substituables
    couples['pair_index'] = couples['couples_alim'].str.len().transform(
            lambda x : [ind for ind in itertools.permutations(range(x), 2)])
    
    # Déplacer chacune des paires d'indices en une ligne séparément 
    lst_col = 'pair_index'
    couples = pd.DataFrame({
          col:np.repeat(couples[col].values, couples[lst_col].str.len())
          for col in couples.columns.drop(lst_col)}
        ).assign(**{lst_col:pd.DataFrame(np.concatenate(couples[lst_col].values)).values.tolist()})
    
    couples['couples_alim'] = couples.apply(lambda df : (df.couples_alim[df.pair_index[0]], df.couples_alim[df.pair_index[1]]), axis = 1)
    
    return couples
 
    

def calcul_score(aliment_1, aliment_2, rules_ori) :
    '''
    Fonction qui prend en entrée les 2 aliments dont on veut trouver le score de substituabilité et les règles d'associations entre aliments,
    et ressort le score de substituabilité calculé selon le score trouvé dans la bibliographie.
    ---------------
    Arguments :
        -aliment_1 : string aliment 1
        -aliment_2 : string aliment 2
        -regles_original : dataFrame contenant les règles d'association entre aliments et contextes alimentaires
    '''
    global rules, inter_df, res_df
    # Préparation de la table pour calculer le score de substitution :
    # Les repas dont le conséquent contient soit aliment_1 soit aliment_2...
    rules = rules_ori[[aliment_1 in x or aliment_2 in x for x in rules_ori['consequents']]].reset_index(drop = True)
    
    # ...puis enlever les éléments de contexte dans le tuple d'antécédents
    liste_contexte = ['seul','accompagne',
                      'cluster_1','cluster_2','cluster_3','cluster_4','cluster_5','cluster_6','cluster_7','cluster_8',
                      'petit-dejeuner','dejeuner','gouter','diner']
    
    rules['antecedents'] = rules['antecedents'].apply(
            lambda ant : [val for val in ant if val not in liste_contexte]).apply(
                    tuple)
    
    
     #rules = rules[rules['antecedents'].str.len() > 0].reset_index(drop = True)

    # union : Les contextes dans les quels aliment_1 OU aliment_2 sont substituables
    union = len(rules)
    
    if union == 0 :
        return 0
    
    else :
        # penalite : Somme des confiances des repas dans lesquels l'un est substituable et l'autre apparait.
        penalite = rules.loc[[aliment_1 in x or aliment_2 in x for x in rules['antecedents']]]['confidence'].sum()
        
        # Score de substitution pour les repas exactement en commun
        inter_df = rules.groupby('antecedents').filter(lambda x : len(x) == 2)
        
        inter = len(inter_df)
        if inter > 0 :
            inter_df = inter_df.groupby('consequents')['confidence'].apply(np.mean)
            print(inter_df)
            inter = inter * inter_df[aliment_2, ] / inter_df.sum()
            
        
        # Score de substitution pour les repas ressemblants
        res_df = rules.groupby('antecedents').filter(lambda x : len(x) != 2)
        
        res = len(res_df)
        if res > 0 :
            res_df = res_df.groupby('consequents')['confidence'].apply(np.mean).reset_index()
    
            if len(res_df) == 1 :
                res_df = pd.DataFrame.merge(res_df,
                                          pd.DataFrame(data = {'consequents' : [tuple([aliment_1]), tuple([aliment_2])]}), 
                                          how = 'outer').fillna(0)
                
            res = res*res_df[res_df['consequents'] == tuple([aliment_2])]['confidence'].sum() / res_df['confidence'].sum()
    
    return (inter + res) / (union + penalite)



def score_substitution(couples_ori, regles_ori) :
    
    tab_scores = couples_ori.copy()
    
    tab_scores['score'] = tab_scores['couples_alim'].apply(lambda couples : calcul_score(couples[0], couples[1], regles_ori))
    
    tab_scores = tab_scores.loc[:, ['couples_alim', 'score']]
    return tab_scores



#conso_pattern_sougr = pd.read_csv("conso_pattern_sougr_transfo.csv",sep = ";", encoding = 'latin-1')
#nomenclature = pd.read_csv("nomenclature.csv",sep = ";",encoding = 'latin-1')
#motifs = find_frequent(conso_pattern_sougr, seuil_support = 0.001, algo = fpgrowth)
#regles = regles_association(motifs, confiance = 0.001, support_only = False, support = 0.001)
#regles_filtre = filtrage(regles, 'petit-dejeuner', 'cluster_1', 'seul')
#couples = creation_couples(regles_filtre,nomenclature)
#scores = score_substitution(couples,regles_filtre)

#t_subst = tableau_substitution(regles_filtre, nomenclature)
#score_contexte = matrice_scores_diff_moy(t_subst, regles_filtre)


