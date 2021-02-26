import dsautils.cnf as cnf
from pkg_resources import resource_filename
from . import reading

CNFCONF = resource_filename("lwa_antpos", "data/cnfConfig.yml")
# TODO: eventually my_cnf can be read from etcd here
df = reading.read_antpos_xlsx()
dd = {'ant': df, 'fpga': df}
my_cnf = cnf.Conf(data=dd, cnf_conf=CNFCONF)


def antenna(name):
    """ Load xlsx file and return ant metadata.
    returns metadata as pandas dataframe indexed by antenna.
    TODO: add argument to select antennas
    """

    df_ant = my_cnf.get('ant').set_index('Name')
    
    return df_ant.loc[name]


def fpga(number):
    """ Load xlsx file and return fpga metadata.
    returns metadata as pandas dataframe indexed by fpga.
    """

    df_fpga = my_cnf.get('fpga').set_index('FPGA')
    return df_fpga.loc[number]

