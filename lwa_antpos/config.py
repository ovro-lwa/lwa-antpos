import dsautils.cnf as cnf
from pkg_resources import resource_filename
from . import reading

__all__ = ['lwa_cnf']

CNFCONF = resource_filename("lwa_antpos", "data/cnfConfig.yml")
# TODO: eventually my_cnf can be read from etcd here
df = reading.read_antpos_xlsx()
dds = {'ant': {}}
for ind in df.index:
    dd = df.loc[ind]
    dds['ant'][ind] = dd
lwa_cnf = cnf.Conf(data=dds, cnf_conf=CNFCONF)


def antenna(name):
    """ Get metadata for one antenna from datafram.
    """

    df_ant = lwa_cnf.get('ant')
    
    return df_ant.loc[name]


def baseline(a1, a2):
    """ Load xlsx file and return ant metadata.
    returns (x,y) tuples for a1 and a2 in units of meters relative to LWA-000.
    """

    df_ant = lwa_cnf.get('ant')
    
    d1 = df_ant.loc[a1]
    d2 = df_ant.loc[a2]
    return (d1.x, d1.y), (d2.x, d2.y)
