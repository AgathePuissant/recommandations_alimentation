# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 14:39:43 2020

@author: anael
"""

import tkinter as tk
from tkinter import ttk
import pandas as pd
import os


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


    def newUser(self,_sexe):
        """
        Récup des infos sur le formualire, 
        création d'une instance de la classe user
        """

        name=self.nametowidget('nom').get()
        age=self.nametowidget('age').get()
        sexe=_sexe.get()

        print(name,age,sexe)

        self.currentUser=user(name,sexe,age)
        self.clean_widgets()
        self.menu_widgets()



    def launch(self):
        """
        Formulaire d'info sur le contexte de consommation
        """
        if self.currentUser==None:
            self.currentUser=user('ana','F',21)

        self.clean_widgets()
        texte=tk.Label(self,
                       text="Bonjour "+self.currentUser.name+'. Nous aurions besoin d\'en savoir plus sur votre contexte de consommation pour ce repas')
        texte.grid(columnspan=4)

        vals = ['Seul','Accompagné']
        etiqs = ['Seul', 'Accompagné']
        varGr_compagnie = tk.StringVar()
        varGr_compagnie.set(vals[1])

        for i in range(2):
            b = tk.Radiobutton(self,
                               variable=varGr_compagnie,
                               text=etiqs[i],
                               value=vals[i],
                               name='compagnie'+vals[i])
            b.grid(row=2,column=i)

        vals = ['Petit_dejeuner','Déjeuner','Collation','Dîner']
        etiqs = ['Petit-dejeuner', 'Déjeuner','Collation','Dîner']
        varGr_repas = tk.StringVar()
        varGr_repas.set(vals[1])

        for i in range(4):
            b = tk.Radiobutton(self,
                               variable=varGr_repas,
                               text=etiqs[i],
                               value=vals[i],
                               name='repas'+vals[i])
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
       



class user():
    """
    Definit les caractéristiques de l'utilisateur
    """
    def __init__(self,_name,_sex,_age):
        self.name=_name
        self.sex=_sex
        self.age=_age


    def affect_cluster(self):
        """
        Permet d'affecter l'utilisateur à un cluster de consommateur
        """
        self.cluster = 0

    def modifier_info(self) :
        """
        Modification d'information si besoin
        """
        pass
    
    def enter_repas(self,_repasEntre):
        """
        _repasEntre : dictionnaire des comboboxs 
                    -> {Alim1: combobox_groupes,combobox_sgroupes}
        renvoie la liste des aliments (sous-groupes) sélectionnées
        """
        self.repasUser=[]
        for alim in _repasEntre:
            self.repasUser.append(_repasEntre[alim][1].get())
        print(self.compagnie,self.repas,self.repasUser)



class Aliments():
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
