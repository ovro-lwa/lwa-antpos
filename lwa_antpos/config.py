import dsautils.cnf as cnf
from pkg_resources import resource_filename
from . import reading

__all__ = ['lwa_cnf']

CNFCONF = resource_filename("lwa_antpos", "data/cnfConfig.yml")
# TODO: eventually my_cnf can be read from etcd here
df = reading.read_antpos_xlsx()
dd = {'ant': df.set_index('Name'), 'fpga': df.set_index('FPGA')}
lwa_cnf = cnf.Conf(data=dd, cnf_conf=CNFCONF)


def antenna(name):
    """ Get metadata for one antenna from datafram.
    """

    df_ant = lwa_cnf.get('ant')
    
    return df_ant.loc[name]


def baseline(a1, a2):
    """ Load xlsx file and return ant metadata.
    returns metadata as pandas dataframe indexed by antenna.
    TODO: add argument to select antennas
    """

    df_ant = lwa_cnf.get('ant')
    
    d1 = df_ant.loc[a1]
    d2 = df_ant.loc[a2]
    return d1, d2


def fpga(number):
    """ Get metadata for an FPGA as dataframe.
    """

    df_fpga = lwa_cnf.get('fpga')

    return df_fpga.loc[number]

