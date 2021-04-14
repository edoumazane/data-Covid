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

today = dt.date.today().strftime("%Y-%m-%d")
date_choice = dt.date.today() - dt.timedelta(days = 0)
date = date_choice.strftime("%Y-%m-%d")
date_text = date_choice.strftime("%d/%m/%Y")

path_test = '../Data/sp-pos-quot-dep-{}-??h??.csv'.format(date)
path_test = glob.glob(path_test)
fname_temp_test = './Temp' + path_test[0][7:-4]
fname_output_test = '../Output' + path_test[0][7:-4]

path_hosp = '../Data/donnees-hospitalieres-classe-age-covid19-{}-??h??.csv'.format(date)
path_hosp = glob.glob(path_hosp)
fname_temp_hosp = './Temp' + path_hosp[0][7:-4]
fname_output_hosp = '../Output' + path_hosp[0][7:-4]

path_vac = '../Data/vacsi-a-dep-{}-??h??.csv'.format(date)
path_vac = glob.glob(path_vac)
fname_temp_vac = './Temp' + path_vac[0][7:-4]
fname_output_vac = '../Output' + path_vac[0][7:-4]

path_synth = '../Data/donnees-{}-synthese-{}.csv'.format(date, today)
fname_temp_synth = './Temp' + path_synth[7:-4]
fname_output_synth = '../Output' + path_synth[7:-4]

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