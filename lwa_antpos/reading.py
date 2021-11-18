import yaml
import json
import pandas as pd
import etcd3
from pkg_resources import resource_filename
from mnc.common import ETCD_HOST, ETCD_PORT
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


def read_antpos_etcd(host=ETCD_HOST, port=ETCD_PORT):
    """ Gets data from etcd and returns dataframe
    """

    le = etcd3.client(host, port)
    dds, _ = le.get('/cfg/system') 
    dd = json.loads(dds.decode("utf-8"))['lwacfg']
    
    df = pd.DataFrame.from_dict(dd, orient='index')
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
