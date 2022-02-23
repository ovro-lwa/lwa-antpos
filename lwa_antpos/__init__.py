__all__ = ['reading', 'station', 'lwa_cnf', 'lwa_df', 'antnames']

import dsautils.cnf as cnf
from pkg_resources import resource_filename
from . import reading

CNFCONF = resource_filename("lwa_antpos", "data/cnfConfig.yml")
# TODO: eventually my_cnf can be read from etcd here
try:
    lwa_df = reading.read_antpos_etcd()
    print('Read antpos from etcd')
except:
    lwa_df = reading.read_antpos_xlsx()
    print('Read antpos from xlsx file in repo')

if 'online' in lwa_df.columns:
    antnames = lwa_df[lwa_df.online].index
else:
    antnames = lwa_df.index

dds = {'ant': {}}
for ind in antnames:
    dd = lwa_df.loc[ind]
    dds['ant'][ind] = dd
lwa_cnf = cnf.Conf(data=dds, cnf_conf=CNFCONF)
