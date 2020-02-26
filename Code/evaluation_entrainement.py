# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 10:43:31 2020

@author: ADMIN
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from ast import literal_eval
import numpy as np

train_global_df = pd.read_csv("Base_Gestion_Systeme/base_entrainement.csv", sep = ";", encoding = "latin-1")
nutri_df = pd.read_csv("Base_Gestion_Systeme/scores_sainlim_ssgroupes.csv", sep = ";", encoding = "latin-1")
train_global_df['repas'] = train_global_df['repas'].apply(lambda repas : literal_eval(repas))
train_global_df['substitution'] = train_global_df['substitution'].apply(lambda substitution : literal_eval(substitution))

# =============================================================================
# % RECOMMANDATIONS / REPAS PAR CLUSTER (IL FAUT AJOUTER LES CLUSTERS DANS LA TABLE AVANT D'ENREGISTRER)

# Global : 
sum(train_global_df['substitution'].str.len() > 2)/len(train_global_df) # 78,07%

def manipulation1(data) :
    pass

def visualisation1() :
    pass

# =============================================================================


# =============================================================================
# % SUBSTITUTIONS ACCEPTÉES / PROPOSÉES PAR COEFF
def taux_acceptation_df(data) :
    
    data = data[data['substitution'].str.len() > 2]
    data = data.groupby(['alpha', 'beta', 'omega_ini', 'seuil_acc', 'reponse'])['user'].count().reset_index().rename(
            columns = {'user' : 'count_True'})
    data['count_reponse'] = data.groupby(['alpha', 'beta', 'omega_ini', 'seuil_acc'])['count_True'].transform('sum')
    data = data[data['reponse'] == True].drop(
                    'reponse', axis = 1)
    data['taux_acceptation'] = round(100*data['count_True'] / data['count_reponse'], 2)
    
    data['alpha_beta'] = list(zip(data['alpha'], data['beta']))
    
    return data

tx_acc_df = taux_acceptation_df(train_global_df)

def visualisation_tx_acc(data) :
    
    # Color
    col_dict = {0.5 : 'green', 0.75 : 'blue', 0.8 : 'red'}
    data['color_col'] = data['seuil_acc'].map(col_dict)
    
    # Marker shape
    mkr_dict = {(1.0005, 1.0001) : 'x', (1.001, 1.0005) : 'o', (1.005, 1.001) : '^', (1.01, 1.005) : 's'}
    
    
    for couple in mkr_dict:
        df = data[data.alpha_beta == couple]

        plt.scatter(x = df.omega_ini, y = df.taux_acceptation, c = df.color_col, marker = mkr_dict[couple], alpha = 0.5, label = couple)
        plt.title("Le taux d'acceptation de recommandation selon alpha, beta, omega et seuil d'acceptation", fontsize = 25)
        plt.xlabel("La valeur initiale de omega", fontsize = 25)
        plt.ylabel("Le taux d'acceptation", fontsize = 25)
        plt.legend()
        
    leg_el = [mpatches.Patch(facecolor = value, edgecolor = "black", label = key, alpha = 0.4) for key, value in col_dict.items()]
    plt.legend(handles = leg_el)
    plt.show()

    
visualisation_tx_acc(tx_acc_df)
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














