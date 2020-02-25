# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 14:45:20 2020

@author: anael
"""

import configparser


config = configparser.ConfigParser() #sauvegarde des éléments relatifs au user
config['CURRENTUSER']={
        'current_user_id':'default',
      }

config['DEFAULTDATA']={
                'id':'defaultid',
                'name':'ana',
                'age':21,
                'sexe':'F',
                'taille':165,
                'poids':58,
                'pref':{'from':3,
        'fruits':3,
        'legume':4,
        'viande':7,
        'poiss':2,
        'volGib':0,
        'prodLait':10},
                'cluster':'None',
                'epsilon':0.5,
                'omega':0.5,
                'last5subs':[],
                }
with open('init.ini', 'w') as configfile:
    config.write(configfile)