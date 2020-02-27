# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 09:36:39 2020

@author: chulai
"""

# FUNCTION IMPORT
import random
import pandas as pd
import numpy as np
#import numpy as np
#from mlxtend.frequent_patterns import fpgrowth
#import preference_consommateur as pref
#import motifs_frequents_substituabilite as mf

# =============================================================================


class VirtualUser():
    """
    Definit les caractéristiques de l'utilisateur
    """
    def __init__(self, _id, tab_pref, tab_sub, w):
        self.id = _id
        self.epsilon = 1
        
        # Affection de l'utilisateur à un cluster de consommation
        self.affect_cluster()
        
        # Création de la table de préférence individuelle
        self.creation_tab_indi(tab_pref, tab_sub)
        
        # Vitesse de modification de epsilon
        # len(....) est le nombre de recommandations "uniques" dont le score est > à 0.5
        self.ep_speed = round(2 / len(self.tab_rep_indi[self.tab_rep_indi['score_substitution'] > 0.5].groupby(['aliment_1', 'aliment_2']).size()), 4)
        
        # score de substitution**w*score de nutrition**(1-w) (score entre 0 et 1)
        self.w = w #w initial petit -> on privilégie score de substitution (comme score appartient entre 0 et 1)
        
        # malus de diversité des recommandations
        self.diversite = []
        
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
        # ========================
        
        # Filtrage de table de préférence du cluster
        self.tab_pref_indi = tab_pref[tab_pref['cluster_consommateur'] == self.cluster].reset_index(drop = True)
        self.tab_pref_indi = self.tab_pref_indi.drop('cluster_consommateur', axis = 1)
        
        # Personnalisation de table de préférence : ajoute aléatoirement -10 à 10% du taux de consommation par groupe
        self.tab_pref_indi['customize'] = [1 + random.uniform(-0.1, 0.1) for i in range(len(self.tab_pref_indi))]
        
        # Application sur les colonnes
        self.tab_pref_indi['nbre_repas_grp'] = self.tab_pref_indi['nbre_repas_grp']*self.tab_pref_indi['customize']
        self.tab_pref_indi['nbre_repas_code'] = self.tab_pref_indi['nbre_repas_code']*self.tab_pref_indi['customize']
        self.tab_pref_indi['consommation'] = self.tab_pref_indi['consommation']*self.tab_pref_indi['customize']
        
        # Recalcul des taux 
        self.tab_pref_indi['taux_code_apparaitre'] = round(100*self.tab_pref_indi['nbre_repas_code']/self.tab_pref_indi['nbre_repas_grp'], 2)
        self.tab_pref_indi['taux_conso_par_code'] = round(100*self.tab_pref_indi['consommation']/self.tab_pref_indi['nbre_repas_code'], 2)
        
        
        # TABLE DE SUBSTITUTION (PERMETTRE AU SYSTÈME DE RECOMMANDER DES SUBSTITUTIONS)
        # ================================================================================
        # Filtrage de table de substitution du cluster
        self.tab_sub_indi = tab_sub[tab_sub['cluster'].isin(['cluster_'+str(self.cluster), 'all'])].reset_index(drop = True)
        
        # Personnalisation de table de substitution : ajoute aléatoirement - 10 à 10% du score de substitution par groupe
        self.tab_sub_indi['score_substitution'] = self.tab_sub_indi['score_substitution'].apply(
                lambda score : round(score*(1+random.uniform(-0.1, 0.1)), 2)).apply(
                        lambda score : score if score < 1 else 1)
        
        self.tab_sub_indi['histoire_recomm'] = False
        
        
        # TABLE DE RÉPONSE (PERMETTRE AUX CONSOMMATEURX DE RÉPONDRE À LA RECOMMANDATION)
        # ================================================================================
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

            nbre_plat = len(self.repas)        

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


    def reponse_substitution(self, cluster, type_repas, avecqui, recommandation) :
        
        reponse = False
        if len(recommandation) > 0 :
            if random.random() <= self.tab_rep_indi[(self.tab_rep_indi['cluster'] == cluster) &
                                                        (self.tab_rep_indi['tyrep'] == type_repas) &
                                                        (self.tab_rep_indi['avecqui'] == avecqui) &
                                                        (self.tab_rep_indi['aliment_1'] == recommandation[0]) &
                                                        (self.tab_rep_indi['aliment_2'] == recommandation[1])]['score_substitution'].tolist()[0] :
                reponse = True          
        return reponse
    
    
    def update_pref(self, conso_code_sem, conso_lib_sem) :
        
        # Ajout du nombre de repas d'une semaine par type de repas
        self.tab_pref_indi['nbre_repas_grp'] = self.tab_pref_indi['nbre_repas_grp'] + 7
        
        # Ajout du nombre de repas d'une semaine par code de role
        self.tab_pref_indi = pd.DataFrame.merge(self.tab_pref_indi,
                                                conso_code_sem[conso_code_sem['id_user'] == self.id].drop(
                                                        'id_user', axis = 1),
                                                on = ['tyrep', 'code_role'],
                                                how = 'left').fillna(0)
        self.tab_pref_indi['nbre_repas_code'] += self.tab_pref_indi['conso_code_sem']
        
        # Ajout du nombre de repas d'une semaine par sous-groupe d'aliments
        self.tab_pref_indi = pd.DataFrame.merge(self.tab_pref_indi,
                                                conso_lib_sem[conso_lib_sem['id_user'] == self.id].drop(
                                                        'id_user', axis = 1),
                                                on = ['tyrep', 'libsougr'],
                                                how = 'left').fillna(0)
        self.tab_pref_indi['consommation'] += self.tab_pref_indi['consommation_sem']
        
        # Mise à jour les taux
        self.tab_pref_indi['taux_code_apparaitre'] = round(100*self.tab_pref_indi['nbre_repas_code'] / self.tab_pref_indi['nbre_repas_grp'], 2)
        self.tab_pref_indi['taux_conso_par_code'] = round(100*self.tab_pref_indi['consommation'] / self.tab_pref_indi['nbre_repas_code'], 2)
        
        # Drop des colones ajoutées
        self.tab_pref_indi.drop(['conso_code_sem', 'consommation_sem'], axis = 1, inplace = True)


        
class System() :
    
    def __init__(self, nbre_user, nbre_jour, seuil_nutri = 70, alpha = 1.005, beta = 1.002, omega = 0.1, seuil_recom = 5, seuil_acc = 0.5, pas_modif = 0.01) :
        
        # LOAD DATAFRAME
        #self.conso_pattern_sougr = pd.read_csv('Base_a_analyser/conso_pattern_sougr_transfo.csv',sep = ";",encoding = 'latin-1')
        self.nomenclature = pd.read_csv("Base_a_analyser/nomenclature.csv",sep = ";",encoding = 'latin-1')
        
        # Regles : supp = 0.001, conf = 0.01
        self.regles = pd.read_csv("Base_Gestion_Systeme/regles.csv", sep = ";", encoding = 'latin-1')
        
        # Création de table de préférence
        self.tab_pref = pd.read_csv('Base_Gestion_Systeme/preference_consommation.csv', sep = ";", encoding = 'latin-1')
        
        # Score de nutrition
        self.score_nutri = pd.read_csv('Base_Gestion_Systeme/scores_sainlim_ssgroupes.csv',sep=';', encoding="latin-1")
        
        # Score par contextes :
        self.score_contexte = pd.read_csv('Base_Gestion_Systeme/score_par_contextes.csv', sep = ';', encoding="latin-1")
        
        # contexte de repas
        self.liste_tyrep = ['petit-dejeuner', 'dejeuner', 'gouter', 'diner']
        self.liste_avecqui = ['seul', 'accompagne']

        # constant d'apprentissage
        self.seuil_nutri = seuil_nutri
        self.alpha = alpha
        self.beta = beta
        self.omega = omega
        
        # constant de pondération
        self.seuil_recom = seuil_recom # nombre de dernière recommandation à évaluer
        self.seuil_acc = seuil_acc # seuil du taux de réponse positive à self.seuil_recom dernières recommandations
        self.pas_modif = pas_modif # pas de modification de chaque pondération
        
        # Création des utilisateurs
        self.nbre_user = nbre_user
        self.add_VirtualUser()
        
        # Création de table de suivi de consommation
        self.nbre_jour = nbre_jour
        self.jour_courant = 1
        self.table_suivi = pd.DataFrame(columns = ['user', 'cluster', 'id_user', 'nojour', 'tyrep', 'avecqui', 'repas', 'substitution', 'reponse', 'omega', 'epsilon'])
        
        
    def add_VirtualUser(self) :
        self.liste_user = []
        for iden in range(1, self.nbre_user + 1) :
            print(iden)
            self.liste_user.append(VirtualUser(iden, self.tab_pref, self.score_contexte, self.omega))    
    
    
    def propose_repas(self) :
        """
        La fonction qui propose les repas de tous les consommateurs du jour self.jour_courant
        """
        
        
        # Table d'un repas pour tous les utilisateurs
        for type_repas in self.liste_tyrep :

            self.conso_repas = pd.DataFrame(data = {
                    'user' : self.liste_user,
                    'cluster' : [user.cluster for user in self.liste_user],
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

    
    def recommandation_substitution(self, user, type_repas, avecqui, repas) :
        
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
        
        # Recommandation par défaut
        recommandation = ()
        
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
            
            # EPSILON-GREEDY
            ep = random.random()
            if ep <= user.epsilon :
                recomm_epsi_df = user.tab_sub_indi.loc[user.tab_sub_indi['histoire_recomm'] == False]
            # Exploitation de la table (des substitutions déjà proposées)
            else :
                recomm_epsi_df = user.tab_sub_indi.loc[user.tab_sub_indi['histoire_recomm'] == True]
            
            
            # RECHERCHE DE SUBSTITUTION
            
            # Définition du niveau de recherche
            cluster = 'cluster_'+str(user.cluster)
            niveau = 1
            niveau_contexte = {1 : [cluster, avecqui], 2 : [cluster, 'all'], 3 : ['all', 'all']}
            
            while len(recommandation) == 0 and niveau <= 3:
                
                # Filtrage des substitutions possibles à partir du contexte et de la liste des aliments à substituer
                # Reset_index est nécessaire pour éviter SettingwithCopyWarning de python
                cluster, avecqui = niveau_contexte[niveau]
                recomm_df = recomm_epsi_df.loc[(recomm_epsi_df['cluster'] == cluster) &
                                               (recomm_epsi_df['tyrep'] == type_repas) &
                                               (recomm_epsi_df['avecqui'] == avecqui) &
                                               (recomm_epsi_df['aliment_1'].isin(aliment_a_substituer))].reset_index(drop = True)
                
                # Malus de diversité
                recomm_df['couples'] = list(zip(recomm_df['aliment_1'], recomm_df['aliment_2']))
                recomm_df['diversite'] = 1
                #recomm_df['couples'].apply(lambda couple : 1 / (user.diversite.count(couple) + 1))
                

                # Maximiser le score défini par la formule pour toutes les substitutions possibles
                recomm_df['score'] = (recomm_df['diversite']*recomm_df['score_substitution']**user.w) * (recomm_df['score_sainlim_nor']**(1 - user.w))
                recomm_df = recomm_df[recomm_df['score'] == recomm_df['score'].max()]
                recomm_df.reset_index(drop = True, inplace = True)
            
                # Recommandation
                try :
                    recommandation = (recomm_df['aliment_1'][0], recomm_df['aliment_2'][0])
                except :
                    pass
                
                niveau += 1
            
            # Si le système trouve pas de substitution dans la table de substitution, on cherche le meilleur gain nutri dans la table nutrition
#            if len(recommandation) == 0 :
#                
#                cluster, avecqui = niveau_contexte[1]
#                tab_nutri = self.score_nutri.copy()
#                
#                # Liste des code groupe
#                liste_codgr = self.score_nutri[self.score_nutri['libsougr'].isin(aliment_a_substituer)]
#                liste_codgr = liste_codgr[['libsougr', 'codgr', 'distance_origine']].rename(
#                        columns = {'libsougr' : 'alim_a_subst'})
#                
#                # Filtrage des aliments dans ce codgr
#                tab_nutri = pd.DataFrame.merge(tab_nutri[~ tab_nutri['libsougr'].isin(aliment_a_substituer)],
#                                               liste_codgr,
#                                               on = 'codgr')
#                tab_nutri['gain_sainlim'] = tab_nutri['distance_origine_x'] - tab_nutri['distance_origine_y']
#                
#                # Recommandation
#                tab_nutri = tab_nutri[tab_nutri['gain_sainlim'] == max(tab_nutri['gain_sainlim'])].reset_index(drop = True)
#                recommandation = (tab_nutri['alim_a_subst'][0], tab_nutri['libsougr'][0])

        return recommandation, cluster, type_repas, avecqui
    
    
    def mise_a_jour(self, user, cluster, type_repas, avecqui, recommandation, reponse) :
        """
        La fonction qui met à jour les scores de substituabilité après chaque accord / refus de proposition d'un repas substituable
        """
        # S'il existe une recommandation
        if len(recommandation) > 0 :
            
            # MISE À JOUR LES SCORE DE SUBSTITUABILITÉ INDIVIDUELLE
            # ========================================================
            
            # Dictionnaire de la puissance de alpha et beta
            dict_puis = {True : 1, False : -1}
            
            # Les filtres à appliquer
            f_contexte = (user.tab_sub_indi['cluster'] == cluster) & (user.tab_sub_indi['tyrep'] == type_repas) & (user.tab_sub_indi['avecqui'] == avecqui)
            f_alim1 = user.tab_sub_indi['aliment_1'] == recommandation[0]
            f_alim2 = user.tab_sub_indi['aliment_2'] == recommandation[1]
            
            # Modifier les scores de a1 -> y et x -> a2
            user.tab_sub_indi.loc[f_contexte & (f_alim1 | f_alim2), 'score_substitution'] *= self.beta**dict_puis[reponse]
            
            # Modifier le score du couple a1 -> a2
            user.tab_sub_indi.loc[f_contexte & f_alim1 & f_alim2, 'score_substitution'] *= (self.alpha/self.beta)**dict_puis[reponse]
            
            # Remise du score à 1 si le score est supérieur à 1
            user.tab_sub_indi['score_substitution'] = user.tab_sub_indi['score_substitution'].apply(
                    lambda score : 1 if score > 1 else score)
            
            
            # MISE À JOUR L'HISTOIRE DE RECOMMANDATION
            # ==========================================
            user.tab_sub_indi.loc[f_contexte & f_alim1 & f_alim2, 'histoire_recomm'] = True
            
            
            # MISE À JOUR LE MALUS DE DIVERSITÉ
            # ====================================
            if len(user.diversite) == 5 :
                user.diversite = user.diversite[1:] + [recommandation]
            
            
            # MISE À JOUR EPSILON 
            # ======================
            user.epsilon = user.epsilon - user.ep_speed
            
    def ponderation(self, user, recommandation, reponse) :
        """
        Pondération pour chaque utilisateur après une recommandation de substitution et puis une réponse
        Si 20 derniers repas, >= 80% acceptation : w += pas si <= 20% acceptation : w += -pas (pas = 0.01)
        """
        
        # Si le système trouve une recommandation pour le nouveau repas proposé par l'utilisateur
        if len(recommandation) > 0 :
            
            # Nombre de dernières recommandations à extraire pour l'évaluation
            seuil_recom = self.seuil_recom - len(recommandation) # pour le cas simple actuel, len(recom) vaut toujours 1
            
            # Table de l'histoire de recommandation de l'utilisateur
            pond_df = self.table_suivi[(self.table_suivi['id_user'] == user.id) &
                                       (self.table_suivi['substitution'].str.len() > 0)]
            
            # Si le nombre de recommandation est suffisant
            if len(pond_df) >= seuil_recom :
                
                # Sélectionner sur les dernières recommandations
                #pond_df = pond_df.tail(seuil_recom)
                
                # Compter le nombre de réponse positive des dernières recommandations
                tx_pos = (pond_df.tail(seuil_recom)['reponse'].sum() + reponse) / self.seuil_recom
                if tx_pos >= self.seuil_acc :
                    user.w = min(user.w + self.pas_modif, 0.5)
                elif tx_pos <= 1 - self.seuil_acc :
                    user.w = max(user.w - self.pas_modif, 0.01)

            
    def processus_recommandation(self, user, type_repas, avecqui, repas) :
        """
        La fonction qui pour chaque repas de l'utilisateur, propose des recommandations de substitution,
        recoit la réponse de l'utilisateur et fait la pondération de omega 
        """
        
        # Recommandation
        recommandation, cluster_res, type_repas_res, avecqui_res = self.recommandation_substitution(user, type_repas, avecqui, repas)
        
        # Réponse de l'utilisateur à la recommandation
        reponse = user.reponse_substitution(cluster_res, type_repas_res, avecqui_res, recommandation)
        
        # Mise à jour le système (histoire de recommandation, score de substitution, malus de diversité, epsilon)
        self.mise_a_jour(user, cluster_res, type_repas_res, avecqui_res, recommandation, reponse)
        
        # Pondération de omega de chaque utilisateur
        self.ponderation(user, recommandation, reponse)
        
        return pd.Series([recommandation, reponse, user.w, user.epsilon])
    
    
    def entrainement(self) :
        
        """
        La fonction qui lance chaque jour des propositions de repas, puis des substitutions possibles,
        puis accord/refus des propositions de substitution, puis mise_a_jour_score et mise_a_jour_df
        """
        
        while self.jour_courant <= self.nbre_jour :
            
            print('Entrainement du jour : ', self.jour_courant , ' / ', self.nbre_jour)
            
            #Propose de repas
            self.propose_repas()
            
            #Processus de recommandation, de réponse et de mise à jour
            self.table_suivi[['substitution', 'reponse', 'omega', 'epsilon']] = self.table_suivi.apply(
                lambda row : self.processus_recommandation(row['user'], row['tyrep'], row['avecqui'], row['repas'])
                if row['nojour'] == self.jour_courant else pd.Series([row['substitution'], row['reponse'], row['omega'], row['epsilon']]), axis = 1)
            
            # Mise à jour de la table préférence
            if self.jour_courant % 7 == 0 :
                self.update_pref_sys()
            
            # Passe à la journée suivante
            self.jour_courant += 1


    def update_pref_sys(self) :
        
        """
        La fonction qui met à jour les tables de fréquence de consommasion de l'utilisateur après chaque SEMAINE
        """
        
        # Quand les données d'une semaine sont collectées
        # Filtrage des données de consommation de cette semaine
        tab_pref = self.table_suivi[(self.table_suivi['nojour'] > self.jour_courant - 7) &
                                    (self.table_suivi['nojour'] <= self.jour_courant)].reset_index(drop = True)
        
        # Transformation de la subsitution en deux colonnes
        tab_pref[['alim_a_subst', 'alim_subst']] = pd.DataFrame(tab_pref['substitution'].tolist(), index = tab_pref.index)
        
        # Transformation des repas du format liste à des lignes
        lst_col = 'repas'
        tab_pref = pd.DataFrame({
                col:np.repeat(tab_pref[col].values, tab_pref[lst_col].str.len())
                for col in tab_pref.columns.drop(lst_col)}
            ).assign(**{lst_col:pd.DataFrame(np.concatenate(tab_pref[lst_col].values))})
        
        # Réalisation des substitutions si la réponse est positive
        tab_pref.loc[(tab_pref.reponse == True) &
                     (tab_pref.repas == tab_pref.alim_a_subst),
                     'repas'] = tab_pref.loc[(tab_pref.reponse == True) &
                                             (tab_pref.repas == tab_pref.alim_a_subst),
                                             'alim_subst']
        
        # Remplacement tyrep (string à code)
        dict_tyrep = {'petit-dejeuner' : 1, 'dejeuner' : 3, 'gouter' : 4, 'diner' : 5}
        tab_pref['tyrep'] = tab_pref['tyrep'].map(dict_tyrep)
        
        # Merge avec la table nomenclature pour avoir les informations sur code_role
        tab_pref = pd.DataFrame.merge(tab_pref, self.nomenclature[['libsougr', 'code_role']].drop_duplicates(),
                                      left_on = 'repas', right_on = 'libsougr', how = 'left')
        
        # Calcul de la consommation par code_role pendant une semaine
        conso_code_sem = tab_pref.groupby(['id_user', 'tyrep', 'code_role'])['nojour'].nunique(
                ).reset_index(
                        ).rename(
                                columns = {'nojour' : 'conso_code_sem'})
        
        # Calcul de la consommation par sous-groupe d'aliments pendant une semaine
        conso_lib_sem = tab_pref.groupby(['id_user', 'tyrep', 'libsougr'])['nojour'].nunique(
                ).reset_index(
                        ).rename(
                                columns = {'nojour' : 'consommation_sem'})
        
        # Ajout de l'information dans la table de fréquence de chaque utilisateur
        for user in self.liste_user :
            user.update_pref(conso_code_sem, conso_lib_sem)

    
# TEST
#sys_test = System(2, 15) # 10 utilisateurs, 7 jours d'entrainement
#
#sys_test.entrainement()
#
#suivi_df = sys_test.table_suivi


# =============================================================================
# FONCTION D'ENTRAINEMENT

def entrainement_systeme(nbre_user) :
    
    # Les constants 
    nbre_jour = 30
    
    liste_alpha_beta = [[1.01, 1.005], [1.1, 1.05], [1.15, 1.075]]
    # , [1.1, 1.05], [1.15, 1.075]
    dict_omega = {0 : [0.5], 0.01 : [0.2, 0.3]}
    seuil_acc = 0.8
    
    colnames = ['alpha', 'beta', 'omega_ini', 'seuil_acc', 'user', 'cluster', 'id_user', 'nojour', 'tyrep', 'avecqui', 'repas', 'substitution', 'reponse', 'omega', 'epsilon']
    data = pd.DataFrame(columns = colnames)
    
    for alpha, beta in liste_alpha_beta :
        for pas_modif, liste_omega in dict_omega.items() :
            for omega in liste_omega :
                print(alpha, beta, omega, pas_modif, seuil_acc)
                systeme = System(nbre_user, nbre_jour, seuil_nutri = 80, alpha = alpha, beta = beta, omega = omega, seuil_recom = 10, seuil_acc = seuil_acc, pas_modif = pas_modif)
                systeme.entrainement()
                df = pd.concat([pd.DataFrame(data = {'alpha' : alpha, 
                                                    'beta' : beta, 
                                                    'omega_ini' : omega, 
                                                    'seuil_acc' : seuil_acc}, index = range(len(systeme.table_suivi))),
                               systeme.table_suivi], axis = 1)
                data = data.append(df, sort = False)
    return data

# train_global_df = entrainement_systeme(1)
# train_global_df.to_pickle("Base_Gestion_Systeme/base_entrainement.pkl")




## ADD TRAINING_USER #
######################
    
train_df = entrainement_systeme(5)
train_global_df = pd.read_pickle("Base_Gestion_Systeme/base_entrainement.pkl")

def join_training_user(tab_ori, tab_add) :
    
    iden_add = tab_ori['id_user'].max()
    tab_add['id_user'] = tab_add['id_user'].apply(lambda iden : iden + iden_add)
    tab_ori = tab_ori.append(tab_add, sort = False)
    
    return tab_ori

train_global_df = join_training_user(train_global_df, train_df)
#train_global_df.to_pickle("Base_Gestion_Systeme/base_entrainement.pkl")


#train_df = entrainement_systeme(10)
#train_df.to_csv("Base_Gestion_Systeme/base_entrainement.csv", sep = ";", encoding = "latin-1", index = False)
# =============================================================================

