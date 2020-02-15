# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 09:36:39 2020

@author: ADMIN
"""

# FUNCTION IMPORT
import random
import pandas as pd
import numpy as np
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
    def __init__(self, _id, tab_pref, tab_sub):
        self.id = _id
        self.epsilon = 1
        
        # Affection de l'utilisateur à un cluster de consommation
        self.affect_cluster()
        
        # Création de la table de préférence individuelle
        self.creation_tab_indi(tab_pref, tab_sub)
        
        # score de substitution**w*score de nutrition**(1-w) (score entre 0 et 1)
        self.w = 0.1 #w initial petit -> on privilégie score de substitution (comme score appartient entre 0 et 1)

    def affect_cluster(self):
        """
        Permet d'affecter l'utilisateur à un cluster de consommateur
        """
        self.cluster = random.randint(1,8)


    def creation_tab_indi(self, tab_pref, tab_sub) :
        """
        La fonction qui crée une table de préférence individuelle des sous-groupes d'aliments
        .. et une table de score de substitution individuelle des sous-groupes d'aliments
        """
        # TABLE DE PRÉFÉRENCE
        # Filtrage de table de préférence du cluster
        self.tab_pref_indi = tab_pref[tab_pref['cluster_consommateur'] == self.cluster].reset_index(drop = True)
        
        # Personnalisation de table de préférence : ajoute aléatoirement -10 à 10% du taux de consommation par groupe
        self.tab_pref_indi = self.tab_pref_indi.loc[:, ['cluster_consommateur', 'tyrep', 'code_role', 'taux_code_apparaitre', 'libsougr', 'taux_conso_par_code']]
        self.tab_pref_indi['taux_conso_par_code'] = self.tab_pref_indi['taux_conso_par_code'].apply(
                lambda taux : round(taux*(1+random.uniform(-0.1, 0.1)), 2)).apply(
                        lambda taux : taux if taux <= 100 else 100)
        
        # TABLE DE SUBSTITUTION (PERMETTRE AU SYSTÈME DE RECOMMANDER DES SUBSTITUTIONS)
        # Filtrage de table de substitution du cluster
        self.tab_sub_indi = tab_sub[tab_sub['cluster'] == 'cluster_'+str(self.cluster)].reset_index(drop = True)
        
        # Personnalisation de table de substitution : ajoute aléatoirement - 10 à 10% du score de substitution par groupe
        self.tab_sub_indi['score_substitution'] = self.tab_sub_indi['score_substitution'].apply(
                lambda score : round(score*(1+random.uniform(-0.1, 0.1)), 2)).apply(
                        lambda score : score if score < 1 else 1)
        
        self.tab_sub_indi['histoire_recomm'] = False
        
        # TABLE DE RÉPONSE (PERMETTRE AUX CONSOMMATEURX DE RÉPONDRE À LA RECOMMANDATION)
        self.tab_rep_indi = self.tab_sub_indi.copy()
        
    
    def enter_repas(self, type_repas, avec_qui, regles):
        """
        La fonction qui renvoie la liste des aliments (sous-groupes) sélectionnées
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
        
        return self.repas_propose
    
        
#test_user = VirtualUser('pp', 'Homme', 16)
#test_user.cluster
#test_user.enter_repas('petit-dejeuner', 'famille', regles)


class System() :
    
    def __init__(self, _nbre_user, _nbre_jour) :
        
        # Load dataframe
        self.conso_pattern_sougr = pd.read_csv('Base_a_analyser/conso_pattern_sougr_transfo.csv',sep = ";",encoding = 'latin-1')
        self.nomenclature = pd.read_csv("Base_a_analyser/nomenclature.csv",sep = ";",encoding = 'latin-1')
        
        # Regles : supp = 0.001, conf = 0.01
        self.regles = pd.read_csv("Base_Gestion_Systeme/regles.csv", sep = ";", encoding = 'latin-1')
        
        # Score de nutrition
        self.score_nutri = pd.read_csv('Base_Gestion_Systeme/scores_sainlim_ssgroupes.csv',sep=';', encoding="latin-1")
        
        # Score par contextes :
        self.score_contexte = pd.read_csv('Base_Gestion_Systeme/score_par_contextes.csv', sep = ';', encoding="latin-1")
        
        # contexte de repas
        self.liste_tyrep = ['petit-dejeuner', 'dejeuner', 'gouter', 'diner']
        self.liste_avecqui = ['seul', 'accompagne']

        # constant d'apprentissage
        self.seuil_nutri = 70
        self.alpha = 1.005
        self.beta = 1.002
        
        # constant de pondération
        self.seuil_recom = 5 # nombre de dernière recommandation à évaluer
        self.seuil_acc = 0.5 # seuil du taux de réponse positive à self.seuil_recom dernières recommandations
        self.pas_modif = 0.01 # pas de modification de chaque pondération
        
        # Création de table de préférence
        self.tab_pref = pref.construct_table_preference(self.conso_pattern_sougr, self.nomenclature)
        
        # Création des utilisateurs
        self.nbre_user = _nbre_user
        self.add_VirtualUser()
        
        # Création de table de suivi de consommation
        self.nbre_jour = _nbre_jour
        self.jour_courant = 1
        self.liste_repas = ['petit-dejeuner', 'dejeuner', 'gouter', 'diner']
        self.liste_avecqui = ['seul', 'accompagne']
        self.table_suivi = pd.DataFrame(columns = ['user', 'id_user', 'nojour', 'tyrep', 'avecqui', 'repas', 'substitution', 'reponse'])
        
    def add_VirtualUser(self) :
        self.liste_user = []
        for iden in range(1, self.nbre_user + 1) :
            print(iden)
            self.liste_user.append(VirtualUser(iden, self.tab_pref, self.score_contexte))    
    
    
    def propose_repas(self) :
        """
        La fonction qui propose les repas de tous les consommateurs du jour self.jour_courant
        """
        
        # Table d'un repas pour tous les utilisateurs
        for type_repas in self.liste_tyrep :
            self.conso_repas = pd.DataFrame(data = {
                    'user' : self.liste_user,
                    'id_user' : [i for i in range(1, self.nbre_user + 1)],
                    'nojour' : self.jour_courant,
                    'tyrep' : type_repas,
                    'avecqui' : [random.choice(self.liste_avecqui) for i in range(self.nbre_user)]})
            
            # Proposition de repas
            self.conso_repas['repas'] = self.conso_repas['user'].apply(
                    lambda user : user.enter_repas(type_repas, self.conso_repas['avecqui'][user.id - 1], self.regles))
            
            # Enregistrement de l'information dans la table de suivi de consommation
            self.table_suivi = self.table_suivi.append(self.conso_repas, sort = False)
        
        # Reset index de la table de suivi de consommation
        self.table_suivi.reset_index(drop = True, inplace = True)
        
    
    def recommandation_reponse(self, user, type_repas, avecqui, repas) :
    
        """
        La fonction qui permet à l'utilisateur de recevoir une recommandation de substitution pour un repas donné.
        À réfléchir : la fonction appartient à quelle classe User / System pour que ce soit plus pratique?
        
        INPUT :
            user : utilisateur qui demande une recommandation de substitution -- class VirtualUser
            type_repas : petit-déjeuner | déjeuner | gouter | diner -- string
            avecqui : seul | accompagne -- string
            repas : liste des sous-groupes d'aliments du repas à améliorer -- list
        
        OUTPUT :
            recomm : la recommandation -- dict
            reponse : acceptation / refus de la recommandation - bool
        """
        
        global recomm_df
        
        recommandation = ()
        reponse = False
        
        # Identification de la liste des aliments à substituer 
        eval_repas = self.score_nutri[self.score_nutri['libsougr'].isin(repas)]
        if eval_repas['distance_origine'].min() <= self.seuil_nutri :
            # la liste des aliments dont le score de nutrition est plus mauvais que notre seuil s'il existe (à substituer)
            aliment_a_substituer = eval_repas[eval_repas['distance_origine'] <= self.seuil_nutri]['libsougr'].tolist()
        else :
            # le sous-groupe le "pire" s'il n'existe pas (score de nutrition minimal > seuil de nutrition)
            aliment_a_substituer = eval_repas[eval_repas['distance_origine'] == eval_repas['distance_origine'].min()]['libsougr'].tolist()
        
        # S'il existe des aliments à substituer, on lance l'algorithme epsilon-greeding
        if len(aliment_a_substituer) > 0 :
            
            recomm_df = recommandation
            ep = random.random()
            niveau = 1
            
            # Un boucle while à ajouter pour monter le niveau de filtrage (après car c'est un peu lourd)
            # Idée : while len(recommandation) == 0 or table_a_filter sont pas encore au bout de niveau (tyrep comme contexte seulement)
            # table_a_filter monte un niveau de recherche ; contexte = [......]
            while len(recomm_df) == 0 and niveau < 2:
            
                # EPSILON-GREEDING
                # Exploration de la table (des substitutions non proposées)
                if ep <= user.epsilon :
                    recomm_df = user.tab_sub_indi[user.tab_sub_indi['histoire_recomm'] == False]
                # Exploitation de la table (des substitutions déjà proposées)
                else :
                    recomm_df = user.tab_sub_indi[user.tab_sub_indi['histoire_recomm'] == True]
                
                # Filtrage des substitutions possibles à partir du contexte et de la liste des aliments à substituer
                recomm_df = recomm_df[(recomm_df['tyrep'] == type_repas) &
                                      (recomm_df['avecqui'] == avecqui) &
                                      (recomm_df['aliment_1'].isin(aliment_a_substituer))]

                # Maximiser le score défini par la formule pour toutes les substitutions possibles
                recomm_df['score'] = (recomm_df['score_substitution']**user.w) * (recomm_df['score_sainlim_nor']**(1 - user.w))
                recomm_df = recomm_df[recomm_df['score'] == recomm_df['score'].max()]
                recomm_df.reset_index(drop = True, inplace = True)
                
                niveau += 1
            
            try :
                recommandation = (recomm_df['aliment_1'][0], recomm_df['aliment_2'][0])
                if random.random() <= user.tab_rep_indi[(user.tab_rep_indi['tyrep'] == type_repas) &
                                                        (user.tab_rep_indi['avecqui'] == avecqui) &
                                                        (user.tab_rep_indi['aliment_1'] == recommandation[0]) &
                                                        (user.tab_rep_indi['aliment_2'] == recommandation[1])]['score_substitution'].tolist()[0] :
                    reponse = True
            except :
                pass

        return pd.Series([recommandation, reponse])
    
    
    def mise_a_jour(self, user, type_repas, avecqui, repas, recommandation, reponse) :
        """
        La fonction qui met à jour les scores de substituabilité après chaque accord / refus de proposition d'un repas substituable
        """
        # S'il existe une recommandation
        if len(recommandation) > 0 :
            
            # MISE À JOUR LES SCORE DE SUBSTITUABILITÉ INDIVIDUELLE
            # 
            dict_puis = {True : 1, False : -1}
            
            # Les filtres à appliquer
            f_contexte = (user.tab_sub_indi['tyrep'] == type_repas) & (user.tab_sub_indi['avecqui'] == avecqui)
            f_alim1 = user.tab_sub_indi['aliment_1'] == recommandation[0]
            f_alim2 = user.tab_sub_indi['aliment_2'] == recommandation[1]
            
            # Modifier les scores de a1 -> y et x -> a2
            user.tab_sub_indi.loc[f_contexte & (f_alim1 | f_alim2), 'score_substitution'] *= self.beta**dict_puis[reponse]
            
            # Modifier le score du couple a1 -> a2
            user.tab_sub_indi.loc[f_contexte & f_alim1 & f_alim2, 'score_substitution'] *= (self.alpha/self.beta)**dict_puis[reponse]
            
            # Remise le score à 1 si le score est supérieur à 1
            user.tab_sub_indi['score_substitution'] = user.tab_sub_indi['score_substitution'].apply(
                    lambda score : 1 if score > 1 else score)
            
            # MISE À JOUR L'HISTOIRE DE RECOMMANDATION
            user.tab_sub_indi.loc[f_contexte & f_alim1 & f_alim2, 'histoire_recomm'] = True
            
            # MISE À JOUR LE MALUS DE DIVERSITÉ
            
            
    def ponderation(self) :
        """
        La fonction qui met à jour la pondération de omega pour chaque utilisateur (à utiliser avec groupby)
        si 20 derniers repas, >= 80% acceptation : w += pas si <= 20% acceptation : w += -pas (pas = 0.01)
        """
        
        # Les constants
        seuil_recom = 5
        seuil_acceptation = 0.5
        pas_modif = 0.01
        
        # Enlever les repas pour lesquels le système ne recommande pas de substitution
        pond_df = self.table_suivi[self.table_suivi['substitution'].str.len() > 0]
        
        # Enlever les utilisateurs qui n'ont pas encore recu un certain nombre de recommdation
        pond_df = pond_df[pond_df.groupby('id_user')['id_user'].transform('size') >= seuil_recom]
        
        # Filtre sur les dernières recommandations
        pond_df = pond_df.groupby('id_user').apply(lambda x : x.tail(seuil_recom)).reset_index(drop = True)
        
        # Compter nombre de réponse True
        pond_df = pond_df.groupby('id_user')['reponse'].sum().reset_index()
        
        # Pondérer omege en fonction des conditions :
        # Augmente si le taux de réponse positive est supérieur à un seuil et...
        for id_user in pond_df[pond_df['reponse'] >= seuil_acceptation*seuil_recom]['id_user'].tolist() :
                self.liste_user[id_user - 1].w += pas_modif
        
        # ... Diminue si le taux de réponse positive est inférieur à un autre seuil
        for id_user in pond_df[pond_df['reponse'] <= (1 - seuil_acceptation)*seuil_recom]['id_user'].tolist() :
                self.liste_user[id_user - 1].w += - pas_modif

    
    def ponderation2(self, user, recommandation, reponse) :
        """
        Pondération pour chaque utilisateur après une recommandation de substitution et puis une réponse
        """
        # Nombre de dernières recommandations à extraire pour l'évaluation
        seuil_recom = self.seuil_recom - len(recommandation)
        
        # Table de l'histoire de recommandation de l'utilisateur
        pond_df = self.table_suivi[(self.table_suivi['id_user'] == user.id) &
                                   (self.table_suivi['substitution'].str.len() > 0)]
        
        # Si le nombre de recommandation est suffisant
        if len(pond_df) >= seuil_recom :
            
            # Sélectionner sur les dernières recommandations
            pond_df = pond_df.tail(seuil_recom).reset_index(drop = True)
            
            # Compter le nombre de réponse positive
            
            
            
    def processus_recommandation(self, user, type_repas, avecqui, repas) :
        """
        """
        
        # Recommandation
        recommandation, reponse = self.recommandation_reponse(user, type_repas, avecqui, repas)
        
        # Mise à jour le malus de diversité 
        # self.mise_a_jour_diversite(user, type_repas, avecqui, recommandation)
        
        # Mise à jour le score
        self.mise_a_jour(user, type_repas, avecqui, repas, recommandation, reponse)
        
        # Pondération de omega de chaque utilisateur
        self.ponderation2(user, recommandation, reponse)
        
        
        return pd.Series([recommandation, reponse, user.w])
    
    def training(self) :
        
        """
        La fonction qui lance chaque jour des propositions de repas, puis des substitutions possibles,
        puis accord/refus des propositions de substitution, puis mise_a_jour_score et mise_a_jour_df
        """

        self.table_suivi[['substitution', 'reponse']] = self.table_suivi.apply(
                lambda row : self.recommandation_reponse(row['user'], row['tyrep'], row['avecqui'], row['repas'])
                if row['nojour'] == self.jour_courant else pd.Series([row['substitution'], row['reponse']]), axis = 1)
    
    def entrainement_final(self) :
        
        """
        La fonction qui lance chaque jour des propositions de repas, puis des substitutions possibles,
        puis accord/refus des propositions de substitution, puis mise_a_jour_score et mise_a_jour_df
        """
        while self.jour_courant <= self.nbre_jour :
            #Propose de repas
            self.propose_repas()
            
            #Processus de recommandation, de réponse et de mise à jour
            self.table_suivi[['substitution', 'reponse', 'w']] = self.table_suivi.apply(
                    lambda row : self.processus_recommandation(row['user'], row['tyrep'], row['avecqui'], row['repas'])
                    if row['nojour'] == self.jour_courant else pd.Series([row['substitution'], row['reponse'], row['w']]), axis = 1)
            
            # Passe à la journée suivante
            self.jour_courant += 1


    
    def mise_a_jour_df(self) :
        """
        La fonction qui met à jour les tables de conso_pattern_sougr, preference, etc. après chaque pas de temps de simulation
        si ca fait 5% de la base conso_pattern_sougr total (if >= 5% then ...)
        """
        pass

# TEST
sys_test = System(10, 5)
# day1
sys_test.propose_repas() # client propose repas 1er jour
sys_test.training() # recommandation 1 er jour

# day2
sys_test.jour_courant += 1
sys_test.propose_repas()
sys_test.training()

test = sys_test.table_suivi
#=========


# Construction de mise à jour score

import pickle
#fileObject = open("save_sys", 'wb')
#pickle.dump(sys_test, fileObject)
#fileObject.close()
#
fileObject = open("save_sys", 'rb')
sys_test = pickle.load(fileObject)
fileObject.close()

test = sys_test.table_suivi

test1 = test[test['substitution'].str.len() > 0]
test1 = test1[test1.groupby('id_user')['id_user'].transform('size') >= 3]
#test1['tyrep'] = pd.Categorical(test1['tyrep'], ['petit-dejeuner', 'dejeuner', 'gouter', 'diner'])
#test1 = test1.groupby('id_user').apply(lambda _df: _df.sort_values(by=['nojour', 'tyrep']))
test1 = test1.groupby('id_user').apply(lambda x : x.tail(3)).reset_index(drop = True)

test2 = test1[test1.groupby('id_user')['reponse'].transform('sum') >= 0.5 * 3]['user'].unique().tolist()

test2 = test1.groupby('id_user')['reponse'].sum().reset_index()


user = sys_test.liste_user[6]
type_repas = 'dejeuner'
avecqui = 'seul'
repas = ['café', 'eau du robinet', 'eau minérale plate', 'sauces', 'légumes feuilles', 'légumes racines, tubercules ou bulbes', 'légumes tiges', 'mélanges de légumes, légumes préparés et autres légumes', 'autres poissons ou poissons sans précision', 'boeuf en pièces ou haché', 'plats à base de pâtes ou de pommes de terre', 'fromages affinés', 'yaourts et assimilés']
recommandation = ('vin', 'eau minérale plate')
reponse = True
alpha = 1.002
beta = 1.001


# score du couple
test1 = user.tab_sub_indi.copy()
dict_coef = {True : 1, False : -1}
filter1 = (test1['tyrep'] == type_repas) & (test1['avecqui'] == avecqui)
filter2 = test1['aliment_1'] == recommandation[0]
filter3 = test1['aliment_2'] == recommandation[1]


test1.loc[filter1 & (filter2 | filter3), 'score_substitution'] = test1.loc[filter1 & (filter2 | filter3), 'score_substitution'] * (beta**dict_coef[reponse])

test1.loc[filter1 & (filter2 | filter3), 'score_substitution'] *= beta**dict_coef[reponse]

test1.loc[filter1 & filter2 & filter3, 'histoire_recomm'] = True



score_contexte = pd.read_csv('Base_Gestion_Systeme/score_par_contextes.csv', sep = ';', encoding="latin-1")
