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

from dicts_paths_v1 import date, date_text, reg_2lignes, fname_output_synth, dep_name

def format_graph(ax, ymin, ymax, first_row = False, last_row = False, first_col = False, last_col = False, force_bottom = False, force_bottomless = False, alt_x = False):
    """
    formats the graph
    ax: axes object
    ymin, ymax: integer
    first_row... last_col: boolean
    """

    # default settings
    ax.patch.set_alpha(0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    # y axis and grid
    ax.set_ylim(ymin, ymax)
    ax.grid(axis = 'y')
    ax.tick_params(axis='y', left = False, labelsize = 12)
    
    # x axis and vertical lines
    ax.set_xlim(dt.datetime(2020, 3, 1), 
                dt.datetime(2021, 6, 1))
    ax.axvline(dt.datetime(2021, 1, 1), 
               ymin = 0, ymax = .9, 
               c = 'black', 
               linewidth = 0.5,
               linestyle = '--')
    ax.axvspan(dt.datetime(2020, 3, 17), 
               dt.datetime(2020, 5, 10),
               ymin = 0, ymax = .9,
               alpha=0.15, color='gray')
    ax.axvspan(dt.datetime(2020, 10, 30), 
               dt.datetime(2020, 12, 15),
               ymin = 0, ymax = .9,
               alpha=0.15, color='gray')
    ax.axvspan(dt.datetime(2021, 4, 5), 
               dt.datetime(2021, 5, 2),
               ymin = 0, ymax = .9,
               alpha=0.15, color='gray')

    # Last column 
    if last_col:
        ax.tick_params(axis='y', left = False, labelright = True, labelleft = False, labelsize = 12)
        
    # Other columns
    if (not first_col) and (not last_col):
        ax.set_yticklabels([])
        
    # Last row
    if (last_row and not force_bottomless) or (force_bottom):
        ax.tick_params(axis='x', bottom = True,
                   labelsize = 12)
        if alt_x:
            ax.tick_params(axis='x', bottom = True,
                   labelsize = 8)
        locs = []
        for i in range(8):
            locs.append(dt.datetime(2020, 3 + 2*i, 1) if 2 * i <= 9
                            else dt.datetime(2021, 2*i - 9, 1)
                       )
        labels = ['mars','mai', 'juil.', 
                 'sept.',  'nov.', 
                 'janv.', 'mars', 
                  'mai']
        if alt_x:
            locs = []
            for i in range(16):
                locs.append(dt.datetime(2020, 3 + i , 1) if i <= 9 
                            else dt.datetime(2021, i - 9, 1))
            labels = ['mars','avril', 'mai', 'juin', 'juil.', 
                     'août', 'sept.', 'oct.', 'nov.', 'déc.', 
                     'janv.', 'fév.', 'mars', 'avril', 
                      'mai', 'juin']
        ax.set_xticks(locs)
        ax.set_xticklabels(labels)
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor") 
            

    # Other rows
    else:
        ax.tick_params(axis='x', bottom = False)
        ax.set_xticklabels([])

def plot_three_curves(ax, d, entity, column_to_plot, main_color):
    """
    """
    dplot = d.loc[d.entity == entity].loc[d.three_class == '60+']
    ax.plot(dplot.jour, dplot[column_to_plot], c = main_color, linewidth = 4, label = '60+')

    dplot = d.loc[d.entity == entity].loc[d.three_class == '30-59']
    ax.plot(dplot.jour, dplot[column_to_plot], c = "black", linewidth = 2, label = '30-59')

    dplot = d.loc[d.entity == entity].loc[d.three_class == '0-29']
    ax.plot(dplot.jour, dplot[column_to_plot], c = "firebrick", linewidth = 1, label = '0-29')

def figure_line(row, nrow, axs, d, column_to_plot, main_color, ymin, ymax, title, regions):
    """
    """
    ncol = len(regions) + 2
    #     Première colonne : France entière et légende
    col = 0
    ax = axs[row * ncol + col]
    plot_three_curves(ax, d, "France entière", column_to_plot, main_color)
    # dplot = d.loc[d.entity == "France entière"].loc[d.three_class == '60+']
    # ax.plot(dplot.jour, dplot[column_to_plot], c = main_color, linewidth = 4, label = '60+')
    # dplot = d.loc[d.entity == "France entière"].loc[d.three_class == '30-59']
    # ax.plot(dplot.jour, dplot[column_to_plot], c = "black", linewidth = 2, label = '30-59')   
    # dplot = d.loc[d.entity == "France entière"].loc[d.three_class == '0-29']
    # ax.plot(dplot.jour, dplot[column_to_plot], c = "firebrick", linewidth = 1, label = '0-29')
    format_graph(ax, ymin, ymax, first_row = (row == 0), last_row = (row == nrow-1), first_col = (col == 0), last_col = (col == ncol-1))
    
    # Légende
    (ax.legend(bbox_to_anchor=[1.6, .45], 
              loc='center',
              labelspacing=0.5,       
              handlelength=2, 
              handletextpad=0.5,
              frameon=True,
              fontsize = 14,
              title = title,
              title_fontsize = 14,
              )
        )
    plt.setp(ax.get_legend().get_title(), multialignment='center')

    #     Première ligne : France entière
    if (row == 0):
        ax.set_title('France entière', 
                     x = 0.5, y = 1.05, 
                     fontdict = {'fontsize': 26,
                                     'fontweight' : 'semibold',
                                     'verticalalignment': 'center',
                                     'horizontalalignment': 'center'},
                     c = 'royalblue', family = 'sans'
                    )

    #     Deuxième colonne vide (pour la légende)
    ax = axs[row * ncol + 1]
    ax.set_axis_off() 

    #     Colonnes suivantes
    for i, region in enumerate(regions):
        col = 2 + i
        ax = axs[row * ncol + col]
        plot_three_curves(ax, d, region, column_to_plot, main_color)
        # dplot = d.loc[d.entity == reg].loc[d.three_class == '60+']
        # ax.plot(dplot.jour, dplot[column_to_plot], linewidth = 4, c = main_color )
        # dplot = d.loc[d.entity == reg].loc[d.three_class == '30-59']
        # ax.plot(dplot.jour, dplot[column_to_plot], c = "black", linewidth = 2)
        # dplot = d.loc[d.entity == reg].loc[d.three_class == '0-29']
        # ax.plot(dplot.jour, dplot[column_to_plot], c = "firebrick", linewidth = 1)
        format_graph(ax, ymin, ymax, first_row = (row == 0), last_row = (row == nrow-1), first_col = (col == 0), last_col = (col == ncol-1))
        
        #         Première ligne : nom des régions       
        if row == 0:
            ax.set_title(reg_2lignes[region], 
                         x = 0.5, y = 1.05, 
                         fontdict = {'fontsize': 22,
                                     'fontweight' : 'semibold',
                                     'verticalalignment': 'center',
                                     'horizontalalignment': 'center'},
                     c = 'royalblue', family = 'sans')

def produce_fig_lines(d, regions, regions_ordered, numero):

    ncol = len(regions) + 2
    
    fig, axs = plt.subplots(5, ncol, figsize = (4 * ncol, 16))
    axs = axs.ravel() 
    
    figure_line(row = 0,
                nrow = 5, 
                axs = axs,
                d = d,
                column_to_plot = "taux de test hebdo", 
                main_color = "gray", 
                ymin = -400, 
                ymax = 11900,
                title = 'Tests pratiqués par semaine\npour 100 000 personnes', 
                regions = regions)  
    
    figure_line(row = 1,
                nrow = 5, 
                axs = axs,
                d = d,
                column_to_plot = "incidence hebdo", 
                main_color = "darkturquoise", 
                ymin = -40, 
                ymax = 1190,
                title = 'Cas positifs par semaine\npour 100 000 personnes', 
                regions = regions)  
    
    figure_line(row = 2,
                nrow = 5, 
                axs = axs,
                d = d,
                column_to_plot = "taux hosp", 
                main_color = "mediumseagreen", 
                ymin = -15, 
                ymax = 379,
                title = 'Patients hospitalisés\npour 100 000 personnes', 
                regions = regions)
    
    figure_line(row = 3,
                nrow = 5, 
                axs = axs,
                d = d,
                column_to_plot = "taux rea", 
                main_color = "darksalmon", 
                ymin = -3, 
                ymax = 76,
                title = 'Patients en réanimation\npour 100 000 personnes', 
                regions = regions)
    
    figure_line(row = 4,
                nrow = 5, 
                axs = axs,
                d = d,
                column_to_plot = "taux décès", 
                main_color = "orchid", 
                ymin = -3, 
                ymax = 76,
                title = 'Décès à l\'hôpital par semaine\npour 100 000 personnes', 
                regions = regions)
    
    fig.subplots_adjust(left=0.05,
                        right=0.95, 
                        bottom=0.2, 
                        top=0.9, 
                        wspace=0.1, 
                        hspace=0.15)
    
    fig.suptitle('{} / 3 \n@E_Dmz - Données Santé Publique France ({})\nLes régions (métropolitaines) sont classées par taux d\'hospitalisation décroissant pendant la semaine qui précède :\n{}'.format(numero, date_text, ' / '.join(regions_ordered),), 
                 x = 0.05, y = 0.12, ha = 'left',
                     
                     fontdict = {'fontsize': 14,
                                     'fontweight' : 'normal',
                                     'verticalalignment': 'center',
                                     'horizontalalignment': 'left'},
                     c = 'black', family = 'sans',
                    )

    fname = fname_output_synth + '-5 lignes-regions-v2-'+ str(numero) + '.pdf'
    fig.savefig(fname, pad_inches = 0)
    fname = fname_output_synth + '-5 lignes-regions-v2-'+ str(numero) + '.png'
    fig.savefig(fname, pad_inches = 0)

def produce_fig(ymin, ymax, d, column_to_plot, main_color, title, regions_ordered, fname):

    nrow, ncol = 4, 4
    fig, axs = plt.subplots(nrow, ncol, figsize = (16,12))
    axs = axs.ravel()

    row, col = 0, 0
    ax = axs[0]
    plot_three_curves(ax, d, "France entière", column_to_plot, main_color)
    # format_graph(ax, row = 0, col = 0, ncol = 4, ymin = ymin, ymax = ymax)
    format_graph(ax, ymin, ymax, first_row = (row == 0), last_row = (row == nrow-1), first_col = (col == 0), last_col = (col == ncol-1), force_bottom=True, alt_x = True)
    
    # Légende
    (ax.legend(bbox_to_anchor=[1.6, .45], 
              loc='center',
              labelspacing=0.5,       
              handlelength=2, 
              handletextpad=0.5,
              frameon=True,
              fontsize = 14,
              title = title,
              title_fontsize = 14,
              )
        )
    plt.setp(ax.get_legend().get_title(), multialignment='center')
    
    ax.set_title('France entière', x = 0.02, y = .85, loc = 'left', 
                 fontsize = 22, c = 'royalblue', fontweight='semibold')

    ax = axs[1]
    ax.set_axis_off() 

    for i, region in enumerate(regions_ordered):

        ax = axs[i+2]
        row = (i+2)//ncol
        col = (i+2)%ncol

        plot_three_curves(ax, d, region, column_to_plot, main_color)
        # dplot = d.loc[d.entity == reg].loc[d.three_class == '60+']
        # ax.plot(dplot.jour, dplot[column_to_plot], c = main_color, linewidth = 4)
        # dplot = d.loc[d.entity == reg].loc[d.three_class == '30-59']
        # ax.plot(dplot.jour, dplot[column_to_plot], linewidth = 2, c = "black")
        # dplot = d.loc[d.entity == reg].loc[d.three_class == '0-30']
        # ax.plot(dplot.jour, dplot[column_to_plot], c = "firebrick", linewidth = 1)
        format_graph(ax, ymin, ymax, first_row = (row == 0), last_row = (row == nrow-1), first_col = (col == 0), last_col = (col == ncol-1), force_bottomless=True)

        ax.set_title(region, x = 0.02, y = -0.15, loc = 'left', 
                     fontsize = 16, c = 'royalblue', fontweight='normal', family = 'sans')

    # fig.subplots_adjust(left=0.1,
    #                     bottom=0.1, 
    #                     right=0.9, 
    #                     top=0.9, 
    #                     wspace=0.05, 
    #                     hspace=0.2)
        fig.subplots_adjust(left=0.05,
                        right=0.95, 
                        bottom=0.15, 
                        top=0.9, 
                        wspace=0.1, 
                        hspace=0.2)

    fig.suptitle('@E_Dmz - Données Santé Publique France ({})'.format(date_text), 
                x = 0.05, y = 0.1, ha = 'left',
                fontdict = {'fontsize': 12,
                                'fontweight' : 'normal',
                                'verticalalignment': 'center',
                                'horizontalalignment': 'left'},
                c = 'black', family = 'sans',
                )

    fname = fname + '.pdf'
    fig.savefig(fname, pad_inches = 0)
    fname = fname + '.png'
    fig.savefig(fname, pad_inches = 0)

def produce_fig_dep(d, deps):
    ncol = max(1, min(4, len(deps)//2))
    nrow = math.ceil(len(deps)/ncol)
    fig, axs = plt.subplots(nrow, ncol, figsize = (4*ncol,3*nrow))
    axs = axs.ravel()
    for ax in axs: ax.set_axis_off()
    ax.patch.set_alpha(0)
    for i, dep in enumerate(deps):
        ax = axs[i]
        # default settings
        ax.patch.set_alpha(0)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        
        # y axis and grid
        ax.set_ylim(-40, 1190)
        ax.tick_params(axis='y', left = False, labelsize = 12)
        
        # x axis and vertical lines
        ax.set_xlim(dt.datetime(2020, 3, 1), 
                    dt.datetime(2021, 6, 1))
        ax.axvline(dt.datetime(2021, 1, 1), 
                ymin = 0, ymax = .9, 
                c = 'black', 
                linewidth = 0.5,
                linestyle = '--')
        ax.axvspan(dt.datetime(2020, 3, 17), 
                dt.datetime(2020, 5, 10),
                ymin = 0, ymax = .7,
                alpha=0.15, color='gray')
        ax.axvspan(dt.datetime(2020, 10, 30), 
                dt.datetime(2020, 12, 15),
                ymin = 0, ymax = .9,
                alpha=0.15, color='gray')
        ax.axvspan(dt.datetime(2021, 4, 5), 
                dt.datetime(2021, 5, 2),
                ymin = 0, ymax = .9,
                alpha=0.15, color='gray')

        plot_three_curves(ax, d, dep, 'incidence hebdo', "darkturquoise")
        ax.set_axis_off()
        ax.set_title(dep, loc = 'left', y = 0.7, fontsize = 30, fontweight = 'semibold', c = "darkturquoise")
        ax.set_title(dep_name[dep], x = -0.05, y = 0, rotation = 90, fontsize = 16)
