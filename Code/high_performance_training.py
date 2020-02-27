# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 14:57:18 2020

@author: chulai
"""

import multiprocessing as mp


print("Number of processors: ", mp.cpu_count())

# Parallelizing using Pool.apply()


# Step 1: Init multiprocessing.Pool()
pool = mp.Pool(mp.cpu_count())

# Step 2: `pool.apply` the `howmany_within_range()`
result = pool.apply(vir.entrainement_systeme, args=(2))

results = [pool.apply(vir.entrainement_systeme, args=(2)) for i in range(2)]

# Step 3: Don't forget to close
pool.close()    

print(results[:10])
#> [3, 1, 4, 4, 4, 2, 1, 1, 3, 3]

import pandas as pd
import Virtual_User_System as vir
import numba as nb
from numba import jit, cuda, vectorize, typeof
# to measure exec time
from timeit import default_timer as timer    

def func(nbre_user) :
    
    # Les constants 
    nbre_jour = 5
    
    liste_alpha_beta = [[1.01, 1.005]]
    # , [1.1, 1.05], [1.15, 1.075]
    dict_omega = {0.01 : [0.2, 0.3]}
    seuil_acc = 0.8
    
    colnames = ['alpha', 'beta', 'omega_ini', 'seuil_acc', 'user', 'cluster', 'id_user', 'nojour', 'tyrep', 'avecqui', 'repas', 'substitution', 'reponse', 'omega', 'epsilon']
    data = pd.DataFrame(columns = colnames)
    
    for alpha, beta in liste_alpha_beta :
        for pas_modif, liste_omega in dict_omega.items() :
            for omega in liste_omega :
                print(alpha, beta, omega, pas_modif, seuil_acc)
                systeme = vir.System(nbre_user, nbre_jour, seuil_nutri = 80, alpha = alpha, beta = beta, omega = omega, seuil_recom = 10, seuil_acc = seuil_acc, pas_modif = pas_modif)
                systeme.entrainement()
                df = pd.concat([pd.DataFrame(data = {'alpha' : alpha, 
                                                    'beta' : beta, 
                                                    'omega_ini' : omega, 
                                                    'seuil_acc' : seuil_acc}, index = range(len(systeme.table_suivi))),
                               systeme.table_suivi], axis = 1)
                data = data.append(df, sort = False)
    return data
# @jit(target ="cuda")
#@vectorize(['float32(float32)'], target='cuda')


seq = ['seuil_acc', nb.float64]   
@jit(seq, target = "cuda")
@nb.njit()

def func2(nbre_user) :
    
    # Les constants 
    nbre_jour = 5
    
    liste_alpha_beta = [[1.01, 1.005]]
    # , [1.1, 1.05], [1.15, 1.075]
    dict_omega = {0.01 : [0.2, 0.3]}
    seuil_acc = 0.8
    # liste_alpha_beta, dict_omega, 
    return nbre_jour, seuil_acc, liste_alpha_beta
    
    colnames = ['alpha', 'beta', 'omega_ini', 'seuil_acc', 'user', 'cluster', 'id_user', 'nojour', 'tyrep', 'avecqui', 'repas', 'substitution', 'reponse', 'omega', 'epsilon']
    data = pd.DataFrame(columns = colnames)
    
    for alpha, beta in liste_alpha_beta :
        for pas_modif, liste_omega in dict_omega.items() :
            for omega in liste_omega :
                print(alpha, beta, omega, pas_modif, seuil_acc)
                systeme = vir.System(nbre_user, nbre_jour, seuil_nutri = 80, alpha = alpha, beta = beta, omega = omega, seuil_recom = 10, seuil_acc = seuil_acc, pas_modif = pas_modif)
                systeme.entrainement()
                df = pd.concat([pd.DataFrame(data = {'alpha' : alpha, 
                                                    'beta' : beta, 
                                                    'omega_ini' : omega, 
                                                    'seuil_acc' : seuil_acc}, index = range(len(systeme.table_suivi))),
                               systeme.table_suivi], axis = 1)
                data = data.append(df, sort = False)
    return data

start = timer()
test = func(1)
print("without GPU:", timer()-start)     
#16.73s

start = timer()
test1 = func2(1)
print("with GPU:", timer()-start)
# autojit is deprecated and will be removed in a future release. Use jit instead.
