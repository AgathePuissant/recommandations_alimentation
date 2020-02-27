# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 10:31:28 2020

@author: anael
"""
import pandas as pd
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
