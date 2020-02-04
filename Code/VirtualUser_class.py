# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 09:36:39 2020

@author: anael
"""

# FUNCTION IMPORT
import random
import pandas as pd
from mlxtend.frequent_patterns import fpgrowth
import preference_consommateur as pref
import motifs_frequents_substituabilite as mf

# =============================================================================


# =============================================================================
# DATA IMPORT
#conso_pattern_sougr = pd.read_csv('Base_a_analyser/conso_pattern_sougr_transfo.csv',sep = ";",encoding = 'latin-1')
#nomenclature = pd.read_csv("Base_a_analyser/nomenclature.csv",sep = ";",encoding = 'latin-1')

#t_subst = mf.tableau_substitution(regles, nomenclature)
#tab_scores = mf.matrice_scores_diff_moy(t_subst, regles)

# =============================================================================

# =============================================================================
# GLOBAL VARIABLE
#supp = 0.001
#conf = 0.01

# DATA PREPARATION
#motifs = mf.find_frequent(conso_pattern_sougr, seuil_support = supp, algo = fpgrowth)
#regles = mf.regles_association(motifs, confiance = conf, support_only = False, support = 0.1)
#regles.to_csv('Base_Gestion_Systeme/regles.csv', sep = ';', encoding = 'latin-1', index = False)
# =============================================================================

class VirtualUser():
    """
    Definit les caractéristiques de l'utilisateur
    """
    def __init__(self, _id, tab_pref):
        self.id = _id
        self.epsilon = 1
        
        # Affection de l'utilisateur à un cluster de consommation
        self.affect_cluster()
        
        # Création de la table de préférence individuelle
        self.creation_tab_pref(tab_pref)


    def affect_cluster(self):
        """
        Permet d'affecter l'utilisateur à un cluster de consommateur
        """
        self.cluster = random.randint(1,8)


    def creation_tab_pref(self, tab_pref) :
        """
        La fonction qui crée une table de préférence individuelle des sous-groupes d'aliments
        """
        # Filtrage de table de préférence du cluster
        self.tab_pref_indi = tab_pref[tab_pref['cluster_consommateur'] == self.cluster].reset_index(drop = True)
        
        # Personnalisation de table de préférence : ajoute aléatoirement -10 à 10% du taux de consommation par groupe
        self.tab_pref_indi = self.tab_pref_indi.loc[:, ['cluster_consommateur', 'tyrep', 'code_role', 'taux_code_apparaitre', 'libsougr', 'taux_conso_par_code']]
        self.tab_pref_indi['taux_conso_par_code'] = self.tab_pref_indi['taux_conso_par_code'].apply(
                lambda taux : round(taux*(1+random.uniform(-0.1, 0.1)), 2)).apply(
                        lambda taux : taux if taux <= 100 else 100)

    
    def enter_repas(self, type_repas, avec_qui, regles):
        """
        _repasEntre : dictionnaire des comboboxs 
                    -> {Alim1: combobox_groupes,combobox_sgroupes}
        renvoie la liste des aliments (sous-groupes) sélectionnées
        """
        repas_code = {'petit-dejeuner' : 1, 'dejeuner' : 3, 'gouter' : 4, 'diner' : 5}
        
        nbre_plat = 0
        
        while nbre_plat == 0 :
            
            self.repas = self.tab_pref_indi[self.tab_pref_indi.tyrep == repas_code[type_repas]]
            
            # Filtrage de code de role
            code_role_filter = self.repas.groupby(['code_role', 'taux_code_apparaitre'])['taux_conso_par_code'].apply(
                    lambda taux : round(100*random.random(),2)).rename('filter_code').reset_index()
            
            code_role_filter = code_role_filter[code_role_filter['filter_code'] <= code_role_filter['taux_code_apparaitre']]
            
            self.repas = pd.DataFrame.merge(self.repas, code_role_filter, on = ['code_role', 'taux_code_apparaitre'], how = 'inner')
            
            # Filtrage des sous-groupes d'aliments
            self.repas['filter_conso'] = self.repas['filter_code'].apply(lambda taux : round(100*random.random(),2))
            self.repas = self.repas[self.repas['filter_conso'] <= self.repas['taux_conso_par_code']]

            nbre_plat = self.repas.shape[0]
        
        # Création du début du repas proposé
        self.repas_propose = self.repas.libsougr.tolist()
        
        # Filtrage des règles d'association pour le plat à proposer
        self.regles = regles.loc[regles['antecedents'].astype(str).str.contains(type_repas) &
                                 regles['antecedents'].astype(str).str.contains('cluster_'+str(self.cluster)) &
                                 regles['antecedents'].astype(str).str.contains(avec_qui)]
        if type_repas == 'dejeuner' :
            self.regles = self.regles.loc[~(self.regles['antecedents'].astype(str).str.contains('petit-dejeuner'))]
        self.regles.reset_index(drop = True, inplace = True)
        
        # Filtrage des plats proposés de bases
        #pd.DataFrame(self.regles.antecedents.tolist()).isin(self.repas.libsougr.tolist()).sum(axis = 1)
        self.regles = self.regles[pd.DataFrame(self.regles.antecedents.tolist()).isin(self.repas_propose).any(axis = 1) &
                                  ~pd.DataFrame(self.regles.consequents.tolist()).isin(self.repas_propose).any(axis = 1)]
        self.regles = self.regles.loc[self.regles.antecedents.str.len() == 4].reset_index(drop = True)
        self.regles = self.regles.loc[self.regles.groupby('antecedents')['confidence'].idxmax()]
        
        # Le repas proposé final du consommateur
        self.repas_propose = self.repas_propose + self.regles.consequents.str[0].tolist()
        print(self.repas_propose)
        
#test_user = VirtualUser('pp', 'Homme', 16)
#test_user.cluster
#test_user.enter_repas('petit-dejeuner', 'famille', regles)


class System() :
    
    def __init__(self) :
        
        # Load dataframe
        self.conso_pattern_sougr = pd.read_csv('Base_a_analyser/conso_pattern_sougr_transfo.csv',sep = ";",encoding = 'latin-1')
        self.nomenclature = pd.read_csv("Base_a_analyser/nomenclature.csv",sep = ";",encoding = 'latin-1')
        
        # Regles : supp = 0.001, conf = 0.01
        self.regles = pd.read_csv("Base_Gestion_Systeme/regles.csv", sep = ";", encoding = 'latin-1')
        
        # Score de nutrition
        self.score_nutri = pd.read_csv('Base_Gestion_Systeme/scores_sainlim_ssgroupes.csv',sep=';',encoding="latin-1")
        
        # Score par contextes :
        self.score_contexte = pd.read_csv('Base_Gestion_Systeme/scores_tous_contextes.csv', sep = ',')
        
        # contexte de repas
        self.liste_tyrep = ['petit-dejeuner', 'dejeuner', 'gouter', 'diner']
        self.liste_avecqui = ['seul', 'famille', 'amis']

        # constant d'apprentissage
        self.seuil_nutri = 70
        alpha = 1.2
        beta = 1
        
        # Création de table de préférence
        self.tab_pref = pref.construct_table_preference(self.conso_pattern_sougr, self.nomenclature)
        
        # Création des utilisateurs
        self.nber_user = 10
        self.add_VirtualUser()
        
        
    def add_VirtualUser(self) :
        self.liste_user = []
        for iden in range(1, self.nber_user + 1) :
            print(iden)
            self.liste_user.append(VirtualUser(iden, self.tab_pref))
    
    def propose_repas(self) :
        for user in self.liste_user :
            user.tyrep = random.choice(self.liste_tyrep)
            user.avecqui = random.choice(self.liste_avecqui)
            print(user.id, user.tyrep, user.avecqui)
            user.enter_repas(user.tyrep, user.avecqui, self.regles)
    
    def propose_substitution(self) :
        """
        repas - liste des libsougr
        """
        transform_avecqui = {'seul' : 'seul', 'famille' : 'accompagne', 'amis' : 'accompagne'}
        
        for user in self.liste_user :
            
            # Extraire aliment à substituer par score sain-lim
            user.nutrirepas = self.score_nutri[self.score_nutri['libsougr'].isin(user.repas_propose)]
            aliment_a_substituer = user.nutrirepas[user.nutrirepas['distance_origine'] <= self.seuil_nutri]['libsougr'].tolist()
            
            # Recherche des substitutions
            if len(aliment_a_substituer) > 0 : #s'il existe des aliments à substituer
                ep = random.random()
                if ep <= user.epsilon :
                    print('exploration')
                    
                    user.tab_subst = self.score_contexte[(self.score_contexte['cluster'] == 'cluster_'+str(user.cluster)) &
                                                         (self.score_contexte['repas'] == user.tyrep) &
                                                         (self.score_contexte['compagnie'] == transform_avecqui[user.avecqui])]
                    
                else :
                    print('exploitation')
            
            else :
                print('Le repas est bon')
        

regf = reg[reg.cluster_consommateur == 1]

sys_test = System()
sys_test.propose_repas()
sys_test.propose_substitution()


test = sys_test.score_contexte
test = test[(test['cluster'] == 'cluster_1') &
            (test['repas'] == 'petit-dejeuner')]

reg = sys_test.regles
test = sys_test.nutrirepas
test = sys_test.liste_user[1].nutrirepas
test[test['distance_origine'] <= 70]['libsougr'].tolist()
