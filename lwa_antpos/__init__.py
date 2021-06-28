__all__ = ['reading', 'station', 'lwa_cnf', 'lwa_df']

import dsautils.cnf as cnf
from pkg_resources import resource_filename
from . import reading

CNFCONF = resource_filename("lwa_antpos", "data/cnfConfig.yml")
# TODO: eventually my_cnf can be read from etcd here
lwa_df = reading.read_antpos_xlsx()
dds = {'ant': {}}
for ind in lwa_df.index:
    dd = lwa_df.loc[ind]
    dds['ant'][ind] = dd
lwa_cnf = cnf.Conf(data=dds, cnf_conf=CNFCONF)
