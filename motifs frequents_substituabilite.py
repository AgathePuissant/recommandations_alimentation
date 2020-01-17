# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""
import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import apriori, fpgrowth, fpmax
from mlxtend.frequent_patterns import association_rules
import pickle

# La base conso_pattern est préparée par R à partir de la base brute
#conso_pattern_grp = pd.read_csv("conso_pattern_grp.csv", sep = ";", encoding = 'latin-1')
conso_pattern_sougr = pd.read_csv("conso_pattern_sougr.csv",sep = ";", encoding = 'latin-1')
nomenclature = pd.read_csv("Nomenclature_3.csv",sep = ";",encoding = 'latin-1')
nomenclature.head(3)



def modif_nomenclature(nomenclature):
    """
    Modifie la table nomenclature pour qu'elle soit utilisable dans la fonction
    substituabilité
    i.e. garde une ligne par sous-groupe, renomme les "sans" et créé le code des sous-groupes
    """
    
    codsougr = [11]
    nomenclature = nomenclature.iloc[:, 0:5]
    ref = nomenclature['libsougr'][0]

    for rang in range(1,len(nomenclature)):
        #Renomme les sous-groupes "sans" dans la table par le nom du groupe
        if nomenclature['libsougr'][rang] == 'sans':
            nomenclature['libsougr'][rang] = nomenclature['libgr'][rang]
            #Renomérote les codes 99 des sous-groupes par 0
            nomenclature['sougr'][rang] = 0
        
        #Supprime les lignes redondantes 
        if nomenclature['libsougr'][rang] == ref:
            nomenclature = nomenclature.drop(rang)
            
        else:
            ref = nomenclature['libsougr'][rang]
            #Créé le code des sous-groupes en concaténant le code du groupe et du sous-groupe existant
            codsougr.append(int(str(nomenclature['codgr'][rang])+str(nomenclature['sougr'][rang])))
    
    nomenclature['codsougr'] = codsougr
    
    #Renumérote les indexs des lignes
    for i in range(len(nomenclature)) :
        nomenclature = nomenclature.rename(index = {nomenclature.index[i]:i})

    return nomenclature
    

def find_frequent(conso_data, type_repas = 0, avec_qui = 0, categorie = 0, seuil_support = 0.05, algo = 'apriori') :
    """
    La fonction qui à partir de la base conso_pattern préparée par R, retourne la base de motif fréquent avec le support
    
    1, data : conso_pattern -- data.frame
    2, type_repas :
        0 on prend tous les repas ; 1 petit-déjeuner ; 2 collation matin
        3 déjeuner ; 4 collation après-midi ; 5 diner ; 6 collation soir -- list
    3, categorie :
        0 : On prend tous les catégories
        Homme : 1 adulte (36-60) ; 2 enfant (0-17) ; 3 jeune adulte (18-35) ; 4 personne âgée (> 60)
        Femme : 5 adulte (36-60) ; 6 enfant (0-17) ; 7 jeune adulte (18-35) ; 8 personne âgée (> 60) -- list
    4, seuil_support : la valeur minimale du support à passer dans la fonction mlxtend.frequent_patterns.apriori -- float

    """

    data=conso_data.copy()
    
    if type_repas != 0 :
        #data = data[data.tyrep == type_repas]
        data = data[data['tyrep'].isin(type_repas)]
        
    if avec_qui != 0 :
        data = data[data['avecqui'].isin(avec_qui)]
        
    if categorie != 0 :
        #data = data[data.id_categorie == categorie]
        data = data[data['id_categorie'].isin(categorie)]
        
    del data['tyrep']
    del data['nomen']
    del data['avecqui']
    del data['nojour']
    del data['id_categorie']
    del data['cluster_consommateur']
        
    
    

    if algo == 'apriori' :
        frequent_itemsets = apriori(data, min_support = seuil_support, use_colnames = True).assign(
            length_item = lambda dataframe: dataframe['itemsets'].map(lambda item: len(item)))
    elif algo == 'fpgrowth' :
        frequent_itemsets = fpgrowth(data, min_support = seuil_support, use_colnames=True).assign(
            length_item = lambda dataframe: dataframe['itemsets'].map(lambda item: len(item)))
    elif algo == 'fpmax' :
        frequent_itemsets = fpmax(data, min_support = seuil_support, use_colnames=True).assign(
            length_item = lambda dataframe: dataframe['itemsets'].map(lambda item: len(item)))
        
    
    return frequent_itemsets.sort_values('support', ascending = False)


def regles_association(d,confiance=0.5,support_only=False,support=0.1,contexte_maximaux=True) :
    """
    Prend en entrée un dataframe de motifs fréquents et renvoie un dataframe des
    règles d'association à un conséquent et qui supprime les motifs inclus
    """
    if support_only==False :
        rules=association_rules(d, metric="confidence", min_threshold=confiance)
    else :
        rules=association_rules(d, support_only=True, min_threshold=0.01)

    rules["consequents_len"] = rules["consequents"].apply(lambda x: len(x))
    
    rules["antecedents_len"] = rules["antecedents"].apply(lambda x: len(x))
    
    rules=rules[(rules["consequents_len"]==1)]
    
    rules.sort_values('antecedents_len', ascending = False)
    
    rules=rules.set_index(pd.Index([i for i in range(len(rules))]))
    
    print(len(rules))
    
            
    #C'est ça qui prend du temps
#    
    if contexte_maximaux==True :
        
        
        N=len(rules)
        
        for i in range(N) :
            
            if i%100==0 :
                print(i)
            
            if i in rules.index :
                
                liste_supp=[]
                
                for j in range(len(rules)) :
                    
                    if rules["consequents"][i]==rules["consequents"][j] and rules["antecedents"][i].issuperset(rules["antecedents"][j]) and i!=j:
                        
                        liste_supp.append(j)
                    
                rules.drop(liste_supp, inplace=True)
                
#                if liste_supp!=[] :
#                    print("nouvelle longueur : "+str(len(rules)))
                
                rules=rules.set_index(pd.Index([i for i in range(len(rules))]))
    
    return rules

def tableau_substitution(rules_original) :
    """
    Prend en entrée un dataframe des règles d'association et ressort
    le tableau des aliments sustituables en fonction du contexte alimentaire
    """
    
    rules = rules_original.copy()
    
    
    N=len(rules)
    
    liste_pas_class=frozenset(['seul','amis','famille','autre','cluster_0','cluster_1','cluster_2','petit-dejeuner','dejeuner','gouter','diner'])
        
    for i in range(N) :
        
        if i in rules.index :
            
            liste_supp=[]
            
            if rules['consequents'][i].intersection(liste_pas_class)==frozenset() :
            
                for j in range(len(rules)) :
                    
                    if rules["antecedents"][i]==rules["antecedents"][j] and i!=j and rules['consequents'][j].intersection(liste_pas_class)==frozenset() :
                        
                        if (nomenclature[(nomenclature["libsougr"]==list(rules["consequents"][i])[0])]["codrole"]).all()==(nomenclature[(nomenclature["libsougr"]==list(rules["consequents"][j])[0])]["codrole"]).all() :
                        
                            liste_supp.append(j)
                        
                            rules["consequents"][i]=rules["consequents"][i].union(rules["consequents"][j])
                            
                            if type(rules["confidence"][i])==list :
                                rules["confidence"][i].append(rules["confidence"][j])
                            else :
                                rules["confidence"][i]=[rules["confidence"][i],rules["confidence"][j]]
                            
                    elif rules['consequents'][j].intersection(liste_pas_class)!=frozenset() :
                        
                        liste_supp.append(j)
                    
            else :
                liste_supp.append(i)
                
            rules.drop(liste_supp, inplace=True)
            
            rules=rules.set_index(pd.Index([i for i in range(len(rules))]))
    return rules
  
        
def score_biblio(aliment_1,aliment_2,regles_original) :
    '''
    Fonction qui prend en entrée les 2 aliments dont on veut trouver le score de substituabilité et les règles d'associations entre aliments,
    et ressort le score de substituabilité calculé selon le score trouvé dans la bibliographie.
    ---------------
    Variables d'entrée :
        -aliment_1 : frozenset de longueur 1
        -aliment_2 : frozenset de longueur 1
        -regles_original : dataFrame contenant les règles d'association entre aliments et contextes alimentaires
    '''
    
    regles=regles_original[(regles_original["consequents"]==aliment_1) | (regles_original["consequents"]==aliment_2)]
    regles=regles.set_index(pd.Index([i for i in range(len(regles))]))
    
    
    x_inter_y=0
    x_union_y=len(regles)
    A_x_y=0
    A_y_x=0
    
    
    
    for i in range(len(regles["antecedents"])) :
        
        
        if regles["consequents"][i]==aliment_1 :
            
            contexte_1=regles["antecedents"][i]
            
            if aliment_2 in contexte_1 :
                A_x_y+=1
            
            for j in range(len(regles["antecedents"])) :
                
                if i!=j and regles["consequents"][j]==aliment_2 :
                    contexte_2=regles["antecedents"][j]
                    
                    if aliment_1 in contexte_2 :
                        A_y_x+=1
                        
                    if contexte_2.issubset(contexte_1) and contexte_2.issuperset(contexte_1) and contexte_1.issubset(contexte_2) and contexte_1.issuperset(contexte_2) :
                        x_inter_y+=1
                    
    return(x_inter_y/(x_union_y+A_x_y+A_y_x))
    

def matrice_scores(tableau,regles) :

    t_scores=pd.DataFrame(columns=["Couples","Score confiance","Score biblio"])
    
    
    for i in range(len(tableau)) :
        if len(tableau["consequents"][i])>1 :
            for j in range(len(tableau["consequents"][i])) :
                aliment_1=tableau["consequents"][i][j]
                for k in range(len(tableau["consequents"][i])) :
                    if j!=k :
                        aliment_2=tableau["consequents"][i][k]
                        
                        if len(t_scores[t_scores["Couples"]== aliment_1+" vers "+aliment_2])==0:
                            t_scores.loc[i]=[aliment_1+" vers "+aliment_2,[tableau["confidence"][i][j]-tableau["confidence"][i][k]],score_biblio(frozenset([aliment_1]),frozenset([aliment_2]),regles)]
                        else :
                            t_scores.loc[t_scores["Couples"] == aliment_1+" vers "+aliment_2]["Score confiance"].values[0].append(tableau["confidence"][i][j]-tableau["confidence"][i][k])

    t_scores["Score confiance"]=t_scores["Score confiance"].apply(lambda x : np.mean(x))
    
    t_scores["Score combiné"]=t_scores["Score biblio"]+t_scores["Score confiance"]
    
    return t_scores
            
def transfo_mod(d) :
    
    d['petit-dejeuner']=[0]*len(d)
    d['dejeuner']=[0]*len(d)
    d['gouter']=[0]*len(d)
    d['diner']=[0]*len(d)
    
    d['seul']=[0]*len(d)
    d['famille']=[0]*len(d)
    d['amis']=[0]*len(d)
    d['autre']=[0]*len(d)
    
    d['cluster_0']=[0]*len(d)
    d['cluster_1']=[0]*len(d)
    d['cluster_2']=[0]*len(d)
    
    
    for i in range(len(conso_pattern_sougr)) :
        
        if d['tyrep'][i]==1 :
            d['petit-dejeuner'][i]=1
        elif d['tyrep'][i]==3 :
            d['dejeuner'][i]=1
        elif d['tyrep'][i]==4 :
            d['gouter'][i]=1
        elif d['tyrep'][i]==5 :
            d['diner'][i]=1
            
        if d['avecqui'][i]==1 :
            d['seul'][i]=1
        elif d['avecqui'][i]==2 :
            d['famille'][i]=1
        elif d['avecqui'][i]==3 :
            d['amis'][i]=1
        elif d['avecqui'][i]==4 :
            d['autre'][i]=1
            
        if d['cluster_consommateur'][i]==0 :
            d['cluster_0'][i]=1
        elif d['cluster_consommateur'][i]==1 :
            d['cluster_1'][i]=1
        elif d['cluster_consommateur'][i]==2 :
            d['cluster_2'][i]=1
            
    return d
            
    
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
CODE PRINCIPAL
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
            
repas=0
avecqui=0
consommateur=0
supp=0.01
conf=0.1

conso_pattern_sougr=transfo_mod(conso_pattern_sougr)
       
nomenclature = modif_nomenclature(nomenclature)

#Que les adultes, que le déjeuner et le dîner  
  
motifs = find_frequent(conso_pattern_sougr,repas,avecqui,consommateur,seuil_support=supp, algo='fpgrowth')

regles = regles_association(motifs,confiance = conf)
##
t_subst = tableau_substitution(regles)
##
#scores = matrice_scores(t_subst,regles)




#modalites_avecqui = np.unique(conso_pattern_sougr["avecqui"].dropna())
#modalites_tyrep = np.unique(conso_pattern_sougr["tyrep"].dropna())
#
#for repas in modalites_tyrep :
#    
#    for avecqui in modalites_avecqui :
#        
#        d = find_frequent(conso_pattern_sougr, [repas], [avecqui], [1,3,4,5,7,8], seuil_support=0.01, algo='fpgrowth')
#        print("Motifs fréquents trouvés")
#        d=regles_association(d,0.3)
#        print("Règles d'association trouvées")
#        d=tableau_substitution(d)
#        print("tableau_substitution_"+str(repas)+"_"+str(avecqui)+"_supp=0,5_conf=0,5")
#            
#        pickle.dump(d,open("tableau_substitution_"+str(repas)+"_"+str(avecqui)+"_supp=0,5_conf=0,5","wb"))
#            
