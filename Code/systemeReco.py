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
import uuid #pour créer des id uniques
import ast
import configparser
from assoc_clust import distances_nid, classif, actualiser_table_clusters



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
        config = configparser.ConfigParser()
        config.read('init.ini')
        self.current_user_id=config['CURRENTUSER']['current_user_id']
   
        
    def menu_widgets(self):
        """
        Menu de la page d'accueil
        """
        self.clean_widgets()
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
                              command=self.quitApp)
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
        
        alim=['fromage','fruits','légumes','poisson','produits laitiers','viande','volaille et gibier']
        alimNam=['from','fruits','legume','poiss','prodLait','viande','volGib']
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
                              command=self.quitApp)
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

        info={}    
        info['name'] = self.nametowidget('nom').get()
        info['age'] = self.nametowidget('age').get()
        info['taille'] = self.nametowidget('taille').get()
        info['poids']=self.nametowidget('poids').get()
        
        widgalim={} #dic des préférénces alimentaires
        for a in _alimNam:
            widgalim[a]=self.nametowidget(a).get()
        info['pref']=widgalim
        info['sexe'] = _sexe.get()
        info['id']=str(uuid.uuid4())
        info['epsilon']=0.5
        info['omega']=0.5
        info['last5subs']=[]  
        info['cluster']='None'

        self.currentUser = User(info)
        

        self.clean_widgets()
        self.menu_widgets()


    def getInfoFromFile(self,_filepath,_section):
        config = configparser.ConfigParser()
        config.read(_filepath)
        info=dict(config._sections[_section])
        return info
        
    def launch(self):
        """
        Formulaire d'info sur le contexte de consommation
        """
        if self.currentUser==None:  #pas de user prédéfini            
            if self.current_user_id=='default': #pas de current User
                info=self.getInfoFromFile('init.ini','DEFAULTDATA')
                            
            else : #user pré-enregistré
                info=self.getInfoFromFile(os.path.join('UserData',self.current_user_id,str(self.current_user_id)+'.ini'),'USERDATA')
        
            self.currentUser = User(info)
                        

        self.clean_widgets()
        texte=tk.Label(self,
                       text = "Bonjour "+self.currentUser.name+'. Nous aurions besoin d\'en savoir plus sur votre contexte de consommation pour ce repas')
        texte.grid(columnspan=4)

        vals = ['seul', 'accompagne']
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
                          command=self.quitApp)
        self.quit.grid(column=1,row=4)
    
    def quitApp(self):
        if self.currentUser!=None:
            self.currentUser.saveUserInfo()
        self.master.destroy()

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
        self.currentUser.contexte={'cluster':self.currentUser.cluster}
        self.currentUser.contexte['compagnie']=_cie.get()
        self.currentUser.contexte['repas']=_repas.get()
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
                          command=self.quitApp)
        self.quit.grid(column=1,row=30,padx=10,pady=5)
        
        
        
    def propose_substitution(self,_repasEntre):
        """
        _repasEntre : dictionnaire des comboboxs 
                    -> {Alim1: combobox_groupes,combobox_sgroupes}
        renvoie la liste des aliments (sous-groupes) sélectionnées
        
        """
        repasLib=[]
        repasCod=[] #[{code groupe, code sous groupe, libellé sous groupe}]
        for alim in _repasEntre:
            repasLib.append((_repasEntre[alim][0].get(),_repasEntre[alim][1].get()))
       
        dataCodesGr=pd.read_csv(os.path.join('Base_a_analyser','nomenclature.csv'), sep=';',encoding = "ISO-8859-1")
        

        for alim in repasLib:
            dicalim={}
            codeGrp=dataCodesGr[dataCodesGr['libgr']==alim[0]]['codgr'].unique()[0]
            codeSgrp=dataCodesGr[dataCodesGr['libsougr']==alim[1]]['sougr'].unique()[0]
            dicalim['codeGrp']=int(codeGrp)
            dicalim['codeSgrp']=int(codeSgrp)
            dicalim['libsougr']=alim[1]
            repasCod.append(dicalim)
        
         
        param=[self.currentUser.epsilon,self.currentUser.omega]
        repas=Aliments(repasCod,
                       self.currentUser.contexte,
                       self.currentUser.dataSubs,
                       param) 
        alimentASubstituer=repas.alimentASubstituer #(libellé sgrp,SAIN,LIM)
        alimentPropose=repas.subsProposee['alimPropose'] #(libellé sgrp,SAIN,LIM)
        
        
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
                       text=str(alimentASubstituer['libsougr'])+
                       '\n'+' Score SAIN : '+
                       str(alimentASubstituer['SAIN'])+
                       '\n'+' Score LIM : '+
                       str(alimentASubstituer['LIM']))
        texte.grid(row=3,column=1,columnspan=4)
        
       
        texte=tk.Label(self,
                       text = 'Nous vous suggérons : ',
                       fg='blue')        
        texte.grid(row=2,column=6,columnspan=4)
        
        texte=tk.Label(self,
                       text=str(alimentPropose['libsougr'])+
                       '\n'+' Score SAIN : '+
                       str(round(alimentPropose['SAIN'],3))+
                       '\n'+' Score LIM : '+
                       str(round(alimentPropose['LIM'],3)))
        texte.grid(row=3,column=6,columnspan=4)
        
        self.buttonAccept= tk.Button(self,
                       text="Accepter",
                       fg='green',
                       command= lambda : repas.acceptation(repas.subsProposee))
        self.buttonAccept.grid(column=1,
                               row=30,
                               padx=10,
                               pady=5)
        
        buttonRefuse= tk.Button(self,
                       text="Refuser",
                       fg='purple',
                       command= lambda : repas.refus(repas.subsProposee))
        buttonRefuse.grid(column=3,
                          row=30,
                          padx=10,
                          pady=5)
        

        


class User():
    """
    Definit les caractéristiques de l'utilisateur
    """
    def __init__(self,_info):
        self.name=_info['name']
        self.sex=_info['sexe']
        self.age=int(_info['age'])
        self.id=_info['id']
        self.taille=int(_info['taille'])
        self.poids=int(_info['poids'])
        self.epsilon=float(_info['epsilon'])
        self.omega=float(_info['omega'])

        
        if type(_info['pref'])==str:
            self.pref=ast.literal_eval(_info['pref']) #conversion en liste
        else:
            self.pref=_info['pref']
            
        if type(_info['last5subs'])==str:
            self.last5subs=ast.literal_eval(_info['last5subs']) #conversion str->dic
        else:
            self.last5subs=_info['last5subs']
        
        
        if _info['cluster']=='None':
            self.get_new_row() #affectation à un cluster
        else:
            self.cluster=_info['cluster']
        
        
        if not os.path.exists('UserData'):
            os.mkdir('UserData')
        self.userdir=(os.path.join('UserData',self.id)) #crée un dossier pour le newUser
        if not os.path.exists(self.userdir): #si n'existe pas de dossier user
            os.mkdir(self.userdir)
            
        if not os.path.exists(os.path.join('UserData',str(self.id),'TabSubstUser.csv')):
            dataSubs=pd.read_csv(os.path.join("Base_Gestion_Systeme","score_par_contextes.csv"), sep=';',encoding = 'ISO-8859-1')
            dataSubs['malus']=False #ajout colonne malus
            dataSubs['Valeur_malus']=1
            dataSubs['Compteur_malus']=0
            dataSubs.to_csv((os.path.join('UserData',str(self.id),'TabSubstUser.csv')), sep=';', encoding='utf-8')
        self.dataSubs=pd.read_csv((os.path.join('UserData',str(self.id),'TabSubstUser.csv')), sep=';',encoding = "utf-8")
      
        
        
        self.saveUserInfo()            
        
        
        # Affection de l'utilisateur à un cluster de consommation
        #self.affect_cluster()
        
    def saveUserInfo(self):
        """
        permet de sauvegarder le fichier ini
        """

        config = configparser.ConfigParser() #sauvegarde des éléments relatifs au user
        config['USERDATA']={
                'id':self.id,
                'name':self.name,
                'age':self.age,
                'sexe':self.sex,
                'taille':self.taille,
                'poids':self.poids,
                'pref':self.pref,
                'cluster':self.cluster,
                'epsilon':self.epsilon,
                'omega':self.omega,
                'last5subs':str(self.last5subs)
                }
        with open(os.path.join(self.userdir,self.id+'.ini'), 'w') as configfile:
            config.write(configfile)
            
            
        config = configparser.ConfigParser() #sauvegarde du fichier init général
        config.read('init.ini')
        config.set('CURRENTUSER','current_user_id',self.id) #actualisation current user
        with open('init.ini', 'w') as configfile:
            config.write(configfile)
            
    
        self.dataSubs.to_csv((os.path.join('UserData',str(self.id),'TabSubstUser.csv')), sep=';', encoding='utf-8')
        
            
    def get_new_row(self):
        """
        """
        if self.sex=="Homme" :
            sexeps = 1 
        sexeps = 2
        tage = classif(self.age, [4,5,6,7,8], [24,34,49,64])
        true_bmi = self.poids / self.taille**2
        bmi = classif(true_bmi, [0,1,2], [18.5, 25])
        [fromages, fruits, legumes,viande, poissons, volaille, ultra_frais] = [classif(i,[0,1],[5]) for i in list(self.pref.values())]
        self.modalites_vect = [sexeps, tage, bmi, fromages, fruits, legumes,viande, poissons,volaille, ultra_frais]
        self.association()

    def association(self):
        """
        df : data_frame
            data frame contenant les valeurs des autres individus (ceux de la table INCA2)
        x_n : vecteur
            contenant les modalités associées au nouvel individu n
        Returns
        -------
        cluster auquel appartient l'individu n
        """
        df= pd.read_csv('clusters_8.csv', sep=',',encoding='latin-1')
        x_n = self.modalites_vect
        df_ss = df.drop(columns=['nomen','clust.num'])
        X = distances_nid(df_ss, x_n,'Gower')
        i = X.index(max(X))
        cluster = df['clust.num'][i]
        actualiser_table_clusters(df,x_n,self.id,cluster)
        self.cluster = cluster


    def modifier_info(self) :
        """
        Modification d'information si besoin
        """
        pass
    


class Aliments() :
    """
    Fourni la liste des aliments proposés en substitution, scorés
    """
    
    def __init__(self,_repasEntre,_contexte,_tabSubst,param,alpha=1.1,beta=1.05):
        """
        _repasEntre :{code grp,code sgrp,libelle sgrp}
        _contexte : {repas:petit-dejeuner, dejeuner, diner,cluster:,compagnie:}
        _tabSubst : dataframe sur lequel on se base pour les scores de subs
        """
        self.contexte=_contexte
        self.dataSubs=_tabSubst
        self.epsilon=param[0]
        self.omega=float(param[1])

        dataNutri=pd.read_csv(os.path.join('Base_Gestion_Systeme','scores_sainlim_ssgroupes.csv'),sep=';',encoding="ISO-8859-1")
        
        self.gamma=0.2 #Malus
        self.alpha=alpha
        self.beta=beta
        self.dataSubs['malus']=False #ajout colonne malus
        self.dataSubs['Valeur_malus']=1#malus à 0 pour tous

        self.dataSubs.loc[self.dataSubs['malus']==True,'Valeur_malus']=self.gamma #actualisation de la valeur du malus
        
        self.NutriScore(_repasEntre,dataNutri)
        
    def NutriScore(self,_repasEntre,dataNutri,indPireScore=0):
     
        repasScore=[] #[(grpAlim1,sgrpAlim1,libAlim1,SAINAlim1,LIMAlim1),...]
        for alim in _repasEntre:    
            scoreSain=dataNutri[(dataNutri['codgr']==alim['codeGrp'])&(dataNutri['sougr']==alim['codeSgrp'])]['SAIN 5 opt'].values[0]
            scoreLim=dataNutri[(dataNutri['codgr']==alim['codeGrp']) & (dataNutri['sougr']==alim['codeSgrp'])]['LIM3'].values[0]
            scoreDist=dataNutri[(dataNutri['codgr']==alim['codeGrp']) & (dataNutri['sougr']==alim['codeSgrp'])]['distance_origine'].values[0]
            alim['SAIN']=round(scoreSain,3)
            alim['LIM']=round(scoreLim,3)
            alim['scoreDist']=round(scoreDist,3)
            repasScore.append(alim)
            

        repasScoreSort=sorted(repasScore,key=lambda alim:alim['scoreDist'],reverse=True) #sort by distance SAIN/LIM

        
# =============================================================================
#       Continuer à prendre le pire, deuxième pire, troisième pire etc mais jusqu'à un certain seuil, 
# i.e tronquer la liste des aliments avec score aliment[0]= seuil
# =============================================================================
        if repasScoreSort[-1]['scoreDist']<80 : #plusieurs aliments potentiellement mauvais
            i=len(repasScoreSort)-1 #dernier aliment
            ListeAlimPropose=[] #liste de tous les aliments pour lesquels on cherche une substitution
                
            while repasScoreSort[i]['scoreDist']<80 and i>=0:
                self.alimentASubstituer=repasScoreSort[i] #(libellé,scoreSAIN,scoreLIM)
                self.calculSubstitution(repasScoreSort,dataNutri)
                ListeAlimPropose.append(self.subsProposee)
                i-=1
            print('listeAlim',ListeAlimPropose)
            self.subsProposee=max(ListeAlimPropose, key = lambda x: x['Score S'])
            self.alimentASubstituer=self.subsProposee['alimASubstituer']
            
                
        else: #on ne substitue que le pire aliment
            self.alimentASubstituer=repasScoreSort[-1] #(libellé,scoreSAIN,scoreLIM)
            self.calculSubstitution(repasScoreSort,dataNutri)
    
    def findSubstitution(self,subData,dataNutri):
        Subst_envisageables=subData[subData['aliment_1']==self.alimentASubstituer['libsougr']][['aliment_2','score_substitution','Valeur_malus','score_sainlim_nor']]       
        Subst_envisageables['S'] = Subst_envisageables['Valeur_malus']*(Subst_envisageables['score_substitution']**self.omega+Subst_envisageables['score_sainlim_nor']**(1-self.omega))
        
        alimPropose=Subst_envisageables.loc[Subst_envisageables['S'].idxmax()]
        nutriAlimPropose=dataNutri[dataNutri['libsougr']==alimPropose['aliment_2']][['libsougr','SAIN 5 opt','LIM3']]
        self.subsProposee={'alimASubstituer':self.alimentASubstituer,
                           'alimPropose':
                               {'libsougr':nutriAlimPropose['libsougr'].values[0],
                                'SAIN':nutriAlimPropose['SAIN 5 opt'].values[0],
                                'LIM' :nutriAlimPropose['LIM3'].values[0]
                                },
                            'Score S':round(alimPropose['S'],4),
                            'NouvelleSubst':False}
    
        print('existe')
        
        return self.subsProposee 
    
        
    def calculSubstitution(self,_repasEntre,dataNutri):
        """
        renvoie liste des aliments scorés
        _repasEntre : 
            list
            liste d'alims ordonnés par score SAIN
        dataNutri :
            pandas df
            pandas df scores alim
        _indPireAlim : 
            int
        poids en paramètre
        soit exploitation = Max aliments scorés,
        soit exploration = random Aliments non explorés
        Actualisation des indices de substitution
        Actualisation des poids
        """
         
# =============================================================================
# Différents niveaux de filtres
# =============================================================================
        #Test existence substitution, filtre = repas,cluster,compagnie
        subData=self.dataSubs[(self.dataSubs['tyrep']==self.contexte['repas'])&(self.dataSubs['cluster']==self.contexte['cluster'])&(self.dataSubs['avecqui']==self.contexte['compagnie'])]
        if not (subData[subData['aliment_1']==self.alimentASubstituer['libsougr']]).dropna(subset=['aliment_2']).empty: 
            self.subsProposee=self.findSubstitution(subData,dataNutri)
            
        else:
            subData=self.dataSubs[(self.dataSubs['tyrep']==self.contexte['repas'])&(self.dataSubs['cluster']==self.contexte['cluster'])&(self.dataSubs['avecqui']=='all')]    
            if not (subData[subData['aliment_1']==self.alimentASubstituer['libsougr']]).dropna(subset=['aliment_2']).empty:
                self.subsProposee=self.findSubstitution(subData,dataNutri)
               
            else:
                subData=self.dataSubs[(self.dataSubs['tyrep']==self.contexte['repas'])&(self.dataSubs['cluster']=='all')&(self.dataSubs['avecqui']=='all')]
                if not (subData[subData['aliment_1']==self.alimentASubstituer['libsougr']]).dropna(subset=['aliment_2']).empty:
                    self.subsProposee=self.findSubstitution(subData,dataNutri)
                    
                else:
                    #Essai substitution du même groupe
                    if (dataNutri[dataNutri['codgr']==self.alimentASubstituer['codeGrp']]).dropna(subset=['libsougr']).shape[0]>1: #si contient autres aliments du mm groupe
                        Subst_secours=dataNutri[(dataNutri['codgr']==self.alimentASubstituer["codeGrp"])&(dataNutri['sougr']!=self.alimentASubstituer['codeSgrp'])]
                        alimPropose=Subst_secours.loc[Subst_secours['distance_origine'].idxmax()] #on prend le max nutritionnel
                        print("alimPropos: ",alimPropose)
                        nutriAlimPropose=dataNutri[dataNutri['libsougr']==alimPropose['libsougr']][['libsougr','SAIN 5 opt','LIM3']]
                        self.subsProposee={'alimASubstituer':self.alimentASubstituer,
                           'alimPropose':
                               {'libsougr':nutriAlimPropose['libsougr'].values[0],
                                'SAIN':nutriAlimPropose['SAIN 5 opt'].values[0],
                                'LIM' :nutriAlimPropose['LIM3'].values[0]
                                },
                            'Score S':0,
                            'NouvelleSubst':True}
                        
                        print('secours')
                    else: #si seul aliment du groupe et aucune substitution possible
                        print('deso on peut rien faire')
                        self.subsProposee={'alimASubstituer':self.alimentASubstituer,
                           'alimPropose':
                               {'libsougr':"Pas mieux",
                                'SAIN':0,
                                'LIM' :0
                                },
                            'Score S':0,
                            'NouvelleSubst':False}

        print(self.epsilon, self.omega)
        #self.subsProposee=('vin', 1.084, 1.430) #test
     
# =============================================================================
# Incorporer ici la notion de epsilon avec exploration/Exploitation
# ajouter dans le dataframe une colonne pour chaque subs proposée
# =============================================================================
    def acceptation(self,_conseq):
        """mise à jour du score avec alpha et beta"""
        print("c'est un oui !!!")
        print(_conseq)
        if _conseq['NouvelleSubst']==True:
            #ajouter subst dans table
            self.ajouter_substition(_conseq)
            pass
        
        Ssubs = self.alpha*self.getSsub()
        self.dataSubs['score_substitution'] = Ssubs
        self.update_beta(_conseq, refus=False)
        self.actualiser_malus(_conseq)
        
        app.menu_widgets()
        
    
    def refus(self,_conseq):
        """mise à jour du score avec alpha et beta"""
        print("dommaaaaaage")
        Ssubs = (1/self.alpha)*self.getSsub()
        self.dataSubs['score_substitution'] = Ssubs
        self.update_beta(_conseq, refus=True)
        self.actualiser_malus(_conseq)
        
        app.menu_widgets()
        pass
    
    def getSsub(self,_conseq):
        repas = self.contexte['repas']
        cluster = self.contexte['cluster']
        compagnie = self.contexte['compagnie']
        series_subs = self.dataSubs.loc[(self.dataSubs['aliment_1']==self)&
                                  (self.dataSubs['aliment_2']==_conseq)&
                                  (self.dataSubs['cluster']==cluster)&
                                  (self.dataSubs['tyrep']==repas)&
                                  (self.dataSubs['avecqui']==compagnie)].values #{repas:petit-dejeuner, dejeuner, diner,cluster:,compagnie:}
        return(series_subs[0])
        
    def update_beta(self,_conseq, refus=True):
        repas = self.contexte['repas']
        cluster = self.contexte['cluster']
        compagnie = self.contexte['compagnie']
        
        #update des antecedents
        coef = self.beta
        if refus :
            coef = 1/self.beta
        
        #antecedents
        ant = self.dataSubs.loc[(self.dataSubs['aliment_1']==self)&
                                (self.dataSubs['cluster']==cluster)&
                                  (self.dataSubs['tyrep']==repas)&
                                  (self.dataSubs['avecqui']==compagnie)]['score_substitution']
        ant = ant*coef
        for i in ant.index:
            self.dataSubs.iloc[i]['score_substitution']= ant[i]
            
        cons = self.dataSubs.loc[(self.dataSubs['aliment_2']==_conseq)&
                                  (self.dataSubs['cluster']==cluster)&
                                  (self.dataSubs['tyrep']==repas)&
                                  (self.dataSubs['avecqui']==compagnie)]['score_substitution']
        cons = cons*coef
        for i in cons.index:
            self.dataSubs.iloc[i]['score_substitution']= cons[i]
            
            
    def ajouter_substition(self,_conseq):
        pass

    
    def actualiser_malus(self,_conseq):
        self.dataSubs.loc[self.dataSubs['aliment_2']==_conseq['alimPropose']['libsougr'],'malus']=True
        self.dataSubs.loc[self.dataSubs['malus']==True,'Compteur_malus']+=1
        self.dataSubs.loc[self.dataSubs['Compteur_malus']>3,'malus']=False #délai dépassé on réinitialise
        self.dataSubs.loc[self.dataSubs['malus']==False,'Compteur_malus']=0 #on réinitialise le compteur
        self.dataSubs.loc[self.dataSubs['malus']==True,'Valeur_malus']=self.gamma #actualisation de la valeur du malus
        
        app.currentUser.dataSubs=self.dataSubs
        
# =============================================================================
# Créer un dataframe Historique de l'utilisateur avec ses repas proposés, 
# son score nutri => On voit l'évolution du score nutri
# =============================================================================
        
# =============================================================================
# Gérer l'actualisation des omegas, à stocker dans le fichier init !
# Avoir un compteur de repas acceptés et refusé : fichier init
# =============================================================================

root = tk.Tk()
app = Application(master=root)
app.mainloop()
