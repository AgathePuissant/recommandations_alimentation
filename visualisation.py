# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 13:54:30 2020

@author: ADMIN
"""

import matplotlib.pyplot as plt


plt.hist(score_contexte.score_substitution, bins = 40)
plt.xticks(np.arange(0, 1, step = 0.025))
plt.show()


test = score_contexte.groupby('cluster').apply(lambda x: x.sort_values(['score_substitution'], ascending=True)).reset_index(drop = True)
test['count_eff'] = 1
test['count_eff'] = test.groupby('cluster')['count_eff'].transform(lambda x : x.cumsum())

fil = test["cluster"].isin(['cluster_1', 'cluster_2', 'cluster_3', 'cluster_4', 'cluster_5'])


import seaborn as sns
sns.set(style="ticks", color_codes=True)
g = sns.FacetGrid(test, col = "cluster", sharey = False)
g.map(plt.plot, "count_eff", "score_substitution", color="steelblue")
