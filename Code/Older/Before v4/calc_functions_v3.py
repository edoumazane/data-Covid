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

def groupby_sum(d, columns):
    """ d: dataframe
        columns: list of column names
        returns: dataframe is grouped according to columns fed in
                other columns are summed
                dataframe is then formatted into a dataframe"""
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
        by: a list of column names
        returns: dataframe reordered"""
    d = d.reindex(columns = columns + [column for column in d.columns if column not in columns])
    return d

def calc_hebdo(d, columns_to_group, columns_to_sum):
    """
    d: a dataframe
    columns_to_group: list of columns from which groups will be formed
            for example ['entity', 'three_class'] -> will calculate hebdo sums for (regionA, class1), (regionA, class2), etc.
    columns_to_sum: list of columns which values will be summed on a week-wise base
            for example ['P', 'T']
    """
    #     calculate unique values for columns to group    
    uniques = []
    for col in columns_to_group:
        uniques.append(list(d[col].unique()))  
    
    #     create new columns :
    columns_to_sum_hebdo = [col + ' hebdo' for col in columns_to_sum]
    d[columns_to_sum_hebdo] = np.zeros((len(d), len(columns_to_sum_hebdo)))
    
    #     iterate through groups
    tic1 = time.time()
    for conds in it.product(*uniques):
        
        conditions_all = np.all(
                                    [(d[col] == cond) for col, cond in zip(columns_to_group, conds)]
                                , axis = 0)
        d2 = d[conditions_all] # select rows corresponding to the group
        
    #             d[['P hebdo','T hebdo']] = d2.apply(lambda x : (d2[ (d2['jour'] <= x['jour']) 
    #                                                             & (d2['jour'] > x['jour'] - np.timedelta64(1,'W'))]
    #                                                         ['P']
    #                                                         .sum()), axis = 1)
    #             d['P hebdo'] = d['P hebdo'] + d['temp'].fillna(0)
    #             d['temp'] = d2.apply(lambda x : (d2[ (d2['jour'] <= x['jour']) 
    #                                                             & (d2['jour'] > x['jour'] - np.timedelta64(1,'W'))]
    #                                                         ['T']
    #                                                         .sum()), axis = 1)
    #             d['T hebdo'] = d['T hebdo'] + d['temp'].fillna(0)     


        d[columns_to_sum_hebdo] = (d[columns_to_sum_hebdo] 
                               + d2
                                    .apply(lambda x: 
                                              d2[columns_to_sum][ 
                                                                  (d2['jour'] <= x['jour']) 
                                                                  & (d2['jour'] > x['jour'] - np.timedelta64(1, 'W'))
                                                                 ].sum(), axis = 1)
                           # actually calculate the sums
                                   
                                    .rename(columns = {old: new for old, new in zip(columns_to_sum,
                                                                                      columns_to_sum_hebdo)})
                           # required to sum two 2-cols dataframes 
                              ).fillna(d[columns_to_sum_hebdo])
                            # required to replace "val + NaN" = NaN by val
            
        toc1 = time.time()  # for graphical output
        print('{:.2f} s : ({}) calculated for ({})'.format(-tic1+toc1, ', '.join(columns_to_sum_hebdo) ,', '.join(conds)))
    return d

def calc_delta_hebdo(d, columns_to_group, columns_to_delta):
    """
    d: a dataframe
    columns_to_group: list of columns from which groups will be formed
            for example ['entity', 'three_class'] -> will calculate hebdo for regionA, class1, regionA, class2, etc.
    columns_to_sum: list of columns which values will be used to calculate a one-week delta
            for example ['dc']
    """
    #     calculate unique values for columns to group    
    uniques = []
    for col in columns_to_group:
        uniques.append(list(d[col].unique()))
    #     new columns :
    columns_to_delta_hebdo = [col + ' hebdo' for col in columns_to_delta]
    d[columns_to_delta_hebdo] = np.zeros((len(d), len(columns_to_delta)))
    #     iterate through groups
    tic1 = time.time()
    for conds in it.product(*uniques):
    #     select rows corresponding to the group
        conditions_all = np.all(
                                    [(d[col] == cond) for col, cond in zip(columns_to_group, conds)]
                                , axis = 0)
        d2 = d[conditions_all]

        #     calculate delta
        d3 = (d2
              .loc[(d.jour >= '2020-03-25')]
              .jour
              .apply(lambda x: 
                            d2[d2.jour == x][columns_to_delta].values[0]
                        - d2[d2.jour == x - np.timedelta64(1,'W')][columns_to_delta].values[0])

             )

        # transform a pd.Series of lists (d3) into a pd.DataFrame (d4)
        d4 = (pd.DataFrame
              .from_dict(dict(zip(d3.index, d3.values)), orient = 'index', columns = columns_to_delta)
              .rename(columns = {old: new for old, new in zip(columns_to_delta, 
                                                              columns_to_delta_hebdo)})
             )

        # add deltas from this group to the dataframe
        d[columns_to_delta_hebdo] = ((d[columns_to_delta_hebdo] + d4)
                                                         .fillna(d[columns_to_delta_hebdo])
                                                        )                        
            
        toc1 = time.time()
        print('{:.2f} s : ({}) calculated for ({})'.format(-tic1+toc1, ', '.join(columns_to_delta_hebdo) ,', '.join(conds)))
    return d