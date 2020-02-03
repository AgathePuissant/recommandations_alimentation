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
                        text="Bienvenue",
                        fg='blue')
        texte2.grid(columnspan=5)


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
        
        s_taille=tk.Scale(self, label='Taille (cm)', name='taille',
                 from_=70, to=250,
                 orient=tk.HORIZONTAL,
                 length=200)
        s_taille.grid(row=4,column=0)
        
        s_poids=tk.Scale(self, label='Poids (kg)', name='poids',
                 from_=30, to=200,
                 orient=tk.HORIZONTAL,
                 length=200)
        s_poids.grid(row=4,column=1)
        
        textePref=tk.Label(self,
                        text="A quel point aimez-vous les aliments ci-dessous",
                        fg='blue')
        textePref.grid(columnspan=3,padx=5)
        
        alim=['fromage','fruits','légumes','viande','poisson','volaille et gibier','produits laitiers']
        alimNam=['from','fruits','legume','viande','poiss','volGib','prodLait']
        _row=6
        for c, v in enumerate(alim):
            s_pref=tk.Scale(self, label=v, name=alimNam[c],
                 from_=0, to=10,
                 orient=tk.HORIZONTAL,
                 length=200)
            if c%2==0:
                 s_pref.grid(row=_row,column=0)
            else :
                s_pref.grid(row=_row,column=1)
                _row+=1


        #print(self.winfo_children()) #list of widgets

        self.quit = tk.Button(self,
                              text="QUIT",
                              fg="red",
                              command=self.master.destroy)
        self.quit.grid(column=1,row=15)


        self.val=tk.Button(self,
                           text="Valider",
                           command= lambda:self.newUser(varGr,alimNam))
        self.val.grid(column=0,row=15)


    def newUser(self, _sexe,_alimNam):
        """
        Récup des infos sur le formulaire, 
        création d'une instance de la classe user
        _sexe=scrollbar sexe
        _aliNam=scrollbar préférences alimentaires
        """

        name = self.nametowidget('nom').get()
        age = self.nametowidget('age').get()
        widgalim={} #dic des préférénces alimentaires
        for a in _alimNam:
            widgalim[a]=self.nametowidget(a).get()
        sexe = _sexe.get()

        print(name,age,sexe,widgalim)

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

        vals = ['petit-dejeuner','dejeuner','collation','diner']
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
        _alim[1].current(0)
    
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
                       command= lambda : self.propose_substitution(_repasEntre=self.grpbox))
        self.val.grid(column=0,row=30,padx=10,pady=5)

        self.quit = tk.Button(self,
                          text="QUIT",
                          fg="red",
                          command=self.master.destroy)
        self.quit.grid(column=1,row=30,padx=10,pady=5)
        
        
        
    def propose_substitution(self,_repasEntre):
        """
        _repasEntre : dictionnaire des comboboxs 
                    -> {Alim1: combobox_groupes,combobox_sgroupes}
        renvoie la liste des aliments (sous-groupes) sélectionnées
        
        """
        repasLib=[]
        repasCod=[] #[code groupe, code sous groupe, libellé sous groupe]
        for alim in _repasEntre:
            repasLib.append((_repasEntre[alim][0].get(),_repasEntre[alim][1].get()))
       
        dataCodesGr=pd.read_csv(os.path.join('Base_a_analyser','nomenclature.csv'), sep=';',encoding = "ISO-8859-1")
        

        for alim in repasLib:
            codeGrp=dataCodesGr[dataCodesGr['libgr']==alim[0]]['codgr'].unique()[0]
            codeSgrp=dataCodesGr[dataCodesGr['libsougr']==alim[1]]['sougr'].unique()[0]
            repasCod.append((int(codeGrp),int(codeSgrp),alim[1]))
        
        repas=Aliments(repasCod,self.currentUser.repas) 
        alimentASubstituer=repas.alimentASubstituer #(libellé sgrp,SAIN,LIM)
        alimentPropose=repas.subsProposee #(libellé sgrp,SAIN,LIM)
        
        print(alimentASubstituer, alimentPropose)
        self.clean_widgets()
        
        texte=tk.Label(self,
                       text = "Nous vous proposons cette substitution :",
                       fg='blue')
        texte.grid(column=1,columnspan=6)
        
        texte=tk.Label(self,
                       text = 'Vous voulez consommer : ',
                       fg='blue')
        texte.grid(row=2,column=1,columnspan=4)
        
        texte=tk.Label(self,
                       text=str(alimentASubstituer[0])+'\n'+' Score SAIN : '+str(alimentASubstituer[1])+'\n'+' Score LIM : '+str(alimentASubstituer[2]))
        texte.grid(row=3,column=1,columnspan=4)
        
       
        texte=tk.Label(self,
                       text = 'Nous vous suggérons : ',
                       fg='blue')        
        texte.grid(row=2,column=6,columnspan=4)
        
        texte=tk.Label(self,
                       text=str(alimentPropose[0])+'\n'+' Score SAIN : '+str(alimentPropose[1])+'\n'+' Score LIM : '+str(alimentPropose[2]))
        texte.grid(row=3,column=6,columnspan=4)
        
        self.buttonAccept= tk.Button(self,
                       text="Accepter",
                       fg='green',
                       command= lambda : repas.acceptation(alimentASubstituer,alimentPropose))
        self.buttonAccept.grid(column=1,
                               row=30,
                               padx=10,
                               pady=5)
        
        buttonRefuse= tk.Button(self,
                       text="Refuser",
                       fg='purple',
                       command= lambda : repas.refus(alimentASubstituer,alimentPropose))
        buttonRefuse.grid(column=3,
                          row=30,
                          padx=10,
                          pady=5)
        


class User():
    """
    Definit les caractéristiques de l'utilisateur
    """
    def __init__(self,_name,_sex,_age):
        self.name=_name
        self.sex=_sex
        self.age=_age
        
        # Affection de l'utilisateur à un cluster de consommation
        #self.affect_cluster()
        
        
    def get_new_row(nouveau_client, modalites):
        """

        Parameters
        ----------
        nouveau_client : list
            Avec le numéro associé à sa modalité.
            Par exemple, dans ce cas on a 10 variables :
            nouveau_client = [2,4,1,0,1,1,0,1,0,0]
            le sexe du nouveau client est associé a la modalité 2
            la classe d'age est 4 donc 18-24 ans
            sa bmi est normale
            etc....
                
        modalites : list
            Dans notre cas 
            modalites = [3,8,3,2,2,2,2,2,2,2]
            car on a :  3 mods pour sexe
                        8 mods pour la classe d'age
                        3 mods pour la bmi
                        2 mods pour les 7 préférences alim qui nous intéressent
        
        Returns 
        -------
        new_row : list
            sous le format voulu pour affect_cluster
            une liste avec 28 éléments avec un 1 là où sa modalité se trouve
            exemple :
                [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1,0, 1, 1, 0, 0, 1]
                     sex                    tage      bmi from fruits..................viand....vol

        """
        n = len(modalites)
        new_row = []
        for i in range(n) :
            l = [0 for j in range(modalites[i])]
            l[nouveau_client[i]] = 1
            new_row += l
        return(new_row)

    def affect_cluster(cluster_data, new_row_bf, modalites) :
        """
        Parameters
        ----------
        cluster_data : numpy array
            tableau avec les poids de chaque modalité pour chaque cluster
        
        new_row_bf : list
            Avec le numéro associé à sa modalité.
            Par exemple, dans ce cas on a 10 variables :
            nouveau_client = [2,4,1,0,1,1,0,1,0,0]
            le sexe du nouveau client est associé a la modalité 2
            la classe d'age est 4 donc 18-24 ans
            sa bmi est normale
            etc....
            
        modalites : list
            Dans notre cas 
            modalites = [3,8,3,2,2,2,2,2,2,2]
            car on a :  3 mods pour sexe
                        8 mods pour la classe d'age
                        3 mods pour la bmi
                        2 mods pour les 7 préférences alim qui nous intéressent
        

        Returns 
        -------
            cluster : int numero du cluster auquel le nouveau client est associé
            

        """
        new_row = get_new_row(new_row_bf, modalites)
        liste = []
        dim = cluster_data.shape
        for i in range(dim[1]):
            x = new_row - cluster_data[:,i]
            liste+=[math.sqrt(sum(abs(x)))]
            minim = min(liste)
        cluster = liste.index(minim)+1
        return (cluster)


    def modifier_info(self) :
        """
        Modification d'information si besoin
        """
        pass
    


class Aliments() :
    """
    Fourni la liste des aliments proposés en substitution, scorés
    """
    
    def __init__(self,_repasEntre,_repas):
        """
        _repasEntre : [(code grp,code sgrp,libelle sgrp)]
        _repas : petit-dejeuner, dejeuner, diner
        """
        self.repas=_repas
        self.NutriScore(_repasEntre)
        
        print(self.repas)
        
        
    def NutriScore(self,_repasEntre):

        dataNutri=pd.read_csv('scores_sainlim_ssgroupes.csv',sep=';',encoding="ISO-8859-1")
        
        repasScore=[]
        for alim in _repasEntre:    
            scoreSain=dataNutri[(dataNutri['codgr']==alim[0])&(dataNutri['sougr']==alim[1])]['SAIN 5 opt'].values[0]
            scoreLim=dataNutri[(dataNutri['codgr']==alim[0]) & (dataNutri['sougr']==alim[1])]['LIM3'].values[0]
            repasScore.append((alim[0],alim[1],alim[2],round(scoreSain,3),round(scoreLim,3)))
        
        LSain=[repasScore[i][1] for i in range(len(repasScore))]
        pireScore=LSain.index(min(LSain))
        pireAlim=repasScore[pireScore]
        self.alimentASubstituer=pireAlim #(libellé,scoreSAIN,scoreLIM)
        self.calculSubstitution(pireAlim)
        
    def calculSubstitution(self,_pireAlim,epsilon=0,omega1=0.5,omega2=0.5,dataNutri):
        """
        renvoie liste des aliments scorés
        _pireAlim : (labelSgrp,scoreSAIN,scoreLIM)
        _alimproposé : (labelSgrp,scoreSAIN,scoreLIM)
        
        poids en paramètre
        soit exploitation = Max aliments scorés,
        soit exploration = random Aliments non explorés
        Actualisation des indices de substitution
        Actualisation des poids
        """
        print(self.repas)
        print(_pireAlim[2])
        self.dataSubs=pd.read_csv('scores_tous_contextes_v3.csv', sep=',',encoding = "utf-8",index_col=0)
        Subst_envisageables=self.dataSubs[(self.dataSubs['repas']==self.repas)&(self.dataSubs['aliment_1']==_pireAlim[2])][['aliment_2','score']]
        Subst_envisageables 
        
        
        #Si pas de substitution
        Subst_secours=dataNutri[(dataNutri['codgr']==_pireAlim[0])
        Subst_secours
        
        
        
        
        
        self.subsProposee=('vin', 1.084, 1.430) #test
     
    def acceptation(self,_antec,_conseq):
        print("c'est un oui !!!")
        self.dataSubs
        pass
    
    def refus(self,_antec,_conseq):
        print("dommaaaaaage")
        pass
      

root = tk.Tk()
app = Application(master=root)
app.mainloop()
