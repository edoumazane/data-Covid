import time
import datetime as dt
import os
import glob
import json
import math
import itertools as it

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from matplotlib.ticker import StrMethodFormatter, AutoMinorLocator

from my_package.v5_datepaths import TODAY, VERSION, output_dir, save_output
from my_package.v5_datepaths import DATE_CHOICE as DATE
from my_package.v5_dicts import reg_2lignes, reg2dep, dep_name, deps_outlay_fig_synthese, pops, pops_France_str, pops_regs_str

from my_package.v5_graph_options import graph_options

# try: os.mkdir('../Output/{}-{}-{}'.format(VERSION, DATE_CHOICE[0], TODAY[0]))
# except: pass
# try: os.mkdir('../Output/{}-{}-{}/PNG'.format(version, DATE_CHOICE[0], TODAY[0]))
# except: pass
# try: os.mkdir('../Output/{}-{}-{}/PDF'.format(version, DATE_CHOICE[0], TODAY[0]))
# except: pass

def format_graph(ax, x_axis = 'complete', y_labels = "to_the_left", rescale = 1, **kwargs):
    """
    formats the graph
    ax: axes object
    ymin, ymax: integer
    x_axis : 'without', 'regular', 'complete'
    y_labels : 'without', 'to_the_left', 'to_the_right
    **kwargs: graph_options
    """
    ax.patch.set_alpha(0)
    
    ###
    # no spines
    ###
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    ###
    # yaxis default settings
    ###
    ymin = kwargs['ymin'] 
    ymax = kwargs['ymax'] * rescale
    ax.set_ylim(ymin, ymax)
    ymajloc = [el for el in kwargs['majloc'] if el < ymax]
    yminloc = [el for el in kwargs['minloc'] if el < ymax]
    ax.yaxis.set_ticks(ymajloc)
    ax.yaxis.set_ticks(yminloc, minor = True)
    ax.yaxis.grid(which = 'major', alpha = 0.5)
    ax.yaxis.grid(which = 'minor', alpha = 0.2)
    ax.yaxis.set_tick_params(left = False, which = 'both', labelsize = 9)
    
    ###
    # yaxis conditional settings
    ###

    if y_labels == "without":
        ax.yaxis.set_tick_params(left = False, labelsize = 9)
        ax.yaxis.set_ticklabels([])

    if y_labels == "to_the_left":
        ax.yaxis.set_tick_params(left = False, labelsize = 9)
        ax.yaxis.set_major_formatter(lambda x, pos: '{: <4d}'.format(int(x)))
        ax.yaxis.set_ticklabels(ymajloc, ha = 'right')

    if y_labels == "to_the_right":
        ax.yaxis.set_tick_params(left = False,
            labelright = True, labelleft = False, labelsize = 9)
        ax.yaxis.set_major_formatter(lambda x, pos: '{: >4d}'.format(int(x)))
        ax.yaxis.set_ticklabels(ymajloc, ha = 'left')
    
    ###
    # xaxis and vertical lines default
    ###

    ax.set_xlim(dt.datetime(2020, 3, 1), 
                    dt.datetime(2021, 6, 1))
    ax.axvline(dt.datetime(2021, 1, 1), 
                    ymin = 0, ymax = .95, 
                    c = 'black', linewidth = 0.5, linestyle = '--')
    ax.axvspan(dt.datetime(2020, 3, 17), 
                    dt.datetime(2020, 5, 10),
                    ymin = 0, ymax = .95, alpha=0.15, color='gray')
    ax.axvspan(dt.datetime(2020, 10, 30), 
                    dt.datetime(2020, 12, 15),
                    ymin = 0, ymax = .95, alpha=0.15, color='gray')
    ax.axvspan(dt.datetime(2021, 4, 5), 
                    dt.datetime(2021, 5, 2),
                    ymin = 0, ymax = .95, alpha=0.15, color='gray')
    
    ###
    # xaxis conditional
    ###

    if x_axis == 'without':
        ax.xaxis.set_tick_params(bottom = False)
        ax.xaxis.set_ticklabels([])

    if x_axis == 'regular':
        ax.xaxis.set_tick_params(bottom = True, labelsize = 9)
        xloc = []
        for i in range(8):
            xloc.append(dt.datetime(2020, 3 + 2*i, 1) if 2 * i <= 9
                            else dt.datetime(2021, 2*i - 9, 1)
                       )
        labels = ['mars','mai', 'juil.', 
                 'sept.',  'nov.', 
                 'janv.', 'mars', 
                  'mai']
        ax.xaxis.set_ticks(xloc)
        ax.xaxis.set_ticklabels(labels, rotation=45, ha="right", rotation_mode="anchor")

    if x_axis == 'complete':
        ax.tick_params(axis='x', bottom = True,
                labelsize = 9)
        xloc = []
        for i in range(16):
            xloc.append(dt.datetime(2020, 3 + i , 1) if i <= 9 
                        else dt.datetime(2021, i - 9, 1))
        labels = ['mars','avril', 'mai', 'juin', 'juil.', 
                    'août', 'sept.', 'oct.', 'nov.', 'déc.', 
                     'janv.', 'fév.', 'mars', 'avril', 
                      'mai', 'juin']
        ax.set_xticks(xloc)
        ax.set_xticklabels(labels)
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor") 

def plot_three_curves(ax, d, entity, column_to_plot, whole = 'without', **kwargs):
    """
    """
    main_color = kwargs['main_color']

    if whole in ['without', 'with']:
        dplot = d.loc[d.entity == entity].loc[d.three_class == '0-29']
        ax.plot(dplot.jour, dplot[column_to_plot], c = "firebrick", linewidth = 1, label = '0-29 ans')
        
        dplot = d.loc[d.entity == entity].loc[d.three_class == '30-59']
        ax.plot(dplot.jour, dplot[column_to_plot], c = "black", linewidth = 1.5, label = '30-59 ans')

        dplot = d.loc[d.entity == entity].loc[d.three_class == '60+']
        ax.plot(dplot.jour, dplot[column_to_plot], c = main_color, linewidth = 3, label = '60 ans et +')

    if whole in ['with', 'only']:
        dplot = d.loc[d.entity == entity].loc[d.three_class == 'whole']
        ax.plot(dplot.jour, dplot[column_to_plot], c = main_color, linewidth = 1.5, linestyle = '-', label = 'tous âges')

def simple_figure(d, entity, column_to_plot, autoscale = False):
    
    if autoscale:
        ymin = d[d.entity == entity][column_to_plot].min()
        ymax = d[d.entity == entity][column_to_plot].max()
    fig, ax = plt.subplots(1, 1, figsize = (12, 3))
    kwargs = graph_options[column_to_plot]

    plot_three_curves(ax, d, entity, column_to_plot, **kwargs)
    if autoscale: format_graph(ax, ymin, ymax)
    else:
        format_graph(ax, **kwargs)
    ax.set_title('{}: {}'.format(entity, column_to_plot), 
                    fontsize = 22, fontweight = 'semibold',
                    c = 'royalblue', family = 'sans', va = 'center', ha = 'center',)

def figure_line(row, nrow, axs, d, column_to_plot, regions):
    """
    """
    ncol = len(regions) + 2

    ###
    # Première colonne : France et légende
    ###

    col = 0
    ax = axs[row * ncol + col]
    plot_three_curves(ax, d, "France", column_to_plot, **graph_options[column_to_plot])
    format_graph(ax,
            x_axis = ('regular' if (row == nrow - 1) else 'without'), 
            y_labels = ('to_the_left' if (col == 0) else 'to_the_right' if (col == ncol - 1) else 'without'), 
            dense = True,
            **graph_options[column_to_plot])
    #####
    # Légende
    #
    ax.legend(bbox_to_anchor=[1.55, .45], loc='center', frameon=True,
              labelspacing=0.5, handlelength=2, handletextpad=0.5, fontsize = 11,     
              title = graph_options[column_to_plot]['title'], title_fontsize = 10,
              )
    plt.setp(ax.get_legend().get_title(), multialignment='center')

    #####
    # Titre première ligne : "France entière"
    #
    if (row == 0):
        ax.set_title('France', 
                    x = 0.5, y = 1.1, fontsize = 24, fontweight = 'semibold',
                    c = 'royalblue', family = 'sans', va = 'center', ha = 'center',
                    )
    #####
    #     Deuxième colonne vide (pour la légende)
    #
    ax = axs[row * ncol + 1]
    ax.set_axis_off() 

    #####
    #     Colonnes suivantes
    #
    for i, region in enumerate(regions):
        col = 2 + i
        ax = axs[row * ncol + col]
        plot_three_curves(ax, d, region, column_to_plot, **graph_options[column_to_plot])
        format_graph(ax,
                x_axis = ('regular' if (row == nrow -1 ) else 'without'), 
                y_labels = ('to_the_left' if (col == 0) else 'to_the_right' if (col == ncol - 1) else 'without'),
                dense = True,
                **graph_options[column_to_plot])
        #####
        # Titres colonnes suivantes, première ligne : nom des régions       
        #
        if row == 0:
            ax.set_title(reg_2lignes[region], 
                        x = 0.5, y = 1.1, fontsize = 16, fontweight = 'semibold',
                        c = 'royalblue', family = 'sans', va = 'center', ha = 'center',
                        )

def fig_type1(d, regions, regions_ordered, fig_id):

    ncol = len(regions) + 2
    fig, axs = plt.subplots(5, ncol, figsize = (2.5 * ncol, 8))
    axs = axs.ravel() 
    
    for i, column_to_plot in enumerate([
        "taux de tests hebdo",
        "incidence hebdo",
        "taux hosp",
        "taux rea", 
        "taux décès",
                    ]):
        figure_line(row = i,
                    nrow = 5,
                    axs = axs,
                    d = d,
                    column_to_plot = column_to_plot,
                    regions = regions,
                    )
    fig.subplots_adjust(left=0.035,
                        right=0.965, 
                        bottom=0.08, 
                        top=0.94, 
                        wspace=0.07, 
                        hspace=0.05)
    
    decomposition_clage = 'En France, il y a : {whole} millions d\'habitants, \
dont + de 60 ans : {class_older} millions, 30 à 59 ans : {class_middle} millions et \
0 à 29 ans : {class_younger} millions'.format(**pops_France_str)

    fig.suptitle('@E_Dmz - Données Santé Publique France ({date})\n\
{fig_id} - {decomposition_clage}'
        .format(fig_id = fig_id, date = DATE[1], decomposition_clage = decomposition_clage),
                x = 0.035, y = 0, 
                fontsize = 8, fontweight = 'normal', c = 'black', family = 'sans',
                ha = 'left', va = 'center')

    dir_PNG = output_dir + 'Type1/'
    save_output(fig, dir_PNG, fig_id)

def fig_type2(d, column_to_plot, regions_ordered):

    nrow, ncol = 4, 4
    fig, axs = plt.subplots(nrow, ncol, figsize = (3*ncol, 8))
    axs = axs.ravel()

    row, col = 0, 0
    ax = axs[0]
    plot_three_curves(ax, d, "France", column_to_plot, **graph_options[column_to_plot])
    format_graph(ax, x_axis='complete', **graph_options[column_to_plot])
    
    #####
    # Légende
    #
    (ax.legend(bbox_to_anchor=[0.5, -.7], 
              loc='center',
              labelspacing=0.5,       
              handlelength=2, 
              handletextpad=0.5,
              frameon=True,
              fontsize = 11,
              title = graph_options[column_to_plot]['title'],
              title_fontsize = 10,
              )
        )
    plt.setp(ax.get_legend().get_title(), multialignment='center')


    #####
    # Titre France
    #
    ax.set_title('France', x = 0.02, y = .95, loc = 'left', 
                 fontsize = 22, c = 'royalblue', fontweight='semibold')
    ax = axs[4]
    ax.set_axis_off() 


    #####
    # Régions
    #
    for i, region in enumerate(regions_ordered):
        if i+1 >= 4:
            i += 1 ## Skip 1st subplot of 2d row
        ax = axs[i+1]
        row = (i+1)//ncol
        col = (i+1)%ncol

        plot_three_curves(ax, d, region, column_to_plot, **graph_options[column_to_plot])
        format_graph(ax, 
                x_axis='without', 
                y_labels = ('to_the_left' if (col == 0) else 'to_the_right' if (col == ncol - 1) else 'without'),
                **graph_options[column_to_plot])

        #####
        # Titre régions
        #
        ax.set_title(region, x = 0.02, y = -0.15, loc = 'left', 
                     fontsize = 13, c = 'royalblue', fontweight='normal', family = 'sans')

        fig.subplots_adjust(left=0.035,
                        right=0.965, 
                        bottom=0.1, 
                        top=0.95, 
                        wspace=0.07, 
                        hspace=0.1) #Enough space for title
    #####
    # Note bas de page
    #

    decomposition_clage = 'En France, il y a : {whole} millions d\'habitants, \
dont + de 60 ans : {class_older} millions, 30 à 59 ans : {class_middle} millions et \
0 à 29 ans : {class_younger} millions'.format(**pops_France_str)

    fig.suptitle('@E_Dmz - Données Santé Publique France ({date})\n{decomposition_clage}'
        .format(date = DATE[1], decomposition_clage = decomposition_clage),
                x = 0.035, y = 0,                   
                fontsize = 8, fontweight = 'normal', c = 'black', family = 'sans',
                ha = 'left', va = 'bottom')

    dir_PNG = output_dir + 'Type2/'
    fig_id = 'fig-{extension}'.format(extension = graph_options[column_to_plot]["fname_extension"])
    save_output(fig, dir_PNG, fig_id) 

def fig_type3(d, region, column_to_plot, hosp = False):
        """
        d dataframe 
        plots one indicator (column_to_plot) for one region (region) and its component "départements"
        """
    #####
    # départements correspondant à la région
    #
        deps = reg2dep[region] 

    #####
    # layout
    #
        ndeps = len(deps)
        nrows = int(np.ceil((ndeps + 1) / 3))
        ncols = 3
        fig = plt.figure(constrained_layout=True, figsize = (12, 1.7 * nrows + 3))
        gs0 = fig.add_gridspec(2, 1, hspace = 0.2, height_ratios=[3, 1.7*nrows]) #haut et bas
        gs00 = gs0[1,0].subgridspec(ncols=ncols, nrows=nrows, wspace = 0.1, hspace = 0.05) #haut: départements et légende
        gs10 = gs0[0,0].subgridspec(1, 2, wspace=0.1, hspace=0) #bas: region et France

    ########
    # Note #
    ########
        avertissement = 'Pour les données hospitalières, la décomposition par classes d\'âge à l\'échelon départemental non disponible' if hosp else '' 
        decomposition_clage = 'En {region} : {whole} millions d\'habitants, \
dont + de 60 ans : {class_older} millions, 30 à 59 ans : {class_middle} millions et \
0 à 29 ans : {class_younger} millions'.format(region = region, **pops_regs_str[region])
        
        fig.suptitle('@E_Dmz - Données Santé Publique France ({date})\n{decomposition_clage}\n{avertissement}'
            .format(date = DATE[1],
                    decomposition_clage = decomposition_clage,
                    avertissement = avertissement),
                    x = 0.035, y = -.03 -0.015 * (5 - nrows), ha = 'left', va = 'top',                 
                    c = 'black', family = 'sans', fontsize = 9,
                        )

    #####
    # classement des départements
    #
        last_week = ((d.jour > np.datetime64(dt.datetime.fromisoformat(DATE[0]) - dt.timedelta(weeks = 1))) 
                & (d.jour <= np.datetime64(dt.datetime.fromisoformat(DATE[0]))))
        deps = (d[(last_week) 
                        & (d.entity.isin(deps))
                        & (d.three_class == '60+')]
                    .groupby('entity')[column_to_plot]
                    .mean()
                    .sort_values(ascending = False)
                    .index
                    .tolist())
        if hosp:
            last_week = ((d.jour > np.datetime64(dt.datetime.fromisoformat(DATE[0]) - dt.timedelta(weeks = 1))) 
                & (d.jour <= np.datetime64(dt.datetime.fromisoformat(DATE[0]))))
            deps = (d[(last_week) 
                        & (d.entity.isin(deps))]
                    .groupby('entity')[column_to_plot]
                    .mean()
                    .sort_values(ascending = False)
                    .index
                    .tolist())
    ################
    # Départements #
    ################
        rescale = d.loc[(d.entity.isin(deps))
                        , column_to_plot].max() / graph_options[column_to_plot]['minloc'][-1]
        
        whole = 'only' if hosp else 'without'
        for i,j in enumerate(deps_outlay_fig_synthese[ndeps]):
            
            #i index of graph, j index of axes
            ax = fig.add_subplot(gs00[j])
            plot_three_curves(ax, d, deps[i], column_to_plot, whole = whole, **graph_options[column_to_plot])
            x_axis = 'regular' if (j >= (3*nrows - 3)) else 'without'
            format_graph(ax, x_axis = x_axis, y_labels = ('to_the_left' if j%3 == 0
                                                                else 'to_the_right' if j%3 == 2 
                                                                else 'without'), rescale = rescale, **graph_options[column_to_plot])
            ax.set_title(deps[i], 
                            x = 0.05, y = 0.85, va = 'top', ha = 'left',
                            fontsize = 24, fontweight = 'semibold', c = 'royalblue', family = 'sans',)
    ###########
    # Légende #
    ###########                   
        ax_leg = fig.add_subplot(gs00[2])
        ax_leg.set_axis_off() 
        ax_leg.legend(*ax.get_legend_handles_labels(),
                    bbox_to_anchor=[0.5, 0.5], loc='center', frameon=True,
                    labelspacing=0.5, handlelength=2, handletextpad=0.5, fontsize = 10,
                    title = graph_options[column_to_plot]['title'], title_fontsize = 11, 
                )
        plt.setp(ax_leg.get_legend().get_title(), multialignment='center')


    ##########
    # Région #
    ##########
        rescale = d.loc[(d.entity.isin([region, 'France']))
                        , column_to_plot].max() / graph_options[column_to_plot]['minloc'][-1]
        
        whole = 'with' if hosp else 'without'
        ax = fig.add_subplot(gs10[0,0])
        plot_three_curves(ax, d, region, column_to_plot, whole = whole, **graph_options[column_to_plot])
        format_graph(ax, x_axis = 'complete', y_labels = 'to_the_left', rescale = rescale,**graph_options[column_to_plot])
        ax.set_title(region, 
                            x = 0, y = 0.95, va = 'bottom', ha = 'left',
                            fontsize = 26, fontweight = 'semibold', c = 'royalblue', family = 'sans',)
    ##########
    # France #
    ##########
        ax = fig.add_subplot(gs10[0,1])
        plot_three_curves(ax, d, 'France', column_to_plot, whole = whole, **graph_options[column_to_plot])
        format_graph(ax, x_axis = 'complete', y_labels = 'to_the_right', rescale = rescale, **graph_options[column_to_plot])
        ax.set_title('France', 
                            x = 0, y = 0.95, 
                            fontsize = 22, fontweight = 'semibold',
                            va = 'bottom', ha = 'left',
                            c = 'royalblue', family = 'sans'
                            )

        # fig.subplots_adjust(left=0.04,
        #                     right=0.96, 
        #                     bottom=0.09, 
        #                     top=0.965, 
        #                     wspace=0.07, 
        #                     hspace=0.1) #Enough space for title


    ##############
    # Save files #
    ##############
        dir_PNG = '{output_dir}Type3/{region}/'.format(
            output_dir = output_dir, 
            region = region)
        fig_id = '{region}-{extension}'.format(region = region, extension = graph_options[column_to_plot]["fname_extension"])
        save_output(fig, dir_PNG, fig_id)

def fig_type4(d, region):
        """
        d dataframe 
        plots all indicators for one region (region)
        """

    #####
    # layout
    #
        nrows = 4
        ncols = 4
        fig = plt.figure(constrained_layout=True, figsize = (12, 8))
        gs0 = fig.add_gridspec(1, 3, width_ratios = [8, 1, 8]) #gauche et droite
        gs00 = gs0[0,0].subgridspec(4, 1,  hspace = 0.2, ) 
        gs01 = gs0[0,2].subgridspec(4, 1,  hspace=0.2) 

    ########
    # Note #
    ########
        decomposition_clage = 'En {region} : {whole} millions d\'habitants, \
dont + de 60 ans : {class_older} millions, 30 à 59 ans : {class_middle} millions et \
0 à 29 ans : {class_younger} millions'.format(region = region, **pops_regs_str[region])
        
        fig.suptitle('@E_Dmz - Données Santé Publique France ({date})\n{decomposition_clage}'
            .format(date = DATE[1],
                    decomposition_clage = decomposition_clage,
                    ),
                    x = 0.035, y = -.03 -0.015 * (5 - nrows), ha = 'left', va = 'top',                 
                    c = 'black', family = 'sans', fontsize = 9,
                        )

        
        for i, column_to_plot in enumerate(['taux de tests hebdo', 'incidence hebdo', 'taux de positifs hebdo', 'taux dose 1', ]):
            ax = fig.add_subplot(gs00[i,0])
            plot_three_curves(ax, d, region, column_to_plot, **graph_options[column_to_plot])
            x_axis = 'regular' if (i == 3) else 'without'
            format_graph(ax, x_axis = x_axis, y_labels = 'to_the_left', rescale = 1, **graph_options[column_to_plot])
            if i == 0:
                ax.set_title(region, x = 0.02, y = .95, loc = 'left', 
                 fontsize = 22, c = 'royalblue', fontweight='semibold')
            #####
            # Légende
            #
            ax.legend(bbox_to_anchor=[1.1, 0], loc='lower left', frameon=True,
                    labelspacing=0.5, handlelength=2, handletextpad=0.5, fontsize = 11,     
                    title = graph_options[column_to_plot]['title'], title_fontsize = 10,
                    )
            plt.setp(ax.get_legend().get_title(), multialignment='center')

        for i, column_to_plot in enumerate(['taux hosp', 'taux rea', 'taux décès', 'taux complet']):
            ax = fig.add_subplot(gs01[i,0])
            plot_three_curves(ax, d, region, column_to_plot, **graph_options[column_to_plot])
            x_axis = 'regular' if (i == 3) else 'without'
            format_graph(ax, x_axis = x_axis, y_labels = 'to_the_left', rescale = 1, **graph_options[column_to_plot])
            if i == 0:
                ax.set_title(' ', x = 0.02, y = .95, loc = 'left', 
                 fontsize = 22, c = 'royalblue', fontweight='semibold')
            #####
            # Légende
            #
            ax.legend(bbox_to_anchor=[1.1, 0], loc='lower left', frameon=True,
                    labelspacing=0.5, handlelength=2, handletextpad=0.5, fontsize = 11,     
                    title = graph_options[column_to_plot]['title'], title_fontsize = 10,
                    )
            plt.setp(ax.get_legend().get_title(), multialignment='center')
        
    ##############
    # Save files #
    ##############
        dir_PNG = '{output_dir}Type4/'.format(
            output_dir = output_dir, 
            )
        fig_id = '{region}'.format(region = region)
        save_output(fig, dir_PNG, fig_id)