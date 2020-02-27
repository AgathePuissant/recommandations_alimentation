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
                'name':'MangerMieux',
                'age':48,
                'sexe':'H',
                'taille':185,
                'poids':80,
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
                'last10subs':{
                        'compteur':0,
                        'accept':0,
                        },
                }
with open('init.ini', 'w') as configfile:
    config.write(configfile)