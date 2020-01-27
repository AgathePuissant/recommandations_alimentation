# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 14:10:12 2020

@author: eloda
"""

import numpy as np
import pandas as pd

ciqual = pd.read_csv("tableciqual2017.csv",sep = ";",encoding = 'latin-1')
#print(ciqual.head())

#i = 0
#for col in ciqual.columns: 
#    print(i,col)
#    i += 1


def calcul_sainlim(data):
    """
    Calcul du score SAIN 5opt, qui estime  le pourcentage moyen de couverture 
    des recommandations nutritionnelles en 5 nutriments dans 100 kcal d'aliment consommé
    Calcul du score LIM3 qui estime le pourcentage de dépassement apports journaliers 
    maximaux recommandés pour 3 nutriments disqualifiants (Na, AGS, GS ajoutés) 
    dans 100 g d’aliment consommé.
    Ajout de 2 colonnes dans tableciqual2017 comportant ces scores
    """
    
    liste_sain = []
    liste_lim = []
    
    for i in range(len(data)):

        try:
            rap = [float(ciqual.iloc[[i],13])/65,float(ciqual.iloc[[i],19])/25,float(ciqual.iloc[[i],43])/900,float(ciqual.iloc[[i],46])/12.5,float(ciqual.iloc[[i],57])/5,float(ciqual.iloc[[i],61])/110]
            sain = ((((rap[0]+rap[1]+rap[2]+rap[3]+rap[4]+rap[5]-min(rap))/5)*100)/float(ciqual.iloc[[i],9]))*100
            if pd.isnull(sain) == True:
                liste_sain.append('NA')
            else:
                liste_sain.append(sain)          
        except:
            liste_sain.append('NA')
    
        try:
            lim = (((float(ciqual.iloc[[i],53])/3153)+(float(ciqual.iloc[[i],24])/22)+(float(ciqual.iloc[[i],17])/50))/3)*100
            if pd.isnull(sain) == True:
                liste_lim.append('NA')
            else:
                liste_lim.append(lim)  
            
        except :
            liste_lim.append('NA')

            
    data['SAIN5opt'] = liste_sain
    data['LIM3'] = liste_lim
    
    return(liste_sain,liste_lim)




def sainlim_moyenne(data):
    """
    Fais la moyenne des scores SAIN et LIM pour les sous-groupes de la table
    ciqual et les stocke dans 2 dictionnaires
    """
    
    sain_moyenne = {}
    lim_moyenne = {}
    
    somme_sain = 0 #Car la première valeur est un NA
    somme_lim = 0
    compte = 1
    ssgr = 4
    for i in range(1,len(data)):

        if list(ciqual.iloc[[i],ssgr])[0] == list(ciqual.iloc[[i-1],ssgr])[0]:
            if list(ciqual.iloc[[i],69])[0] != 'NA':
                somme_sain += float(ciqual.iloc[[i],69])
            if list(ciqual.iloc[[i],70])[0] != 'NA':  
                somme_lim += float(ciqual.iloc[[i],70])

            compte += 1
        
        
        else:
            sain_moyenne[list(ciqual.iloc[[i-1],ssgr])[0]] = somme_sain/compte
            lim_moyenne[list(ciqual.iloc[[i-1],ssgr])[0]] = somme_lim/compte
            compte = 1
            
            if list(ciqual.iloc[[i],5])[0] == '-':
                ssgr = 4
            else:
                ssgr = 5
                
            
            if list(ciqual.iloc[[i],69])[0] != 'NA':
                somme_sain = float(ciqual.iloc[[i],69])
            else:
                somme_sain = 0
            if list(ciqual.iloc[[i],70])[0] != 'NA':
                somme_lim = float(ciqual.iloc[[i],70])
            else:
                somme_lim = 0
                
    
    return(sain_moyenne)




sain = calcul_sainlim(ciqual)


moy = sainlim_moyenne(ciqual)
print(moy)

df = pd.DataFrame(moy, index=[0])

export_csv = ciqual.to_csv('tableciqual2017_sainlim.csv',index=False)
#export_csv = df.to_csv('ssgrp_ciqual.csv',index=False)