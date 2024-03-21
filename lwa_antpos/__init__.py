__all__ = ['reading', 'station', 'lwa_cnf', 'lwa_df', 'antnames', 'mapping']

try:
    import dsautils.cnf as cnf
except ModuleNotFoundError:
    print('dsautils.cnf not found. skipping...')
from pkg_resources import resource_filename
from . import reading

CNFCONF = resource_filename("lwa_antpos", "data/cnfConfig.yml")
# TODO: eventually my_cnf can be read from etcd here
try:
    lwa_df = reading.read_antpos()
    print('Read antpos from default source')
except:
    try:
        lwa_df = reading.read_antpos_yaml()
        print('Failed with default source. Forcing to yaml...')
    except:
        try:
            lwa_df = reading.read_antpos_etcd()
            print('Failed with default source. Forcing to etcd...')
        except:
            lwa_df = None
            print('Cannot read antpos')

if lwa_df is not None:
    if 'online' in lwa_df.columns:
        antnames = lwa_df[lwa_df.online == 'YES'].index
    else:
        antnames = lwa_df.index

        dds = {'ant': {}}
        for ind in antnames:
            dd = lwa_df.loc[ind]
            dds['ant'][ind] = dd
            assert dd.corr_num in range(352), "corr_num is assumed to be in range(352)"

    try:
        lwa_cnf = cnf.Conf(data=dds, cnf_conf=CNFCONF)
    except NameError:
        pass
