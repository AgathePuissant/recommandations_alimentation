# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 21:12:53 2020

@author: lili-
"""
import pandas as pd

file="clusters_8.csv"
df_18 = pd.read_csv(file, sep = ";", encoding = 'latin-1')

def classif(caracteristique, liste_cat, liste_seuils):
    n = len(liste_cat)
    if n==2 :
        if caracteristique<liste_seuils[1]:
            return(liste_cat[0])
        return(liste_cat[1])
    if caracteristique<=liste_seuils[0]:
        return(liste_cat[0])
    for i in range(1,n-1):
        if (caracteristique>liste_seuils[i-1]) and (caracteristique<=liste_seuils[i]):
            return(liste_cat[i])
    if caracteristique>liste_seuils[n-1]:
        return(liste_cat[n-1])

def fonction_gower(x_1,x_2):
    """

    Parameters
    ----------
    x_1 : vecteur
        contenant les modalités associées à l'individu 1
    x_2 : vecteur
        contenant les modalités associées à l'individu 2

    Returns
    -------
    Similarité d'après l'indice de Gower

    """
    n_1 = len(x_1)
    n_2 = len(x_2) # x_2.shape[0]
    compteur = 0
    if n_1 == n_2 :
        for i in range(n_1):
            if x_1[i]==x_2[i]:
                compteur +=1
        return(compteur/n_1)
    return()

def distances_nid(df, n_id, distance="Gower"):
    """

    Parameters
    ----------
    df : data_frame
        data frame contenant les valeurs des modalités des autres individus (ceux de la table INCA2)
    n_id : vecteur
        contenant les modalités associées au nouvel individu
    distance : fonction Gower
        DESCRIPTION. The default is None.

    Returns
    -------
    vecteur de similarité avec les autres individus

    """
    #dimension = df.shape
    lignes = df.index
    n = len(lignes)
    X = []
    if distance == "Gower" :
        for i in range(0,n):
            j = lignes[i]
            dist = fonction_gower(n_id,list(df.loc[j]))
            X+=[dist]
    return(X)

def actualiser_table_clusters(df, x_n, nomen, clust):
    last_ind = df.index[-1]
    df.loc[last_ind+1] = [nomen]+x_n+[clust]
    df.to_csv('clusters_8.csv', index=False)