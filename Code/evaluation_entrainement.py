# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 10:43:31 2020

@author: ADMIN
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

train_global_df = pd.read_csv("Base_Gestion_Systeme/base_entrainement.csv", sep = ";", encoding = "latin-1")
#train_global_df['cluster'] = train_global_df['user'].apply(lambda user : user.cluster)

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
            columns = {'user' : 'count_True'}).drop(
                    'reponse', axis = 1)
    data['count_reponse'] = data.groupby(['alpha', 'beta', 'omega_ini', 'seuil_acc'])['count_True'].transform('sum')
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
def manipulation3() :
    pass

def visualisation3() :
    pass
# =============================================================================




















