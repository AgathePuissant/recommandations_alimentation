# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 10:31:28 2020

@author: anael
"""
import pandas as pd
import seaborn as sns
import numpy as np
import os
import matplotlib.pyplot as plt

dfAgathe=pd.read_csv("scores_tous_contextes_v4.csv",sep=",",encoding="ISO-8859-1")
dfLai=pd.read_csv(os.path.join("Base_Gestion_Systeme","score_par_contextes.csv"),sep=";",encoding="ISO-8859-1")


plt.hist(dfAgathe['score'])
plt.xlabel('Score de substitution')
plt.ylabel('Nombre de substitution')
plt.title('Histogramme de répartition des scores de substitution')
plt.text(0.3,500, str(dfAgathe.size)+' substitutions',color='green')
plt.show()


plt.hist(dfLai['score_substitution'])
plt.xlabel('Score de substitution')
plt.ylabel('Nombre de substitution')
plt.title('Histogramme de répartition des scores de substitution')
plt.text(0.2,1200, str(dfLai.size)+' substitutions',color='green')


# =============================================================================
# Histogramme pour le seuil du score nutritionnel
# =============================================================================
dataNutri=pd.read_csv(os.path.join('Base_Gestion_Systeme','scores_sainlim_ssgroupes.csv'),sep=';',encoding="ISO-8859-1")
plt.hist(dataNutri['distance_origine'])

plt.hist(dfLai['score_sainlim_nor'])


# =============================================================================
# Pour les tests de construction
# =============================================================================
dataNutri=pd.read_csv(os.path.join('Base_Gestion_Systeme','scores_sainlim_ssgroupes.csv'),sep=';',encoding="ISO-8859-1")
dfLai=pd.read_csv(os.path.join("Base_Gestion_Systeme","score_par_contextes.csv"),sep=";",encoding="ISO-8859-1")
dfLai.dtypes
dfLai['Valeur_malus']=0.2
Malus=dfLai['Valeur_malus']
ScoreSubst=dfLai['score_substitution']
ScoreNutri=dfLai['score_sainlim_nor']
omega=0.5
dfLai['S'] = Malus*(ScoreSubst**omega+ScoreNutri**(1-omega))
result=dfLai.loc[dfLai['S'].idxmax()]
result
nutri_result=dataNutri[dataNutri['libsougr']==result['aliment_2']][['libsougr','SAIN 5 opt','LIM3']].values.tolist()[0]
print(dataNutri[dataNutri['libsougr']==result['aliment_2']]['libsougr'].values[0])
nutri_result.append(result['S'])
nutri_result


Subst_secours=dataNutri[(dataNutri['codgr']==33)&(dataNutri['sougr']!=2)]
alimPropose=Subst_secours.loc[Subst_secours['distance_origine'].idxmax()] #on prend le max nutritionnel
nutriAlimPropose=dataNutri[dataNutri['libsougr']==alimPropose['libsougr']][['libsougr','SAIN 5 opt','LIM3']]
                                               
seq=dfLai[(((dfLai['aliment_1']=='café')&(dfLai['aliment_2']!='cacao, poudres et boissons cacaotées'))|((dfLai['aliment_1']!='café')&(dfLai['aliment_2']=='cacao, poudres et boissons cacaotées')))&
            (dfLai['cluster']=='cluster_1')&
            (dfLai['tyrep']=='petit-dejeuner')&
            (dfLai['avecqui']=='seul')][['aliment_1','aliment_2']]

seq


# =============================================================================
# Distribution du score sain_lim
# =============================================================================


sg_scores = pd.read_csv("scores_sainlim_ssgroupes.csv",sep = ",",encoding = 'latin-1')

print(sg_scores.head())

i = 0
for col in sg_scores.columns: 
    print(i,col)
    i += 1
    
def ajout_code_al(data):
    
    liste_code = []
    for i in range(len(data)):
        code = [int(data.iloc[[i],0]),int(data.iloc[[i],2])]
        liste_code.append(code)
    
    data["code_sougr"] = liste_code
    return(liste_code)    
    
    
    
def distrib_aliments(data):
    
    
    lib = list(data.iloc[:,3])
    x = data.iloc[:,6]
    y = data.iloc[:,5]
    
    plt.scatter(x, y)
    plt.annotate(lib[0], (x[0],y[0]))
    for i in range(1,len(lib)):
        if x[i]!= x[i-1] and y[i] != y[i-1]:
            plt.annotate(lib[i], (x[i], y[i]))
    
    plt.plot([7.5,7.5],[0,60],'go--', linewidth=2, marker=None)
    plt.plot([0,70],[5,5],'go--', linewidth=2,marker=None)
    plt.xlabel('LIM3')
    plt.ylabel('SAIN5opt')
    plt.title("Distribution des sous-groupes d'aliments en appliquant (SAIN 5opt, LIM 3)")
    plt.show()
        
        
    
ajout_code_al(sg_scores)
distrib_aliments(sg_scores)


# =============================================================================
# Choix de vitesse de décroissance de epsilon
# =============================================================================

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
