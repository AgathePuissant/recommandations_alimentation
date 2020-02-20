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
plt.text(0.2,500, str(dfLai.size)+' substitutions',color='green')


