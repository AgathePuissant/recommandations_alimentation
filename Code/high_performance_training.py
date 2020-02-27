# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 14:57:18 2020

@author: ADMIN
"""

import multiprocessing as mp
print("Number of processors: ", mp.cpu_count())

# Parallelizing using Pool.apply()


# Step 1: Init multiprocessing.Pool()
pool = mp.Pool(mp.cpu_count())

# Step 2: `pool.apply` the `howmany_within_range()`
result = pool.apply(entrainement_systeme, args=(2))

results = [pool.apply(entrainement_systeme, args=(2)) for i in range(2)]

# Step 3: Don't forget to close
pool.close()    

print(results[:10])
#> [3, 1, 4, 4, 4, 2, 1, 1, 3, 3]