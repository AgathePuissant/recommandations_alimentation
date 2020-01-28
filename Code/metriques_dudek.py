# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 11:21:31 2020

@author: agaca
"""

def basic_dudek(R1,R2) :
    '''
    Fonction qui renvoie un dictionnaire contenant :  
        - la métrique de recouvrement entre deux sets de règles d'association : rules_overlap
        - la différence moyenne de support entre ces deux sets : supp_diff
        - la différence moyenne de confiance entre ces deux sets : con_diff
    --------------
        - R1, R2 : DataFrame de règles d'association obtenus avec le module mlxtend
    '''
    R1_inter_R2=R1.merge(right=R2,left_on=['antecedents','consequents'],right_on=['antecedents','consequents'])
    
    card_R1_union_R2=len(R1)+len(R2)
    card_R1_inter_R2 = len(R1_inter_R2)
    
    sum_diff_supp = (R1_inter_R2['support_x']-R1_inter_R2['support_y']).sum()
    sum_diff_con = (R1_inter_R2['confidence_x']-R1_inter_R2['confidence_y']).sum()
    
    rules_overlap = card_R1_inter_R2/card_R1_union_R2
    supp_diff = (sum_diff_supp + card_R1_union_R2 - card_R1_inter_R2)/card_R1_union_R2
    con_diff = (sum_diff_con + card_R1_union_R2 - card_R1_inter_R2)/card_R1_union_R2
    
    return {"rules_overlap" : rules_overlap, "supp_diff" : supp_diff, "con_diff" : con_diff}


def MRC(D,s,g,bs) :
    pass

def RDU(D,mrc) :
    pass