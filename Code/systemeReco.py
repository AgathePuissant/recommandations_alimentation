# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 14:39:43 2020

@author: anael
"""
# =============================================================================
# LIBRARY IMPORT
import tkinter as tk
from tkinter import ttk
import pandas as pd
import random
import os
from mlxtend.frequent_patterns import fpgrowth

# FUNCTION IMPORT
import preference_consommateur as pref
import motifs_frequents_substituabilite as mf

# =============================================================================


# =============================================================================
# DATA IMPORT
conso_pattern_sougr = pd.read_csv('Base_a_analyser/conso_pattern_sougr_transfo.csv',sep = ";",encoding = 'latin-1')
nomenclature = pd.read_csv("Base_a_analyser/nomenclature.csv",sep = ";",encoding = 'latin-1')

# =============================================================================


# =============================================================================
# GLOBAL VARIABLE
supp = 0.001
conf = 0.01

# DATA PREPARATION
motifs = mf.find_frequent(conso_pattern_sougr, seuil_support = supp, algo = fpgrowth)
regles = mf.regles_association(motifs, confiance = conf, support_only = False, support = 0.1)

# =============================================================================

class Application(tk.Frame):
    """
    Coeur de l'app
    """
    def __init__(self, master=None):
        """
        Initialisation de la fenêtre Tkinter
        """
        super().__init__(master)
        self.master = master
        self.grid()
        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)
        self.menu_widgets()
        self.currentUser=None

    def menu_widgets(self):
        """
        Menu de la page d'accueil
        """
        self.BnewUser = tk.Button(self,
                                  text='Nouvel utilisateur',
                                  command=self.getnew)
        self.BnewUser.grid(padx=5)

        self.Blaunch=tk.Button(self,
                              text='Proposer repas',
                              command=self.launch)
        self.Blaunch.grid(padx=5)

        self.quit = tk.Button(self,
                              text="QUIT",
                              fg="red",
                              command=self.master.destroy)
        self.quit.grid(padx=5)

    def clean_widgets(self):
        """
        Nettoie tous les widgets sur la fenêtre
        """
        for widget in self.winfo_children():
            widget.destroy()

    def getnew(self):
        """
        Entrée d'un nouvel utilisateur,
        formulaire
        """

        print("Nouvel utilisateur")
        self.clean_widgets()

        texte2=tk.Label(self,
                        text="A midi j'ai mangé de la chantilly")
        texte2.grid()


        l = tk.Label(self,
                     text='Nom',
                     width=10,
                     name='lnom')

        e = tk.Entry(self,
                     width=10,
                     name='nom')

        l.grid(column=0, row=1)
        e.grid(column=1,row=1)

        vals = ['F','H']
        etiqs = ['Femme', 'Homme']
        varGr = tk.StringVar()
        varGr.set(vals[1])
        for i in range(2):
            b = tk.Radiobutton(self,
                               variable=varGr,
                               text=etiqs[i],
                               value=vals[i],
                               name='sexe'+vals[i])
            b.grid(row=2,column=i)

        s=tk.Scale(self, label='age', name='age',
                 from_=0, to=100,
                 orient=tk.HORIZONTAL,
                 length=200)
        s.grid(row=3)


        print(self.winfo_children()) #list of widgets

        self.quit = tk.Button(self,
                              text="QUIT",
                              fg="red",
                              command=self.master.destroy)
        self.quit.grid(column=1,row=4)


        self.val=tk.Button(self,
                           text="Valider",
                           command= lambda:self.newUser(varGr))
        self.val.grid(column=0,row=4)


    def newUser(self, _sexe):
        """
        Récup des infos sur le formualire, 
        création d'une instance de la classe user
        """

        name = self.nametowidget('nom').get()
        age = self.nametowidget('age').get()
        sexe = _sexe.get()

        print(name,age,sexe)

        self.currentUser = User(name,sexe,age)
        self.clean_widgets()
        self.menu_widgets()



    def launch(self):
        """
        Formulaire d'info sur le contexte de consommation
        """
        if self.currentUser == None:
            self.currentUser = User('ana','F',21)

        self.clean_widgets()
        texte=tk.Label(self,
                       text = "Bonjour "+self.currentUser.name+'. Nous aurions besoin d\'en savoir plus sur votre contexte de consommation pour ce repas')
        texte.grid(columnspan=4)

        vals = ['Seul', 'Accompagné']
        etiqs = ['Seul', 'Accompagné']
        varGr_compagnie = tk.StringVar()
        varGr_compagnie.set(vals[1])

        for i in range(2):
            b = tk.Radiobutton(self,
                               variable = varGr_compagnie,
                               text = etiqs[i],
                               value = vals[i],
                               name = 'compagnie'+ vals[i])
            b.grid(row = 2, column = i)

        vals = ['Petit_dejeuner','Déjeuner','Collation','Dîner']
        etiqs = ['Petit-dejeuner', 'Déjeuner','Collation','Dîner']
        varGr_repas = tk.StringVar()
        varGr_repas.set(vals[1])

        for i in range(4):
            b = tk.Radiobutton(self,
                               variable = varGr_repas,
                               text = etiqs[i],
                               value = vals[i],
                               name = 'repas'+vals[i])
            b.grid(row=3,column=i)

        self.val=tk.Button(self,
                       text="Valider",
                       command= lambda:self.propose_repas(varGr_compagnie,varGr_repas))
        self.val.grid(column=0,row=4)

        self.quit = tk.Button(self,
                          text="QUIT",
                          fg="red",
                          command=self.master.destroy)
        self.quit.grid(column=1,row=4)

    def getUpdateData(self, event,_alim):
        """
        Update les valeurs de la liste déroulante des sous-groupes
        event : modif de la valeur sélectionnée pour le groupe
        _alim : aliment du repas considéré par le changement. 
                -> [combobox_grp,combobox_sgrp]
        """
        _alim[1]['values'] = self.category[_alim[0].get()]
    
    def selectbox(self,_row):
        """
        Création Combobox grp et sgrps pour chaque aliment du repas
        _row : numéro de l'aliment dans le repas
                -> int
        """
        data=pd.read_csv(os.path.join('Base_a_analyser','nomenclature.csv'), sep=';',encoding = "ISO-8859-1")
        Lgrps=list(data['libgr'].unique()) #get all groups
        self.category={} #grps et sgrps associés {Alim1:GrpCombo,SgrpCombo}
        for grp in Lgrps:
            self.category[grp]=list(data[data['libgr']==grp]['libsougr'].unique()) #get all sgroups
        
        texte=tk.Label(self,
                       text='Aliment'+str(_row))
        texte.grid(row=_row,column=1)

        GrpCombo = ttk.Combobox(self,
                                values=sorted(list(self.category.keys())),
                                width = 30,
                                state="readonly")
        GrpCombo.grid(row=_row,column=2,padx=5)
        self.grpbox['Alim'+str(_row)]=[]
        self.grpbox['Alim'+str(_row)].append(GrpCombo)
        SgrpCombo = ttk.Combobox(self,
                                 width = 15,
                                 state="readonly")
        SgrpCombo.grid(row=_row,column=3,padx=5)
        self.grpbox['Alim'+str(_row)].append(SgrpCombo)

        GrpCombo.bind('<<ComboboxSelected>>', lambda event,_alim=self.grpbox['Alim'+str(_row)]:self.getUpdateData(event,_alim=self.grpbox['Alim'+str(_row)])) 
        
        self.plus=tk.Button(self,
                       text="+",
                       command= lambda:self.selectbox(_row+1))
        self.plus.grid(column=4,row=_row)
        
    def propose_repas(self,_cie,_repas):
        """
        Affiche autant de combobox qu'il y a d'alims dans le repas
        """
        self.currentUser.compagnie=_cie.get()
        self.currentUser.repas=_repas.get()
        self.grpbox={}
        self.clean_widgets()
        self.selectbox(_row=1)
 
        
        self.val=tk.Button(self,
                       text="Valider",
                       command= lambda:self.currentUser.enter_repas(self.grpbox))
        self.val.grid(column=0,row=30,padx=10,pady=5)

        self.quit = tk.Button(self,
                          text="QUIT",
                          fg="red",
                          command=self.master.destroy)
        self.quit.grid(column=1,row=30,padx=10,pady=5)
       

class User():
    """
    Definit les caractéristiques de l'utilisateur
    """
    def __init__(self,_name,_sex,_age):
        self.name=_name
        self.sex=_sex
        self.age=_age
        
        # Affection de l'utilisateur à un cluster de consommation
        self.affect_cluster()
        


    def affect_cluster(self):
        """
        Permet d'affecter l'utilisateur à un cluster de consommateur
        """
        pass

    def modifier_info(self) :
        """
        Modification d'information si besoin
        """
        pass
    
    def enter_repas(self, _repasEntre):
        """
        _repasEntre : dictionnaire des comboboxs 
                    -> {Alim1: combobox_groupes,combobox_sgroupes}
        renvoie la liste des aliments (sous-groupes) sélectionnées
        """
        self.repasUser=[]
        for alim in _repasEntre:
            self.repasUser.append(_repasEntre[alim][1].get())
        print(self.compagnie,self.repas,self.repasUser)
            
        
class VirtualUser():
    """
    Definit les caractéristiques de l'utilisateur
    """
    def __init__(self,_name,_sex,_age):
        self.name=_name
        self.sex=_sex
        self.age=_age
        
        # Affection de l'utilisateur à un cluster de consommation
        self.affect_cluster()
        
        # Création de la table de préférence individuelle
        self.creation_tab_pref()


    def affect_cluster(self):
        """
        Permet d'affecter l'utilisateur à un cluster de consommateur
        """
        self.cluster = random.randint(0,2)


    def creation_tab_pref(self) :
        """
        La fonction qui crée une table de préférence individuelle des sous-groupes d'aliments
        """
        # Input table de consommation des sous-groupes d'aliments du cluster self.cluster
        conso_cluster = conso_pattern_sougr[conso_pattern_sougr['cluster_consommateur'] == self.cluster]
        
        # Création de table de préférence
        self.tab_pref_indi = pref.construct_table_preference(conso_cluster, nomenclature)
        
        # Personnalisation de table de préférence : ajoute aléatoirement -10 à 10% du taux de consommation par groupe
        self.tab_pref_indi = self.tab_pref_indi.loc[:, ['cluster_consommateur', 'tyrep', 'code_role', 'taux_code_apparaitre', 'libsougr', 'taux_conso_par_code']]
        self.tab_pref_indi['taux_conso_par_code'] = self.tab_pref_indi['taux_conso_par_code'].apply(
                lambda taux : round(taux*(1+random.uniform(-0.1, 0.1)), 2)).apply(
                        lambda taux : taux if taux <= 100 else 100)


    def modifier_info(self) :
        """
        Modification d'information si besoin
        """
        pass
    
    def enter_repas(self, type_repas, avec_qui):
        """
        _repasEntre : dictionnaire des comboboxs 
                    -> {Alim1: combobox_groupes,combobox_sgroupes}
        renvoie la liste des aliments (sous-groupes) sélectionnées
        """
        repas_code = {'petit-dejeuner' : 1, 'dejeuner' : 3, 'gouter' : 4, 'diner' : 5}
        
        input_repas = self.tab_pref_indi[self.tab_pref_indi.tyrep == repas_code[type_repas]]
        
        nbre_plat = 0
        
        while nbre_plat == 0 :
            
            self.repas = input_repas
            
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
#test_user.enter_repas('petit-dejeuner', 'famille')

class Aliments() :
    """
    Fourni la liste des aliments proposés en substitution, scorés
    """
    def __init__(self,_repasEntre):
        self.substitutionsProposées={} #actualise avec les aliments proposés en substitution,
                                        #1 si accepté, 0 sinon


    def calculSubstitution():
        """
        renvoie liste des aliments scorés
        """
        pass

    def proposeSubstituion():
        """
        poids en paramètre
        soit exploitation = Max aliments scorés,
        soit exploration = random Aliments non explorés
        Actualisation des indices de substitution
        Actualisation des poids
        """








root = tk.Tk()
app = Application(master=root)
app.mainloop()
