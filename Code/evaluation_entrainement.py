# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 10:43:31 2020

@author: chulai
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

train_global_df = pd.read_pickle("Base_Gestion_Systeme/base_entrainement.pkl")
nutri_df = pd.read_csv("Base_Gestion_Systeme/scores_sainlim_ssgroupes.csv", sep = ";", encoding = "latin-1")

# =============================================================================
# % RECOMMANDATIONS / REPAS PAR CLUSTER (IL FAUT AJOUTER LES CLUSTERS DANS LA TABLE AVANT D'ENREGISTRER)

# Global :

def taux_recommandation(data) :
    
    data = data.copy()
    
    # Comptage du nombre de repas    
    data['nbre_repas'] = data.groupby(['alpha', 'beta', 'omega_ini', 'seuil_acc'])['id_user'].transform('size')
    
    # Filtrage des repas dont le système propose une substitution
    data = data[data['substitution'].str.len() > 0]
    
    # Comptage du nombre de recommandation
    data = data.groupby(['alpha', 'beta', 'omega_ini', 'seuil_acc', 'nbre_repas'])['substitution'].size()
    data = data.rename('nbre_recom').reset_index()
    
    # Calcul du taux de recommandation
    data['taux_recommandation'] = round(100*data['nbre_recom'] / data['nbre_repas'], 2)
    
    # Couple alpha - beta
    data['alpha_beta'] = list(zip(data['alpha'], data['beta']))
    
    return data


def visualisation_tx_recom(data) :
    
    # Plot facet grid    
    sns.set(style="ticks", color_codes=True)
    g = sns.FacetGrid(data, col = "alpha_beta", hue = "omega_ini", col_wrap = 3, sharey = False, legend_out = False)
    g = (g.map(plt.bar, "omega_ini", "taux_recommandation", width = 0.08).add_legend())
    g.set(xlim = (0.1, 0.6), ylim = (0, 80),
          xticks = np.arange(0.1, 0.6, 0.1), yticks = np.arange(0, 80, 5))
    
    # Title and axis title
    g.fig.suptitle("Taux de recommandation par repas selon l'initialisation des paramètres",
                       fontsize = 25)
    g.set_xlabels("Omega initial (sans unité)", fontsize = 16)
    g.set_ylabels("Taux de recommandation (%)", fontsize = 16)
    
    plt.show()
    

def visualisation_tx_recom_cl(data) :
    
    # Plot facet grid    
    sns.set(style = "ticks", color_codes = True, font_scale = 1)
    g = sns.FacetGrid(data, row = "alpha_beta", col = "cluster", hue = "omega_ini", sharey = False, margin_titles = True)
    g = (g.map(plt.bar, "omega_ini", "taux_recommandation", width = 0.08).add_legend())
    g.set(xlim = (0.1, 0.6), ylim = (0, 80),
          xticks = np.arange(0.1, 0.6, 0.1), yticks = np.arange(0, 80, 10))
    
    # Title and axis title
    g.fig.subplots_adjust(top = .9)
    g.fig.suptitle("Taux de recommandation par repas selon l'initialisation des paramètres",
                       fontsize = 18)
    g.set_xlabels("Omega initial (sans unité)", fontsize = 12)
    g.set_ylabels("Taux de recommandation (%)", fontsize = 12)
    
    plt.show()


## VISUALISATION
##################

# Data Préparation
tx_recom_df = taux_recommandation(train_global_df)
tx_recom_cl_df = train_global_df.groupby('cluster').apply(lambda df : taux_recommandation(df)).reset_index()

# Graphiques
visualisation_tx_recom(tx_recom_df)
visualisation_tx_recom_cl(tx_recom_cl_df)

# =============================================================================


# =============================================================================
# % SUBSTITUTIONS ACCEPTÉES / PROPOSÉES PAR COEFF
def taux_acceptation_df(data) :
    
    # Filtrage des repas dont le système propose une substitution
    data = data[data['substitution'].str.len() > 0]
    
    # Comtage le nombre de réponse True et False
    data = data.groupby(['alpha', 'beta', 'omega_ini', 'seuil_acc', 'reponse']).size(
            ).rename('count_True').reset_index()
    
    # Comptage le nombre de réponse au total (True + False)
    data['count_reponse'] = data.groupby(['alpha', 'beta', 'omega_ini', 'seuil_acc'])['count_True'].transform('sum')
    
    # Filtrage des réponses True
    data = data[data['reponse'] == True].drop('reponse', axis = 1)
    
    # Calcul du taux d'acceptation
    data['taux_acceptation'] = round(100*data['count_True'] / data['count_reponse'], 2)
    
    # Couple alpha - beta
    data['alpha_beta'] = list(zip(data['alpha'], data['beta']))
    
    return data



def visualisation_tx_acc(data) :
    
    # Plot facet grid    
    sns.set(style="ticks", color_codes=True)
    g = sns.FacetGrid(data, col = "alpha_beta", hue = "omega_ini", col_wrap = 3, sharey = False, legend_out = False)
    g = (g.map(plt.bar, "omega_ini", "taux_acceptation", width = 0.08).add_legend())
    g.set(xlim = (0.1, 0.6), ylim = (20, 50),
          xticks = np.arange(0.1, 0.6, 0.1), yticks = np.arange(20, 50, 2))
    
    # Title and axis title
    g.fig.suptitle("Taux d'acceptation de recommandation selon l'initialisation des paramètres",
                       fontsize = 25)
    g.set_xlabels("Omega initial (sans unité)", fontsize = 16)
    g.set_ylabels("Taux d'acceptation (%)", fontsize = 16)
    
    # Color legend
#    omega_dict = {0.2 : 'steelblue', 0.3 : 'sandybrown', 0.5 : 'forestgreen'}
#    handles = [mpatches.Patch(color = col, label = lab) for lab, col in omega_dict.items()]
#    plt.legend(handles = handles)
    plt.show()



def visualisation_tx_acc_cl(data) :
    
    # Plot facet grid    
    sns.set(style = "ticks", color_codes = True, font_scale = 1)
    g = sns.FacetGrid(data, row = "alpha_beta", col = "cluster", hue = "omega_ini", sharey = False, margin_titles = True)
    g = (g.map(plt.bar, "omega_ini", "taux_acceptation", width = 0.08).add_legend())
    g.set(xlim = (0.1, 0.6), ylim = (20, 50),
          xticks = np.arange(0.1, 0.6, 0.1), yticks = np.arange(20, 50, 2))
    
    # Title and axis title
    g.fig.subplots_adjust(top = .9)
    g.fig.suptitle("Taux d'acceptation de recommandation selon l'initialisation des paramètres",
                       fontsize = 18)
    g.set_xlabels("Omega initial (sans unité)", fontsize = 12)
    g.set_ylabels("Taux d'acceptation (%)", fontsize = 12)
    
    plt.show()
    
# VISUALISATION
# Data
tx_acc_df = taux_acceptation_df(train_global_df)
tx_acc_cl_df = train_global_df.groupby('cluster').apply(lambda df : taux_acceptation_df(df)).reset_index()

# Graphiques
visualisation_tx_acc(tx_acc_df)
visualisation_tx_acc_cl(tx_acc_cl_df)

# =============================================================================

# =============================================================================
# AMÉLIORATION DU SCORE NUTRI PAR COEFF
def score_nutri_repas(data,nutri) :
    # Déplacer chacune des paires d'indices en une ligne séparément 
    
    #Décomposition des repas pour avoir un aliment par ligne
    lst_col = 'repas'
    data = pd.DataFrame({
          col:np.repeat(data[col].values, data[lst_col].str.len())
          for col in data.columns.drop(lst_col)}
        ).assign(**{lst_col:pd.DataFrame(np.concatenate(data[lst_col].values))})
    
    #Ajout d'une colonne avec le score SAIN LIM de chaque aliment 
    data = data.rename(columns = {'repas' : 'libsougr'})
    #Séparation de la colonne substitution en 2 colonnes
    data[['alim_a_sub','alim_prop']] = pd.DataFrame(data.substitution.values.tolist(), index= data.index)

#libsougr_conso donne la liste des aliments réellements consommés (en prenant en compte les substitutions)
    data['libsougr_conso'] = data['libsougr']
    data.loc[(data.reponse == True) &
                 (data.libsougr_conso == data.alim_a_sub),
                        'libsougr_conso'] = data.loc[(data.reponse == True) &
                              (data.libsougr_conso == data.alim_a_sub),'alim_prop']
    
    
    data = pd.DataFrame.merge(data, nutri, on = 'libsougr', how = 'left').drop([
            'codgr','libgr','sougr','sougr ciqual correspondant',
       'SAIN 5 opt', 'LIM3', '100_LIM3'], axis = 1).rename(
            columns = {'distance_origine' : 'scorenutri_ali_prop'})
    
    
    data = pd.DataFrame.merge(data, nutri, left_on = 'libsougr_conso', right_on='libsougr', how = 'left').drop([
            'codgr','libgr','sougr','sougr ciqual correspondant',
       'SAIN 5 opt', 'LIM3', '100_LIM3'], axis = 1).rename(
            columns = {'distance_origine' : 'scorenutri_ali_cons'})
    
    
    #Calcul de la moyenne du score SAIN LIM par repas
    #moyenne_rep = data.groupby(['alpha','beta','omega_ini','seuil_acc','id_user', 'nojour', 'tyrep'])['distance_origine'].apply(np.mean).reset_index().rename(
    #                columns = {'distance_origine' : 'scorenutri_rep'})
    
    #data = pd.DataFrame.merge(data, moyenne_rep, on = ['alpha','beta','omega_ini','seuil_acc','id_user','nojour','tyrep'], how = 'left')
    
    
    #Calcul de la moyenne du score SAIN LIM par jour (tout utilisateur et tout repas confondu)
    moyenne_jour = data.groupby(['alpha','beta','omega_ini','seuil_acc','nojour'])['scorenutri_ali_prop'].apply(np.mean).reset_index().rename(
            columns = {'scorenutri_ali_prop' : 'scorenutri_jour_prop'})
    
    moyenne_jour_cons = data.groupby(['alpha','beta','omega_ini','seuil_acc','nojour'])['scorenutri_ali_cons'].apply(np.mean).reset_index().rename(
            columns = {'scorenutri_ali_cons' : 'scorenutri_jour_cons'})
    
    #Calcul de l'écart-type du score SAIN LIM par jour (tout utilisateur et tout repas confondu)
    std_jour = data.groupby(['alpha','beta','omega_ini','seuil_acc','nojour'])['scorenutri_ali_prop'].apply(np.std).reset_index().rename(
            columns = {'scorenutri_ali_prop' : 'scorenutri_stdjour_prop'})
    
    std_jour_cons = data.groupby(['alpha','beta','omega_ini','seuil_acc','nojour'])['scorenutri_ali_cons'].apply(np.std).reset_index().rename(
            columns = {'scorenutri_ali_cons' : 'scorenutri_stdjour_cons'})
    
    #Création d'une table avec la moyenne et l'écart type de SAIN LIM par jour
    score_nutri1 = pd.DataFrame.merge(moyenne_jour, std_jour, on = ['alpha','beta','omega_ini','seuil_acc','nojour'], how = 'left')
    score_nutri2 = pd.DataFrame.merge(moyenne_jour_cons, std_jour_cons, on = ['alpha','beta','omega_ini','seuil_acc','nojour'], how = 'left')

    score_nutri = pd.DataFrame.merge(score_nutri1, score_nutri2, on = ['alpha','beta','omega_ini','seuil_acc','nojour'], how = 'left')

    #data = pd.DataFrame.merge(data, moyenne_jour, on = ['alpha','beta','omega_ini','seuil_acc','nojour'], how = 'left')
    #data = pd.DataFrame.merge(data, std_jour, on = ['alpha','beta','omega_ini','seuil_acc','nojour'], how = 'left')
    
    #Colonne param correspondant à la liste des valeurs des paramètres
    score_nutri['param'] = list(zip(score_nutri['alpha'], score_nutri['beta'],score_nutri['omega_ini'],score_nutri['seuil_acc']))
    score_nutri['alpha_beta'] = list(zip(score_nutri['alpha'], score_nutri['beta']))

    return(score_nutri)
    
    

def visualisation_nutri_continu(data,alpha= 1.0005,beta=1.0001,omega_ini=0.1,seuil_acc=0.8) :
    
    param = list(score_nutri["param"].unique())
    #data = data[data.omega_ini == omega_ini] 
    #data = data[data.seuil_acc == seuil_acc]
    
    for val in param:
        df = data[data.param == val]
        plt.plot(df.nojour, df.scorenutri_jour, label = val)
        plt.title("Evolution de la qualité nutritionnelle des repas en fonction des paramètres")
        plt.xlabel("jour")
        plt.ylabel("Moyenne du score SAIN-LIM")
        plt.legend()
        
    
# ==============================================
#score_nutri = score_nutri_repas(train_global_df,nutri_df)
#test = visualisation_nutri_continu(score_nutri)














