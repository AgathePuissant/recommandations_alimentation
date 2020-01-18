import numpy as np

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