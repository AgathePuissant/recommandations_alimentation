# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""
import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

# La base conso_pattern est préparée par R à partir de la base brute
#conso_pattern_grp = pd.read_csv("conso_pattern_grp.csv", sep = ";", encoding = 'latin-1')
conso_pattern_sougr = pd.read_csv("conso_pattern_sougr.csv",sep = ";", encoding = 'latin-1')
#conso_pattern_sougr.head(3)
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
    

def find_frequent(data, type_repas = 0, categorie = 0, seuil_support = 0.05) :
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
    if type_repas != 0 :
        #data = data[data.tyrep == type_repas]
        data = data[data['tyrep'].isin(type_repas)]
        if categorie != 0 :
            #data = data[data.id_categorie == categorie]
            data = data[data['id_categorie'].isin(categorie)]

    data = data.iloc[:, 3: data.shape[1]-2]
    frequent_itemsets = apriori(data, min_support = seuil_support, use_colnames = True).assign(
            length_item = lambda dataframe: dataframe['itemsets'].map(lambda item: len(item)))
    return frequent_itemsets.sort_values('support', ascending = False)



def supprimer_motifs_inclus(d) :
    ''' prend en entrée un dataframe de sortie de motifs fréquents 
    et supprime les motifs compris dans d'autres motifs.'''

    d = d.sort_index(axis=0)
    
    liste_supp=[]
    
    for i in d['itemsets'] :
        for j in d['itemsets'] :
            if d.loc[d['itemsets']==i].index[0]!=d.loc[d['itemsets']==j].index[0] :
                if i.issubset(j) :
                    liste_supp.append(d.index[d.loc[d['itemsets']==i].index[0]])
                elif j.issubset(i) :
                    liste_supp.append(d.index[d.loc[d['itemsets']==j].index[0]])
         
    liste_supp=np.unique(liste_supp)
              
    d=d.drop(d.index[liste_supp])
    
    return d



def differe_de_1(d) :
    """
     prend en entrée un dataframe de sortie de motifs fréquents 
    et renvoie une liste de listes contenant :
         - La liste des aliments composant le contexte alimentaire
         - La liste contenant les 2 éléments potentiellement substituables 
         i.e. qui sont consommés dans le même contexte alimentaire
    """

    couples=[]

    for i in d['itemsets'] :
        for j in d['itemsets'] :
            if d.loc[d['itemsets']==i].index[0]!=d.loc[d['itemsets']==j].index[0] :
            #Génère chaque couple en double (dans un sens et dans l'autre)
                new_1=i.difference(j)
                new_2=j.difference(i)
                
                if len(new_1)==1 and len(new_2)==1:
                    
                    couples.append([list(i.difference(new_1.union(new_2))),[list(new_1)[0],list(new_2)[0]]])
                    
    return couples



def substituabilite(d,nomenclature):
    """
    Prend en entrée le résultat de differe_de_1 et renvoie une liste du même 
    type ne comprenant que des couples d'aliments réellement substituables, i.e.
    qui ont la même fonction dans le repas (selon la base role_repas)
    """
    
    motifs_sub = []
    
    for motif in d:
        couple = motif[1]
        role = []
        for rang in range(len(nomenclature)):
            if nomenclature["libsougr"][rang] == couple[0] or nomenclature["libsougr"][rang] == couple[1]: 
            #if nomenclature["codsougr"][rang] == couple[0] or nomenclature["codsougr"][rang] == couple[1]:
                role.append(nomenclature["codrole"][rang])
        
        if role[0] == role[1]:
            motifs_sub.append(motif)
            
    return motifs_sub

def regles_association(d,confiance) :
    """
    Prend en entrée un dataframe de motifs fréquents et renvoie un dataframe des
    règles d'association à un conséquent
    """
    
    rules=association_rules(d, metric="confidence", min_threshold=confiance)

    rules["consequents_len"] = rules["consequents"].apply(lambda x: len(x))
    
    rules=rules[(rules["consequents_len"]==1)]
    
    rules=rules.set_index(pd.Index([i for i in range(len(rules))]))
    
    return rules

def tableau_substitution(rules) :
    """
    Prend en entrée un dataframe des règles d'association et ressort
    le tableau des aliments sustituables en fonction du contexte alimentaire
    """
    table_association=[]

    for ligne in range (len(rules)) :
        
        aliments_subst=rules["consequents"][ligne]
        
        for ligne_comp in range(len(rules)) :
            
            if ligne!=ligne_comp :
                
                if rules["antecedents"][ligne].issubset(rules["antecedents"][ligne_comp]) and rules["antecedents"][ligne].issuperset(rules["antecedents"][ligne_comp]) :
                    
                    aliments_subst=aliments_subst.union(rules["consequents"][ligne_comp])
                    
        table_association.append([rules["antecedents"][ligne],aliments_subst])
        
    df_association=pd.DataFrame(table_association,columns=["Contexte alimentaire","Aliments substituables"])
    df_association=df_association.drop_duplicates()
    
    return df_association
  
        


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
CODE PRINCIPAL
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
            
       
nomenclature = modif_nomenclature(nomenclature)
#Que les adultes, que le déjeuner et le dîner    
d = find_frequent(conso_pattern_sougr,[3,5],[1,3,4,5,7,8],seuil_support=0.01)
#d = supprimer_motifs_inclus(d)
#d = differe_de_1(d)
#d = substituabilite(d,nomenclature)

d=regles_association(d,0)

d=tableau_substitution(d)

print(d)

