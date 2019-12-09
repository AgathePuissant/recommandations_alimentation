# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules


conso_pattern = pd.read_csv("conso_data.csv",encoding = 'latin-1')
conso_pattern.head(3)


def find_frequent(data, type_repas = 0, categorie = 0, seuil_support = 0.05) :
    """
    La fonction qui à partir de la base conso_pattern préparée par R, retourne la base de motif fréquent avec le support
    
    1, data : conso_pattern -- data.frame
    2, type_repas :
        0 on prend tous les repas ; 1 petit-déjeuner ; 2 collation matin
        3 déjeuner ; 4 collation après-midi ; 5 diner ; 6 collation soir -- list
    3, categorie :
        0 : On prend tous les catégories
        Homme : 1 adulte (36-60) ; 2 enfant (0-17) ; 3 jeune adulte (18-35) ; 4 personne âgée (> 60)
        Femme : 5 adulte (36-60) ; 6 enfant (0-17) ; 7 jeune adulte (18-35) ; 8 personne âgée (> 60) -- list
    4, seuil_support : la valeur minimale du support à passer dans la fonction mlxtend.frequent_patterns.apriori -- float

    """
    if type_repas != 0 :
        #data = data[data.tyrep == type_repas]
        data = data[data['tyrep'].isin(type_repas)]
        if categorie != 0 :
            #data = data[data.id_categorie == categorie]
            data = data[data['id_categorie'].isin(categorie)]

    data = data.iloc[:, 3: data.shape[1]-1]
    frequent_itemsets = apriori(data, min_support = seuil_support, use_colnames = True).assign(
            length_item = lambda dataframe: dataframe['itemsets'].map(lambda item: len(item)))
    return frequent_itemsets.sort_values('support', ascending = False)

# Exemple : motif fréquent du petit déjeuner des hommes adultes
d = find_frequent(conso_pattern,[3,5],[1,3,4,5,7,8])


ar = association_rules(d, metric="confidence", min_threshold=0.7)

d.to_csv("C:\\Users\\eloda\\OneDrive\\Documents\\IODAA\\Fil Rouge\\motifs_frq_adultes.csv", index=False,encoding = 'latin-1')
