# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

#Modification de la table : valeurs qui informent si l'aliment a été mangé ou non
import pandas as pd
from mlxtend.frequent_patterns import apriori

# La base conso_pattern est préparée par R à partir de la base brute
conso_pattern_grp = pd.read_csv("conso_pattern_grp.csv", sep = ";", encoding = 'latin-1')
conso_pattern_sougr = pd.read_csv("conso_pattern_sougr.csv", sep = ";", encoding = 'latin-1')

def find_frequent(data, type_repas, categorie, seuil_support) :
    """
    La fonction qui à partir de la base conso_pattern préparée par R, retourne la base de motif fréquent avec le support
    
    1, data : conso_pattern_grp pour l'analyse par groupe d'aliment
              conso_pattern_sougr pour l'analyse par sous-groupe d'aliment -- data.frame
    2, type_repas :
        0 on prend tous les repas ; 1 petit-déjeuner ; 2 collation matin
        3 déjeuner ; 4 collation après-midi ; 5 diner ; 6 collation soir -- int
    3, categorie :
        0 : On prend tous les catégories
        Homme : 1 adulte (36-60) ; 2 enfant (0-17) ; 3 jeune adulte (18-35) ; 4 personne âgée (> 60)
        Femme : 5 adulte (36-60) ; 6 enfant (0-17) ; 7 jeune adulte (18-35) ; 8 personne âgée (> 60) -- int
    4, seuil_support : la valeur minimale du support à passer dans la fonction mlxtend.frequent_patterns.apriori -- float
    """
    if type_repas != 0 :
        data = data[data.tyrep == type_repas]
        if categorie != 0 :
            data = data[data.id_categorie == categorie]
    data = data.iloc[:, 3: data.shape[1]-2]
    frequent_itemsets = apriori(data, min_support = seuil_support, use_colnames = True).assign(
            length_item = lambda dataframe: dataframe['itemsets'].map(lambda item: len(item)))
    return frequent_itemsets.sort_values('support', ascending = False)

# Exemple : motif fréquent du petit déjeuner des hommes adultes
d = find_frequent(conso_pattern_sougr, 1, 2, 0.05)
d = find_frequent(conso_pattern_grp, 1, 2, 0.05)
