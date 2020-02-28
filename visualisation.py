# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 13:54:30 2020

@author: chulai
"""
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

score_contexte = pd.read_csv('Base_Gestion_Systeme/score_par_contextes.csv', sep = ';', encoding="latin-1")


def histo_cumul_subs(data) :
    
    # Manipulationi de données
    data = data[data['cluster'] != 'all']
    data = data.groupby('cluster').apply(lambda x: x.sort_values(['score_substitution'], ascending=True)).reset_index(drop = True)
    data['count_eff'] = 1
    data['count_eff'] = data.groupby('cluster')['count_eff'].transform(lambda x : x.cumsum())
    
    # Plot
    sns.set(style="ticks", color_codes=True)
    g = sns.FacetGrid(data, col = "cluster", col_wrap = 4, sharey = False)
    g = g.map(plt.plot, "count_eff", "score_substitution", color="steelblue")
    #g.set(xlim=(0, 1000), ylim=(0, 1))
    g.set(xticks = np.arange(0, 1100, 100), yticks = np.arange(0, 1.1, .1))
    g.fig.subplots_adjust(wspace = .2, hspace = .2)
    g.fig.subplots_adjust(top=.9)
    g.fig.suptitle('Nombre cumulé de substitutions en fonction du score de substitution par cluster',
                       fontsize = 16)
    g.set_axis_labels(x_var="Score de substitution", y_var="Nombre cumulé de substition")
    plt.show()

histo_cumul_subs(score_contexte)
