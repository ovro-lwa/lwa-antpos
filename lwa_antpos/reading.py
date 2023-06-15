import yaml
import json
import pandas as pd
try:
    from dsautils import dsa_store
except ModuleNotFoundError:
    print('no etcd3 found. skipping...')
from pkg_resources import resource_filename

ls = dsa_store.DsaStore()
antposfile = resource_filename("lwa_antpos", "data/LWA-352 Antenna Status & System Configuration.xlsx")
# "data/LWA-352 Antenna Positions & System Status.xlsx"  # old name


def read_antpos_xlsx(filename=antposfile):
    """ Gets data from xlsx file and returns dataframe
    """

    df = pd.read_excel(filename, engine='openpyxl', header=1, usecols=lambda x: 'Unnamed' not in x)
    df.drop(index=0, inplace=True)  # descriptive header should be dropped
    df.drop(columns='dict_key', inplace=True)  # descriptive column should be dropped
    assert "antname" in df.columns
    df.set_index('antname', inplace=True)

    return df

def update_antpos_etcd():
    """ Read xlsx format file, restructure, and put in etcd.
    """

    from astropy import time
    from numpy import nan

    df = read_antpos_xlsx()
    df.reset_index(inplace=True)
    df.replace(nan, '', inplace=True)
    ls.put_dict('/cfg/system', {'lwacfg': df.to_dict(), 'time': time.Time.now().mjd})


def read_antpos_etcd():
    """ Gets data from etcd and returns dataframe
    """

    dds = ls.get_dict('/cfg/system') 
    df = pd.DataFrame.from_dict(dds['lwacfg'], orient='index')

    assert "antname" in df.columns
    df.set_index('antname', inplace=True)

    return df


def read_antpos_yaml(filename):
    """ Gets data from yaml and returns dataframe
    """

    with open(filename, 'r') as fp:
        dd = yaml.load(fp)

    df = pd.DataFrame.from_dict(dd, orient='index')
    assert "antname" in df.columns
    df.set_index('antname', inplace=True)

    return df
