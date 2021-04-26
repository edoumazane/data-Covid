# import time
# import datetime as dt
# import os
# import glob
# import json

# import itertools as it
# import numpy as np
import pandas as pd

from my_package.v5_datepaths import temp_dir, retrieve_data, retrieve_temp
from my_package.v5_dicts import dep2reg, class_2_3C, reg_name, classvac_2_3C, reg_3C_pop, pops

def groupby_sum(d, columns):
    """ d: dataframe
        columns: list of str, columns to groupby
        returns: dataframe, grouped according to columns fed in
                other columns are summed
    """
    dg = (d
          .groupby(columns)
          .agg([sum])
          .reset_index()
         )
    dg.columns = dg.columns.droplevel(level = 1)
    dg = dg.reindex(columns = d.columns) # keep same column order                        
    return dg

def columns_first(d, columns):
    """ d: dataframe
        by: list of str, columns to put first
        returns: dataframe reordered
    """
    d = d.reindex(columns = columns + [column for column in d.columns if column not in columns])
    return d

def map_rename(d, col_in, col_out, func):
    """ d: dataframe
        col_in mapped: str, name of column mapped and deleted
        func: function mapped
        col_out: str, name of resulting column
        returns: modified dataframe
    """
    d[col_in] = d[col_in].map(func)
    return d.rename(columns = {col_in: col_out})


### functions for the coronavirus-tests dataset

def sp_input():
    """
    returns din: raw dataframe
    path_temp: pathway for temporary files
    """
    dataset = 'sp-pos-quot-dep'
    data_fname, path_temp = retrieve_data(dataset)
    print(data_fname)
    din = pd.read_csv(data_fname, sep = ';', parse_dates = ['jour'], dtype = {'dep': str})
    return din, path_temp

def sp_tot_3C(din, three_class = True,):

    din = din.copy()
    din = din[~din.dep.isin(['970', '975', '977', '978'])].reset_index(drop = True)

    d_dep = din.rename(columns = {'dep': 'entity'})

    d = map_rename(din, 'dep', 'entity', lambda x: dep2reg[x])
    d_reg = groupby_sum(d, columns = ['entity', 'jour', 'cl_age90'])

    d = din.drop(columns = ['dep'])
    d_nat = groupby_sum(d, columns = ['jour', 'cl_age90'])
    d_nat['entity'] = 'France'

    d = pd.merge(d_dep, d_reg, how = 'outer')
    d_tot = pd.merge(d, d_nat, how = 'outer')

    if three_class:
        d = map_rename(d_tot, 'cl_age90', 'three_class', lambda x: class_2_3C[x])
        d3C = groupby_sum(d, ['entity', 'jour', 'three_class'])
        return columns_first(d3C, columns = ['entity', 'three_class', 'jour'])
    else:
        return columns_first(d_tot, columns = ['entity', 'cl_age90', 'jour'])

def sp_compute(din):
    """
    d: dataframe with columns 'P', 'T' and 'pop'
    returns: dataframe with extra columns 'P hebdo', 'T hebdo', 'incidence hebdo', 'taux de positifs hebdo', 'taux de tests hebdo'
    """
    d = din.copy()
    d1 = (d
            .groupby(['entity', 'three_class'])
            .rolling(window = 7, on = 'jour')
            .sum()
            .fillna(0)
            .reset_index()
            .set_index('level_2')
            .rename(columns = {
                                    'P': 'P hebdo',
                                    'T': 'T hebdo',
                                })
        )
    d[['P hebdo', 'T hebdo']] = d1[['P hebdo', 'T hebdo']]
    d['incidence hebdo'] = d['P hebdo'] / d['pop'] * 100000
    d['taux de positifs hebdo'] = d['P hebdo'] / d['T hebdo'] * 100
    d['taux de tests hebdo'] = d['T hebdo'] / d['pop'] * 100000
    
    return d

### functions for the hospital dataset

def hosp_input():
    dataset = 'donnees-hospitalieres-classe-age-covid19'
    data_fname, path_temp = retrieve_data(dataset)
    print(data_fname)
    din = pd.read_csv(data_fname, sep = ';', parse_dates = ['jour'], dtype = {'reg': str})
    return din, path_temp

def hosp_3C(d):
    d['entity'] = (d['reg']
                .map(lambda x: reg_name[str(x)] )
                .replace({
                    'Guadeloupe':'Outre-mer (DROM)',
                    'Martinique':'Outre-mer (DROM)',
                    'Guyane':'Outre-mer (DROM)',
                    'La Réunion':'Outre-mer (DROM)',
                    'Mayotte':'Outre-mer (DROM)',
                })
                )
    d['three_class'] = d['cl_age90'].map(lambda x: class_2_3C[x])
    
    d.drop(columns = ['reg', 'cl_age90'], inplace = True)
    
    d_reg = groupby_sum(d, columns = ['entity', 'jour', 'three_class',])

    d = d_reg.copy()
    d_nat = groupby_sum(d, columns = ['jour', 'three_class',])
    d_nat['entity'] = 'France'

    d_tot = pd.merge(d_reg, d_nat, how = 'outer')

    d_tot = d_tot.drop(columns = ['HospConv', 'SSR_USLD', 'autres', 'rad'])

    return columns_first(d_tot, ['entity', 'three_class', 'jour',])

def hosp_compute(din):
    d = din.copy()
    d['dc hebdo'] = d['dc'] - (d.groupby(['entity', 'three_class'])
                            .shift(7)
                            )['dc']
    d['taux hosp'] = d.apply(lambda x: x['hosp'] / reg_3C_pop 
                                                        [ x['entity'] ]
                                                        [ x['three_class'] ] * 100000, 
                            axis = "columns")
    d['taux rea'] = d.apply(lambda x: x['rea'] / reg_3C_pop
                                                        [ x['entity'] ]
                                                        [ x['three_class'] ] * 100000, 
                            axis = "columns")
    d['taux décès'] = d.apply(lambda x: x['dc hebdo'] / reg_3C_pop
                                                        [ x['entity'] ]
                                                        [ x['three_class'] ] * 100000, 
                            axis = "columns")
    return d

### functions for the hospital department dataset

def hosp_dep_input():
    dataset = 'donnees-hospitalieres-covid19'
    data_fname, path_temp = retrieve_data(dataset)
    print(data_fname)
    din = pd.read_csv(data_fname, sep = ';', parse_dates = ['jour'], dtype = {'reg': str})
    return din, path_temp

def hosp_dep_compute(din):
    
    d1 = din.copy()
    d2 = (d1[d1.sexe == 0]
                .drop(columns =['sexe'])
                .sort_values(['dep', 'jour'])
                .reset_index(drop = True)
                .rename(columns = {'dep': 'entity'})
    )
    d2['dc hebdo'] = d2['dc'] - d2.groupby(['entity']).shift(7)['dc']

    d = d2.copy()
    
    d['taux hosp'] = d.apply(lambda x: x['hosp'] / pops 
                                                        [ x['entity'] ]
                                                        [ 'whole' ] * 100000, 
                            axis = "columns")
    d['taux rea'] = d.apply(lambda x: x['rea'] / pops
                                                        [ x['entity'] ]
                                                        [ 'whole' ] * 100000, 
                            axis = "columns")
    d['taux décès'] = d.apply(lambda x: x['dc hebdo'] / pops
                                                        [ x['entity'] ]
                                                        [ 'whole' ] * 100000, 
                            axis = "columns")
    return d

### functions for the vaccine dataset

def vac_input():
    dataset = 'vacsi-a-dep'
    data_fname, path_temp = retrieve_data(dataset)
    din = pd.read_csv(data_fname, sep = ';', parse_dates = ['jour'], dtype = {'dep': str})
    print(data_fname)
    return din, path_temp

def vac_tot_3C(din, three_class = True):
    din = din[~din.dep.isin(['00', '750', '970', '975', '977', '978'])].reset_index(drop = True)

    d_dep = din.rename(columns = {'dep': 'entity'})

    d = map_rename(din, 'dep', 'entity', lambda x: dep2reg[x])
    d_reg = groupby_sum(d, columns = ['entity', 'jour', 'clage_vacsi'])

    d = din.drop(columns = ['dep'])
    d_nat = groupby_sum(d, columns = ['jour', 'clage_vacsi'])
    d_nat['entity'] = 'France'

    d = pd.merge(d_dep, d_reg, how = 'outer')
    d_tot = pd.merge(d, d_nat, how = 'outer')

    if not three_class:
        return columns_first(d, columns = ['entity', 'clage_vacsi', 'jour'])
    else:
        d = map_rename(d_tot, 'clage_vacsi', 'three_class', lambda x: classvac_2_3C[x])
        d3C = groupby_sum(d, ['entity', 'jour', 'three_class'])
        return columns_first(d3C, columns = ['entity', 'three_class', 'jour'])

def vac_compute(din):
    d = din.copy()
    d['taux dose 1'] = d.apply(lambda x: x['n_cum_dose1'] / reg_3C_pop 
                                                    [ x['entity'] ]
                                                    [ x['three_class'] ] * 100, 
                         axis = "columns")
    d['taux dose 2'] = d.apply(lambda x: x['n_cum_dose2'] / reg_3C_pop
                                                    [ x['entity'] ]
                                                    [ x['three_class'] ] * 100, 
                        axis = "columns")
    return d