# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 14:39:43 2020

@author: anael
"""

import tkinter as tk
import pandas as pd


class Application(tk.Frame):
    def __init__(self, master=None):
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
        for widget in self.winfo_children():
            widget.destroy()

    def getnew(self):
        
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
        print("ok")
    
        name=self.nametowidget('nom').get()
        age=self.nametowidget('age').get()
        sexe=_sexe.get()
        
        print(name,age,sexe)
       
        self.currentUser=user(name,sexe,age)
        self.clean_widgets()
        self.menu_widgets()
    
        
    
    def launch(self):
        """Lance la suggestion de repas"""
        if self.currentUser!=None:
            self.clean_widgets()
            texte=tk.Label(self, 
                           text="Bonjour "+self.currentUser.name+'. Nous aurions besoin d\'en savoir plus sur votre contexte de consommation pour ce repas')
            texte.grid()
            
            vals = ['S','A']
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
            
            vals = ['M','L','B','D']
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
                           command= lambda:self.currentUser.propose_repas(varGr_compagnie,varGr_repas))        
            self.val.grid(column=0,row=4)
                
            self.quit = tk.Button(self, 
                              text="QUIT", 
                              fg="red",
                              command=self.master.destroy)
            self.quit.grid(column=1,row=4)
            
            

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
        pass
    
    
    def propose_repas(self,_cie,_repas):
        """
        Entre le contexte
        Propose une liste d'aliments
        """
        cie=_cie.get()
        repas=_repas.get()
        print(cie,repas)
        suggestion=Aliments()


class Aliments():
    """
    Fourni la liste des aliments proposés en substitution, scorés
    """
    def __init__(self):
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
  