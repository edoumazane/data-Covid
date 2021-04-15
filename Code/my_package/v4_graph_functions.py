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

from my_package.v4_datepaths import TODAY, VERSION, output_dir
from my_package.v4_datepaths import DATE_CHOICE as DATE
from my_package.v4_dicts import reg_2lignes, reg2dep, dep_name, deps_outlay_fig_synthese

from my_package.v4_graph_options import graph_options

# try: os.mkdir('../Output/{}-{}-{}'.format(VERSION, DATE_CHOICE[0], TODAY[0]))
# except: pass
# try: os.mkdir('../Output/{}-{}-{}/PNG'.format(version, DATE_CHOICE[0], TODAY[0]))
# except: pass
# try: os.mkdir('../Output/{}-{}-{}/PDF'.format(version, DATE_CHOICE[0], TODAY[0]))
# except: pass

def format_graph(ax, x_axis = 'complete', y_labels = "to_the_left", **kwargs):
    """
    formats the graph
    ax: axes object
    ymin, ymax: integer
    x_axis : 'without', 'regular', 'complete'
    y_labels : 'without', 'to_the_left', 'to_the_right
    **kwargs: graph_options
    """
    ax.patch.set_alpha(0)
    ymin = kwargs['ymin']
    ymax = kwargs['ymax']

    # default settings
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    # y axis default
    ax.set_ylim(ymin, ymax)
    ax.grid(axis = 'y')
    # y axis conditional

    if y_labels == "without":
        ax.tick_params(axis='y', left = False, labelsize = 9) 
        ax.set_yticklabels([])

    if y_labels == "to_the_left":
        ax.tick_params(axis='y', left = False, labelsize = 9)

    if y_labels == "to_the_right":
        ax.tick_params(axis='y', left = False,
            labelright = True, labelleft = False, labelsize = 9)
        
    # x axis and vertical lines default
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
    # x axis conditional

    if x_axis == 'without':
        ax.tick_params(axis='x', bottom = False)
        ax.set_xticklabels([])

    if x_axis == 'regular':
        ax.tick_params(axis='x', bottom = True,
                   labelsize = 9)
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

    if x_axis == 'complete':
        ax.tick_params(axis='x', bottom = True,
                labelsize = 9)
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

def plot_three_curves(ax, d, entity, column_to_plot, **kwargs):
    """
    """
    main_color = kwargs['main_color']

    dplot = d.loc[d.entity == entity].loc[d.three_class == '0-29']
    ax.plot(dplot.jour, dplot[column_to_plot], c = "firebrick", linewidth = 1, label = '0-29 ans')
    
    dplot = d.loc[d.entity == entity].loc[d.three_class == '30-59']
    ax.plot(dplot.jour, dplot[column_to_plot], c = "black", linewidth = 1.5, label = '30-59 ans')

    dplot = d.loc[d.entity == entity].loc[d.three_class == '60+']
    ax.plot(dplot.jour, dplot[column_to_plot], c = main_color, linewidth = 3, label = '60 ans et +')

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

    #     Première colonne : France et légende
    col = 0
    ax = axs[row * ncol + col]
    plot_three_curves(ax, d, "France", column_to_plot, **graph_options[column_to_plot])
    format_graph(ax,
            x_axis = ('regular' if (row == nrow - 1) else 'without'), 
            y_labels = ('to_the_left' if (col == 0) else 'to_the_right' if (col == ncol - 1) else 'without'), 
            **graph_options[column_to_plot])
    # Légende
    (ax.legend(bbox_to_anchor=[1.55, .45], 
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

    # Titre première ligne : "France entière"
    if (row == 0):
        ax.set_title('France', 
                     x = 0.5, y = 1.05, 
                     fontdict = {'fontsize': 24,
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
                         fontdict = {'fontsize': 16,
                                     'fontweight' : 'semibold',
                                     'verticalalignment': 'center',
                                     'horizontalalignment': 'center'},
                     c = 'royalblue', family = 'sans')

def fig_type1(d, regions, regions_ordered, fig_id):

    ncol = len(regions) + 2
    fig, axs = plt.subplots(5, ncol, figsize = (2.5 * ncol, 10))
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
                        bottom=0.1, 
                        top=0.95, 
                        wspace=0.07, 
                        hspace=0.05)
    
    fig.suptitle('{fig_id}\n@E_Dmz - Données Santé Publique France ({date})'.format(fig_id = fig_id, date = DATE[1]),
                 x = 0.03, y = 0.045, ha = 'left',                     
                     fontdict = {'fontsize': 8,
                                     'fontweight' : 'normal',
                                     'verticalalignment': 'center',
                                     'horizontalalignment': 'left'},
                     c = 'black', family = 'sans',
                    )
    
    dir_PNG = output_dir + 'Type1/'
    dir_PDF = dir_PNG + 'PDF/'
    
    if not os.path.exists(dir_PNG):
        os.makedirs(dir_PNG)
    if not os.path.exists(dir_PDF):
        os.makedirs(dir_PDF)

    fname_PDF = dir_PDF + 'regions-{}.pdf'.format(fig_id)
    fname_PNG = dir_PNG + 'regions-{}.png'.format(fig_id)

          
    fig.savefig(fname_PDF, pad_inches = 0)  
    fig.savefig(fname_PNG, pad_inches = 0)

def fig_type2(d, column_to_plot, regions_ordered):

    nrow, ncol = 4, 4
    fig, axs = plt.subplots(nrow, ncol, figsize = (4*ncol, 13))
    axs = axs.ravel()

    row, col = 0, 0
    ax = axs[0]
    plot_three_curves(ax, d, "France", column_to_plot, **graph_options[column_to_plot])
    format_graph(ax, x_axis='complete', **graph_options[column_to_plot])
    
    # Légende
    (ax.legend(bbox_to_anchor=[1.6, .45], 
              loc='center',
              labelspacing=0.5,       
              handlelength=2, 
              handletextpad=0.5,
              frameon=True,
              fontsize = 14,
              title = '{}\n'.format(DATE[1]) + graph_options[column_to_plot]['title'],
              title_fontsize = 16,
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
                     fontsize = 18, c = 'royalblue', fontweight='normal', family = 'sans')

        fig.subplots_adjust(left=0.05,
                        right=0.95, 
                        bottom=0.2, 
                        top=0.9, 
                        wspace=0.12, 
                        hspace=0.2)
    fig.suptitle('@E_Dmz - Données Santé Publique France ({})'.format(DATE[1]), 
                x = 0.05, y = 0.12, ha = 'left',
                fontdict = {'fontsize': 12,
                                'fontweight' : 'normal',
                                'verticalalignment': 'center',
                                'horizontalalignment': 'left'},
                c = 'black', family = 'sans',
                )

    dir_PNG = output_dir + 'Type2/'
    dir_PDF = dir_PNG + 'PDF/'
    
    if not os.path.exists(dir_PNG):
        os.makedirs(dir_PNG)
    if not os.path.exists(dir_PDF):
        os.makedirs(dir_PDF)

    fname_PNG = dir_PNG + 'fig{}.png'.format(
                            graph_options[column_to_plot]['fname_extension'])
    fname_PDF = dir_PDF + 'fig{}.pdf'.format(
                            graph_options[column_to_plot]['fname_extension'])

    fig.savefig(fname_PNG, pad_inches = 0)
    fig.savefig(fname_PDF, pad_inches = 0)  

def fig_type3(d, region, column_to_plot):
    
    deps = reg2dep[region]
    ndeps = len(deps)
    nrows = int(np.ceil((ndeps + 2) / 4))
    ncols = 4 
    
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


    fig = plt.figure(constrained_layout=False, figsize = (16, 2 * nrows + 4))
    gs0 = fig.add_gridspec(2, 1, hspace = 0.2, height_ratios=[1.5*nrows, 3])
    
    gs00 = gs0[0,0].subgridspec(ncols=ncols, nrows=nrows, wspace = 0.1, hspace = 0.05)
    


    for i,j in enumerate(deps_outlay_fig_synthese[ndeps]):
        #i number of graph, j number of axe
        ax = fig.add_subplot(gs00[j])
        plot_three_curves(ax, d, deps[i], column_to_plot, **graph_options[column_to_plot])
        format_graph(ax, x_axis = 'without', y_labels = ('to_the_left' if j%4 == 0 
                                                            else 'to_the_right' if j%4 == 3 
                                                            else 'without'), **graph_options[column_to_plot])
        ax.set_title(deps[i], 
                        x = 0.05, y = 0.85, 
                        fontdict = {'fontsize': 26,
                                        'fontweight' : 'semibold',
                                        'verticalalignment': 'top',
                                        'horizontalalignment': 'left'},
                        c = 'royalblue', family = 'sans'
                    )
    ax_leg = fig.add_subplot(gs00[3])
    ax_leg.set_axis_off() 
    (ax_leg.legend(*ax.get_legend_handles_labels(),
                bbox_to_anchor=[0, 0], 
                  loc='lower left',
                  labelspacing=0.5,       
                  handlelength=2, 
                  handletextpad=0.5,
                  frameon=True,
                  fontsize = 12,
                  title = graph_options[column_to_plot]['title'],
                  title_fontsize = 14,
                  )
            )
    
    
    gs10 = gs0[1,0].subgridspec(1, 2, wspace=0.1, hspace=0)
    ax = fig.add_subplot(gs10[0,0])
    plot_three_curves(ax, d, region, column_to_plot, **graph_options[column_to_plot])
    format_graph(ax, x_axis = 'complete', y_labels = 'to_the_left', **graph_options[column_to_plot])
    ax.set_title(region, 
                         x = 0.05, y = 0.9, 
                         fontdict = {'fontsize': 26,
                                         'fontweight' : 'semibold',
                                         'verticalalignment': 'bottom',
                                         'horizontalalignment': 'left'},
                         c = 'royalblue', family = 'sans'
                        )

    ax = fig.add_subplot(gs10[0,1])
    plot_three_curves(ax, d, 'France', column_to_plot, **graph_options[column_to_plot])
    format_graph(ax, x_axis = 'complete', y_labels = 'to_the_right', **graph_options[column_to_plot])
    ax.set_title('France', 
                         x = 0.05, y = 0.9, 
                         fontdict = {'fontsize': 24,
                                         'fontweight' : 'semibold',
                                         'verticalalignment': 'bottom',
                                         'horizontalalignment': 'left'},
                         c = 'royalblue', family = 'sans'
                        )
    
##
    dir_PNG = '{output_dir}Type3/{region}/'.format(
        output_dir = output_dir, 
        region = region)
    dir_PDF = dir_PNG + 'PDF/'
    
    if not os.path.exists(dir_PNG):
        os.makedirs(dir_PNG)
    if not os.path.exists(dir_PDF):
        os.makedirs(dir_PDF)

    fname = 'fig-{region}{indicateur}'.format(region = region,
                            indicateur = graph_options[column_to_plot]['fname_extension'])
    fname_PNG = dir_PNG + fname + '.png'
    fname_PDF = dir_PDF + fname + '.pdf'

    fig.savefig(fname_PNG, pad_inches = 0)
    fig.savefig(fname_PDF, pad_inches = 0) 

    # plt.clf() 

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
