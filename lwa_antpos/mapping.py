from pandas import DataFrame
import numpy as np

from . import lwa_df

isodd = lambda a: bool(a % 2)


def filter_df(columnname, value):
    """ Gets full DataFrame and filters by columnname == value.
    Returns new DataFrame
    """

    return lwa_df.loc[lambda lwa_df: lwa_df[columnname] == value]


def get_unique(df, columnname):
    """ Return unique values for columnname in DataFrame
    """

    return np.unique(df[columnname].values)


def antpol_to_arx(antname, polname):
    """ Given antname and polname, return arx (address, channel) tuple
    """

    return tuple(lwa_df.loc[antname][['arx_address', f'pol{polname.lower()}_arx_channel']].to_list())


def antpol_to_digitizer(antname, polname):
    """ Given antname and polname, return (snap2loc, digitizer) tuple.
    Digitizer is remapped to 0-63 (fmc=0 => 0-31, fmc=1 => 32-63).
    """

    start = 32*lwa_df.loc[antname]['fmc']
    snap2loc, dig0 = lwa_df.loc[antname][['snap2_location', f'pol{polname.lower()}_digitizer_channel']].to_list()
    return int(snap2loc), int(start + dig0)


def antpol_to_fpga(antname, polname):
    """ Given antname and polname, return (snap2loc, fpga input) tuple.
    """

    snap2loc, fpgainp = lwa_df.loc[antname][['snap2_location', f'pol{polname.lower()}_fpga_num']].to_list()
    return int(snap2loc), int(fpgainp)


def ant_to_snap2loc(antname):
    """ Given antname, return snap2 (chassis, location) as tuple
    """

    return (lwa_df.loc[antname]['snap2_chassis'], lwa_df.loc[antname]['snap2_location'])


def snap2_to_antpol(snap2loc, inp):
    """ Given snap2loc and input number, return ant name.
    """

    if isinstance(snap2loc, str):
        snap2loc = int(snap2loc.lstrip('snap'))

    pol = 'b' if isodd(inp) else 'a'  # input alternates pols
#    start = 32*lwa_df['fmc']
#    remapped = start + lwa_df[f'pol{pol}_digitizer_channel']
#    remapped = lwa_df[f'pol{pol}_digitizer_channel']
    sel = np.where((inp == lwa_df[f'pol{pol}_fpga_num']) & (lwa_df['snap2_location'] == snap2loc))[0]
    if len(sel) != 1:
        print(f'Did not find exactly one antpol for input {inp}')
        return lwa_df.iloc[sel].index.to_list()
    else:
        return lwa_df.iloc[sel].index.to_list()[0] + pol.upper()


def antname_to_correlator(antname):
    """ Given antname, return correlator number
    """

    return int(lwa_df.loc[antname]['corr_num'])


def correlator_to_antname(corr_num):
    """ Given correlator number, return antname.
    """

    antlist = filter_df('corr_num', corr_num).index.to_list()
    if len(antlist) == 1:
        return antlist[0]
    else:
        print(f'Did not find exactly one ant')
        return list(antlist)
