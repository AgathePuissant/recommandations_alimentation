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
        self.pack()
        self.create_widgets()
        self.currentUser=None

    def create_widgets(self):
        self.BnewUser = tk.Button(self,
                                  text='Nouvel utilisateur',
                                  command=self.getnew)
        self.BnewUser.pack()
        
        self.Blaunch=tk.Button(self,
                              text='Proposer repas',
                              command=self.launch)
        self.Blaunch.pack()
                                  
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def getnew(self):
        print("Nouvel utilisateur")
        for widget in self.winfo_children():
            widget.destroy()
        texte2=tk.Label(self, text="A midi j'ai mangé de la chantilly")
        texte2.pack()
        
        criteresCluster=['nom', 'sexe', 'age']
        
        for line, item in enumerate(criteresCluster):
             l = tk.Label(self, text=item, width=10)
             e = tk.Entry(self, width=10,name=item)
             l.pack()
             e.pack()
        
        
        self.quit = tk.Button(self, 
                              text="QUIT", 
                              fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")
        
        self.val=tk.Button(self,
                           text="Valider",
                           command=self.newUser)
        self.val.pack()
        
        
    def newUser(self):
        print("ok")

        for widget in self.winfo_children():
            widget.destroy()
            
        self.currentUser=user("Ana","F",21)
    
        
    
    def launch(self):
        """Lance la suggestion de repas"""
        if self.currentUser!=None:
            self.currentUser.propose_repas()

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
    
    
    def propose_repas(self):
        """
        Entre le contexte
        Propose une liste d'aliments
        """
        print("bouffe")
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
  