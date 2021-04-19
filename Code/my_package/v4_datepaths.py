import time
import datetime as dt
import os
import glob
import shutil

def date(days = 0):
    """
    days: int, days before today (default = 0)
    returns: tuple of str, date in two string format: %Y-%m-%d and %d/%m/%Y
    """
    day = dt.date.today() - dt.timedelta(days = days)
    date_0 = day.strftime("%Y-%m-%d")
    date_1 = day.strftime("%d/%m/%Y")
    return date_0, date_1

def retrieve_data(dataset):
    """
    date_of_choice: string, date of choice %Y-%m-%d 
    dataset: string, target dataset
    version: string, version of code file
    returns: tuple of strings, path to data file, prefix path to temp files
    """

    ## Retrieve data file name in Data directory
    fname_format = '../Data/{dataset}-{date_choice}-??h??.csv'.format(
                dataset = dataset, date_choice = DATE_CHOICE[0])
    try: 
        fname = glob.glob(fname_format)[0]
    except: 
        print('There is no file {}'.format(fname_format))
        return 

    path_temp = './Temp/{version}/{prefix}'.format(
                version = VERSION, prefix = fname[8:-4])
    
    return fname, path_temp

def retrieve_temp(dataset, extension):
    """
    date_of_choice: string, date of choice %Y-%m-%d 
    dataset: string, target dataset
    extension: string, eg 'tot' or 'tot-3C
    version: string, version of code file
    returns: path to temp file
    """
    fname_format = './Temp/{version}/{dataset}-{date_choice}-??h??-{extension}.csv'.format(
                version = VERSION, dataset = dataset, date_choice = DATE_CHOICE[0], extension = extension)
    try: 
        fname = glob.glob(fname_format)[0]
    except: 
        print('There is no file {}'.format(fname_format))
        return
    print(fname)
    return fname

def save_output(fig, dir_PNG, suffix):
    
    dir_SVG = dir_PNG + 'SVG/'
    dir_PDF = dir_PNG + 'PDF/'
    
    if not os.path.exists(dir_PNG):
        os.makedirs(dir_PNG)
    if not os.path.exists(dir_PDF):
        os.makedirs(dir_PDF)
    if not os.path.exists(dir_SVG):
        os.makedirs(dir_SVG)


    fname_PNG = dir_PNG + suffix + '.png'
    fname_PDF = dir_PDF + suffix + '.pdf'
    fname_SVG = dir_SVG + suffix + '.svg'

    fig.savefig(fname_PNG, bbox_inches = 'tight', pad_inches = 0.1)
    fig.savefig(fname_PDF, bbox_inches = 'tight', pad_inches = 0.1)  
    fig.savefig(fname_SVG, bbox_inches = 'tight', pad_inches = 0.5) 

    return

#### Script

VERSION = 'v4'

## TODAY and DATE_CHOICE are tuples
TODAY = date()

days = input('Today is {}. Retrieve data from how many days? '.format(TODAY[1]))
if not days:
    days = 1
else:
    days = int(days)
DATE_CHOICE = date(days)
print('Ok, will retrieve data from {}'.format(DATE_CHOICE[1]))

## Setup Temp directory
temp_dir = './Temp/{}'.format(VERSION)
try: 
    os.mkdir(temp_dir)
except: pass

## Setup Output directory
output_dir = '../Output/Archives_v4/{version}-{date_choice}-{today}/'.format(
            version = VERSION, date_choice = DATE_CHOICE[0], today = TODAY[0])
try: os.mkdir(output_dir)
except: pass

def copy_to_main_output_dir(output_dir = output_dir):
    for root, dirs, files in os.walk(output_dir[:-1]):  # replace the . with your starting directory
        for file in files:
            path_file = os.path.join(root,file)
            shutil.copy2(path_file,'../Ouput/')