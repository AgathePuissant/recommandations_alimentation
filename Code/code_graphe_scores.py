# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 15:25:39 2020

@author: agaca
"""

import motifs_frequents_substituabilite as mf
import pandas as pd
import itertools
from mlxtend.frequent_patterns import apriori, fpgrowth, fpmax
from mlxtend.frequent_patterns import association_rules
import numpy as np

conso_pattern_sougr = pd.read_csv("conso_pattern_sougr_transfo.csv",sep = ";", encoding = 'latin-1')
nomenclature = pd.read_csv("nomenclature.csv",sep = ";",encoding = 'latin-1')
motifs = mf.find_frequent(conso_pattern_sougr, seuil_support = 0.001, algo = fpgrowth)
regles = mf.regles_association(motifs, confiance = 0.001, support_only = False, support = 0.001)
regles_filtre = mf.filtrage(regles, 'petit-dejeuner', 'cluster_1', 'seul')
couples = mf.creation_couples(regles_filtre,nomenclature)
scores = mf.score_substitution(couples,regles_filtre)

#t_subst = tableau_substitution(regles_filtre, nomenclature)
#score_contexte = matrice_scores_diff_moy(t_subst, regles_filtre)
