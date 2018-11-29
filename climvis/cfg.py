"""This configuration module is a container for parameters and constants."""
import os
import platform
import configparser

#cru_dir = '/home/mowglie/disk/OGGM_INPUT/cru/'

def get_data_path():
    """ Get data path from .cruvis file in home directory.
    The file has to look like this:
    [PATH]
    cru_dir = /path/to/data/
    """
    homedir = os.path.expanduser('~')
    # Get operating system and define path to .cruvis file
    operatingsys = platform.platform()
    if 'Windows' in operatingsys:
        crufilepath = homedir + '\.cruvis'
    elif 'Linux' in operatingsys:
        crufilepath = homedir + '/.cruvis'
    else:
        raise('Operatingsystem unknown')
    # Read path to data from config-file
    config = configparser.ConfigParser()
    config.read(crufilepath)
    return config['PATH']['cru_dir']

cru_dir = get_data_path()  
cru_tmp_file = cru_dir + 'cru_ts4.01.1901.2016.tmp.dat.nc'
cru_pre_file = cru_dir + 'cru_ts4.01.1901.2016.pre.dat.nc'
cru_topo_file = cru_dir + 'cru_cl1_topography.nc'

bdir = os.path.dirname(__file__)
html_tpl = os.path.join(bdir, 'data', 'template.html')
world_cities = os.path.join(bdir, 'data', 'world_cities.csv')

default_zoom = 8
