import time
import datetime as dt
import os
import glob
import json

import itertools as it
import numpy as np

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

import seaborn as sns

def date(days):
    """
    days: integer, days before today (default = 0)
    returns date in two string format: %Y-%m-%d and %d/%m/%Y
    """
    day = dt.date.today() - dt.timedelta(days = days)
    date_choice = day.strftime("%Y-%m-%d")
    date_text = day.strftime("%d/%m/%Y")
    return date_choice, date_text


today, today_text = date(0)
days = input('Today is {}. Retrieve data from how many days? '.format(today_text))
if not days:
    days = 1
else:
    days = int(days)
date_choice, date_text = date(days)
print('Ok, will retrieve data from {}'.format(date_text))


def data_path(date_choice, dataset, version = '5Lv3'):
    """
    date_of_choice: string, date of choice %Y-%m-%d 
    dataset: string, target dataset
    version: string, version of code file
    returns: tuple of strings, path to data file, prefix path to temp files
    """
    fname_format = '../Data/{}-{}-??h??.csv'.format(dataset, date_choice)
    try: 
        fname = glob.glob(fname_format)[0]
    except: 
        print('There is no file {}'.format(fname_format))
        return
    try: os.mkdir('./Temp/{}'.format(version))
    except: pass
    path_temp = './Temp/{}/{}'.format(version, fname[7:-4])
    print(fname)
    return fname, path_temp

def temp_path(date_choice, dataset, extension, version = '5Lv3'):
    """
    date_of_choice: string, date of choice %Y-%m-%d 
    dataset: string, target dataset
    extension: string, eg 'tot' or 'tot-3C
    version: string, version of code file
    returns: path to temp file
    """
    fname_format = './Temp/{}/{}-{}-??h??-{}.csv'.format(version, dataset, date_choice, extension)
    try: 
        fname = glob.glob(fname_format)[0]
    except: 
        print('There is no file {}'.format(fname_format))
        return
    print(fname)
    return fname


fname = 'Json/reg_name.json'
with open(fname, 'r') as f:
    reg_name = json.loads(f.read())

fname = 'Json/reg2dep.json'
with open(fname, 'r') as f:
    reg2dep = json.loads(f.read())

fname = 'Json/dep-name.json'
with open(fname, 'r') as f:
    dep_name = json.loads(f.read())

fname = 'Json/dep2reg.json'
with open(fname, 'r') as file:
    dep2reg = json.loads(file.read())

fname = 'Json/reg_3C_pop.json'
with open(fname, 'r') as file:
    reg_3C_pop = json.loads(file.read())

class_2_3C = {0: 'whole',
               9: '0-29',
               19: '0-29',
               29: '0-29',
               39: '30-59',
               49: '30-59',
               59: '30-59',
               69: '60+',
               79: '60+',
               89: '60+',
               90: '60+',
              }

classvac_2_3C = {0: 'whole',
               24: '0-29',
               29: '0-29',
               39: '30-59',
               49: '30-59',
               59: '30-59',
               64: '60+',
               69: '60+',
               74: '60+',
               79: '60+',
               80: '60+',
              }

reg_2lignes = {'Auvergne-Rhône-Alpes': 'Auvergne-\nRhône-Alpes',
 'Bourgogne-Franche-Comté': 'Bourgogne-\nFranche-Comté',
 'Bretagne': 'Bretagne',
 'Centre-Val de Loire': 'Centre-\nVal de Loire',
 'Corse': 'Corse',
 'Grand Est': 'Grand Est',
 'Hauts-de-France': 'Hauts-de-France',
 'Normandie': 'Normandie',
 'Nouvelle-Aquitaine': 'Nouvelle-\nAquitaine',
 'Occitanie': 'Occitanie',
 'Outre-mer': 'Outre-mer',
 'Pays de la Loire': 'Pays\nde la Loire',
 "Provence-Alpes-Côte d'Azur": "Provence-\nAlpes-Côte d'Azur",
 'Île-de-France': 'Île-de-France'}

deps = ['01', '02', '03', '04', '05', '06', '07', '08',
       '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19','2A', '2B',
       '21', '22', '23', '24', '25', '26', '27', '28', '29', 
       '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40',
       '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51',
       '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62',
       '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73',
       '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84',
       '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95',
       '971', '972', '973', '974', '975', '976', '977', '978']

regs = ['Auvergne-Rhône-Alpes',
 'Bourgogne-Franche-Comté',
 'Bretagne',
 'Centre-Val de Loire',
 'Corse',
 'Grand Est',
 'Hauts-de-France',
 'Île-de-France',
 'Normandie',
 'Nouvelle-Aquitaine',
 'Occitanie',
 'Pays de la Loire',
 "Provence-Alpes-Côte d'Azur",
 'Outre-mer']