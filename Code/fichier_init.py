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

config['USERDATA']={
                'id':'defaultid',
                'name':'ana',
                'age':21,
                'sexe':'F',
                'taille':165,
                'poids':58,
                'pref':[],
                'epsilon':0.5,
                'omega1':0.5,
                'omega2':0.5,
                }
with open('init.ini', 'w') as configfile:
    config.write(configfile)