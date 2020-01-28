# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 11:21:31 2020

@author: agaca
"""

def rule_overlap(R1,R2) :
    '''
    Fonction de calcul de la métrique de recouvrement entre deux sets de règles d'association.
    --------------
        - R1, R2 : DataFrame de règles d'association obtenus avec le module mlxtend
    '''
    
    card_R1_union_R2=len(R1)+len(R2)
    card_R1_inter_R2=len(R1.merge(right=R2,left_on=['antecedents','consequents'],right_on=['antecedents','consequents']))
    
    return card_R1_inter_R2/card_R1_union_R2

def supp_diff(R1,R2) :
    
    card_R1_union_R2 = len(R1)+len(R2)
    R1_inter_R2=R1.merge(right=R2,left_on=['antecedents','consequents'],right_on=['antecedents','consequents'])
    card_R1_inter_R2 = len(R1_inter_R2)
    sum_diff_supp = R1[(R1['antecedents']==R1_inter_R2['antecedents']) & (R1['consequents']==R1_inter_R2['consequents'])]-R2[(R2['antecedents']==R1_inter_R2['antecedents']) & (R2['consequents']==R1_inter_R2['consequents'])]
    
    pass

def con_diff(R1,R2) :
    pass

def MRC(D,s,g,bs) :
    pass

def RDU(D,mrc) :
    pass