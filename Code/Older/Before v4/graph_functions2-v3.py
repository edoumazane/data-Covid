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

from graph_functions_v3 import format_graph, plot_three_curves

def simple(ax, d, entity, column_to_plot):
    kwargs = graph_options[column_to_plot]
    plot_three_curves(ax, d, entity, column_to_plot, **kwargs)
    format_graph(ax, **kwargs)
    ax.set_title('{}: {}'.format(entity, column_to_plot), 
                    fontdict = {'fontsize': 22,
                                     'fontweight' : 'semibold',
                                     'verticalalignment': 'center',
                                     'horizontalalignment': 'center'},
                     c = 'royalblue', family = 'sans')
    return

