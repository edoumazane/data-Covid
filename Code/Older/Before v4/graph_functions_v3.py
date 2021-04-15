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

from dicts_paths_v3 import today, date_choice, date_text, reg_2lignes, dep_name

fname = 'graph_options.json'
with open(fname, 'r') as f:
    graph_options = json.loads(f.read())

version = '5Lv3'

try: os.mkdir('../Output/{}-{}-{}'.format(version, date_choice, today))
except: pass
try: os.mkdir('../Output/{}-{}-{}/PNG'.format(version, date_choice, today))
except: pass
try: os.mkdir('../Output/{}-{}-{}/PDF'.format(version, date_choice, today))
except: pass

path_output = '../Output/{}-{}-{}/'.format(version, date_choice, today)

def format_graph(ax, x_axis = 'complete', y_labels = "to_the_left", **kwargs):
    """
    formats the graph
    ax: axes object
    ymin, ymax: integer
    x_axis : 'without', 'regular', 'complete'
    y_labels : 'without', 'to_the_left', 'to_the_right
    first_row... last_col: boolean
    """

    ymin = kwargs['ymin']
    ymax = kwargs['ymax']


    # default settings
    ax.patch.set_alpha(0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    # y axis and grid
    ax.set_ylim(ymin, ymax)
    ax.grid(axis = 'y')
    
    
    # x axis and vertical lines
    ax.set_xlim(dt.datetime(2020, 3, 1), 
                dt.datetime(2021, 6, 1))

    ax.axvline(dt.datetime(2021, 1, 1), 
               ymin = 0, ymax = .95, 
               c = 'black', 
               linewidth = 0.5,
               linestyle = '--')
    ax.axvspan(dt.datetime(2020, 3, 17), 
               dt.datetime(2020, 5, 10),
               ymin = 0, ymax = .95,
               alpha=0.15, color='gray')
    ax.axvspan(dt.datetime(2020, 10, 30), 
               dt.datetime(2020, 12, 15),
               ymin = 0, ymax = .95,
               alpha=0.15, color='gray')
    ax.axvspan(dt.datetime(2021, 4, 5), 
               dt.datetime(2021, 5, 2),
               ymin = 0, ymax = .95,
               alpha=0.15, color='gray')

    # Last column 
    if y_labels == "to_the_left":
        ax.tick_params(axis='y', left = False, labelsize = 8)

    if y_labels == "to_the_right":
        ax.tick_params(axis='y', left = False, labelright = True, labelleft = False, labelsize = 8)

        
    # Other columns
    if y_labels == "without":
        ax.tick_params(axis='y', left = False, labelsize = 8) 
        ax.set_yticklabels([])
        
    # Last row
    if x_axis == 'regular':
        ax.tick_params(axis='x', bottom = True,
                   labelsize = 10)
        locs = []
        for i in range(8):
            locs.append(dt.datetime(2020, 3 + 2*i, 1) if 2 * i <= 9
                            else dt.datetime(2021, 2*i - 9, 1)
                       )
        labels = ['mars','mai', 'juil.', 
                 'sept.',  'nov.', 
                 'janv.', 'mars', 
                  'mai']
        ax.set_xticks(locs)
        ax.set_xticklabels(labels)
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor") 

    elif x_axis == 'complete':
        ax.tick_params(axis='x', bottom = True,
                labelsize = 10)
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
            
    elif x_axis == 'without':
        ax.tick_params(axis='x', bottom = False)
        ax.set_xticklabels([])

def plot_three_curves(ax, d, entity, column_to_plot, **kwargs):
    """
    """
    main_color = kwargs['main_color']

    dplot = d.loc[d.entity == entity].loc[d.three_class == '0-29']
    ax.plot(dplot.jour, dplot[column_to_plot], c = "firebrick", linewidth = 1, label = '0-29 ans')
    
    dplot = d.loc[d.entity == entity].loc[d.three_class == '30-59']
    ax.plot(dplot.jour, dplot[column_to_plot], c = "black", linewidth = 2, label = '30-59 ans')

    dplot = d.loc[d.entity == entity].loc[d.three_class == '60+']
    ax.plot(dplot.jour, dplot[column_to_plot], c = main_color, linewidth = 4, label = '60 ans et +')

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
                    fontdict = {'fontsize': 22,
                                     'fontweight' : 'semibold',
                                     'verticalalignment': 'center',
                                     'horizontalalignment': 'center'},
                     c = 'royalblue', family = 'sans')

def figure_line(row, nrow, axs, d, column_to_plot, regions):
    """
    """
    
    ncol = len(regions) + 2

    #     Première colonne : France entière et légende
    col = 0
    ax = axs[row * ncol + col]
    plot_three_curves(ax, d, "France entière", column_to_plot, **graph_options[column_to_plot])
    format_graph(ax,
            x_axis = ('regular' if (row == nrow - 1) else 'without'), 
            y_labels = ('to_the_left' if (col == 0) else 'to_the_right' if (col == ncol - 1) else 'without'), 
            **graph_options[column_to_plot])
    # Légende
    (ax.legend(bbox_to_anchor=[1.6, .45], 
              loc='center',
              labelspacing=0.5,       
              handlelength=2, 
              handletextpad=0.5,
              frameon=True,
              fontsize = 14,
              title = graph_options[column_to_plot]['title'],
              title_fontsize = 14,
              )
        )
    plt.setp(ax.get_legend().get_title(), multialignment='center')

    # Titre première ligne : "France entière"
    if (row == 0):
        ax.set_title('France', 
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
        plot_three_curves(ax, d, region, column_to_plot, **graph_options[column_to_plot])
        format_graph(ax,
                x_axis = ('regular' if (row == nrow -1 ) else 'without'), 
                y_labels = ('to_the_left' if (col == 0) else 'to_the_right' if (col == ncol - 1) else 'without'),
                **graph_options[column_to_plot])
        
        # Titre première ligne : nom des régions       
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
    
    for i, column_to_plot in enumerate([
        "taux de test hebdo",
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
    
    fig.subplots_adjust(left=0.05,
                        right=0.95, 
                        bottom=0.2, 
                        top=0.9, 
                        wspace=0.1, 
                        hspace=0.15)
    
    fig.suptitle('{num} / 3 \n@E_Dmz - Données Santé Publique France ({date})\nLes régions sont classées selon le taux d\'hospitalisation pendant la semaine précédente :\n{regs}'.format(num = numero, date = date_text, regs = ' / '.join(regions_ordered),), 
                 x = 0.05, y = 0.12, ha = 'left',                     
                     fontdict = {'fontsize': 14,
                                     'fontweight' : 'normal',
                                     'verticalalignment': 'center',
                                     'horizontalalignment': 'left'},
                     c = 'black', family = 'sans',
                    )

    fname = path_output + 'PDF/regions_' + str(numero) + '.pdf'
    fig.savefig(fname, pad_inches = 0)
    fname = path_output + 'PNG/regions_' + str(numero) + '.png'
    fig.savefig(fname, pad_inches = 0)

def produce_fig(d, column_to_plot, regions_ordered):

    nrow, ncol = 4, 4
    fig, axs = plt.subplots(nrow, ncol, figsize = (4*ncol, 13))
    axs = axs.ravel()

    row, col = 0, 0
    ax = axs[0]
    plot_three_curves(ax, d, "France entière", column_to_plot, **graph_options[column_to_plot])
    format_graph(ax, x_axis='complete', **graph_options[column_to_plot])
    
    # Légende
    (ax.legend(bbox_to_anchor=[1.6, .45], 
              loc='center',
              labelspacing=0.5,       
              handlelength=2, 
              handletextpad=0.5,
              frameon=True,
              fontsize = 14,
              title = '{}\n'.format(date_text) + graph_options[column_to_plot]['title'],
              title_fontsize = 14,
              )
        )
    plt.setp(ax.get_legend().get_title(), multialignment='center')
    ax.set_title('France', x = 0.02, y = .95, loc = 'left', 
                 fontsize = 22, c = 'royalblue', fontweight='semibold')
    ax = axs[1]
    ax.set_axis_off() 

    for i, region in enumerate(regions_ordered):

        ax = axs[i+2]
        row = (i+2)//ncol
        col = (i+2)%ncol

        plot_three_curves(ax, d, region, column_to_plot, **graph_options[column_to_plot])
        format_graph(ax, 
                x_axis='without', 
                y_labels = ('to_the_left' if (col == 0) else 'to_the_right' if (col == ncol - 1) else 'without'),
                **graph_options[column_to_plot])

        ax.set_title(region, x = 0.02, y = -0.15, loc = 'left', 
                     fontsize = 16, c = 'royalblue', fontweight='normal', family = 'sans')

        fig.subplots_adjust(left=0.05,
                        right=0.95, 
                        bottom=0.2, 
                        top=0.9, 
                        wspace=0.1, 
                        hspace=0.2)

    fig.suptitle('@E_Dmz - Données Santé Publique France ({})'.format(date_text), 
                x = 0.05, y = 0.12, ha = 'left',
                fontdict = {'fontsize': 12,
                                'fontweight' : 'normal',
                                'verticalalignment': 'center',
                                'horizontalalignment': 'left'},
                c = 'black', family = 'sans',
                )

    fname = path_output + 'PDF/fig{}.pdf'.format(graph_options[column_to_plot]['fname_extension'])
    fig.savefig(fname, pad_inches = 0)
    fname = path_output + 'PNG/fig{}.png'.format(graph_options[column_to_plot]['fname_extension'])
    fig.savefig(fname, pad_inches = 0)

# def produce_fig_dep(d, deps):
#     ncol = max(1, min(4, len(deps)//2))
#     nrow = math.ceil(len(deps)/ncol)
#     fig, axs = plt.subplots(nrow, ncol, figsize = (4*ncol,3*nrow))
#     axs = axs.ravel()
#     for ax in axs: ax.set_axis_off()
#     ax.patch.set_alpha(0)
#     for i, dep in enumerate(deps):
#         ax = axs[i]
#         # default settings
#         ax.patch.set_alpha(0)
#         ax.spines['top'].set_visible(False)
#         ax.spines['right'].set_visible(False)
#         ax.spines['bottom'].set_visible(False)
#         ax.spines['left'].set_visible(False)
        
#         # y axis and grid
#         ax.set_ylim(-40, 1190)
#         ax.tick_params(axis='y', left = False, labelsize = 12)
        
#         # x axis and vertical lines
#         ax.set_xlim(dt.datetime(2020, 3, 1), 
#                     dt.datetime(2021, 6, 1))
#         ax.axvline(dt.datetime(2021, 1, 1), 
#                 ymin = 0, ymax = .9, 
#                 c = 'black', 
#                 linewidth = 0.5,
#                 linestyle = '--')
#         ax.axvspan(dt.datetime(2020, 3, 17), 
#                 dt.datetime(2020, 5, 10),
#                 ymin = 0, ymax = .7,
#                 alpha=0.15, color='gray')
#         ax.axvspan(dt.datetime(2020, 10, 30), 
#                 dt.datetime(2020, 12, 15),
#                 ymin = 0, ymax = .9,
#                 alpha=0.15, color='gray')
#         ax.axvspan(dt.datetime(2021, 4, 5), 
#                 dt.datetime(2021, 5, 2),
#                 ymin = 0, ymax = .9,
#                 alpha=0.15, color='gray')

#         plot_three_curves(ax, d, dep, 'incidence hebdo', "darkturquoise")
#         ax.set_axis_off()
#         ax.set_title(dep, loc = 'left', y = 0.7, fontsize = 30, fontweight = 'semibold', c = "darkturquoise")
#         ax.set_title(dep_name[dep], x = -0.05, y = 0, rotation = 90, fontsize = 16)
