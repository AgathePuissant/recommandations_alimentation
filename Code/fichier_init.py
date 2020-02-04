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
with open('init.ini', 'w') as configfile:
    config.write(configfile)