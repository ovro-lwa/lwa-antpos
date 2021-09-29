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
    """ Given antname and polname, return arx channel
    """

    return lwa_df.loc[antname][f'pol{polname.lower()}_arx_channel']


def antpol_to_digitizer(antname, polname):
    """ Given antname and polname, return digitizer channel
    """

#    start = 32*lwa_df.loc[antname]['fmc']
#    return start + lwa_df.loc[antname][f'pol{polname.lower()}_digitizer_channel']
    return lwa_df.loc[antname][f'pol{polname.lower()}_digitizer_channel']


def ant_to_snap2loc(antname):
    """ Given antname, return snap2 (chassis, location) as tuple
    """

    return (lwa_df.loc[antname]['snap2_chassis'], lwa_df.loc[antname]['snap2_location'])


def digitizer_to_antpol(digitizer):
    """ Given digitizer channel and pol, return a list of ant names.
    """

    pol = 'b' if isodd(digitizer) else 'a'  # digitizer alternates pols
#    start = 32*lwa_df['fmc']
#    remapped = start + lwa_df[f'pol{pol}_digitizer_channel']
    remapped = lwa_df[f'pol{pol}_digitizer_channel']

    sel = np.where(remapped == digitizer)
    if len(sel) != 1:
        print(f'Did not find exactly one antpol for digitizer {digitizer}')
        return lwa_df.iloc[sel].index.to_list()
    else:
        return lwa_df.iloc[sel].index.to_list()[0] + pol.upper()


def antpol_to_correlator(antname, polname):
    """ Given antname and polname, return correlator number
    """

    chassis, location = ant_to_snap2loc(antname)
    digitizer = antpol_to_digitizer(antname, polname)
    return 64*(location-1) + digitizer


def correlator_to_antpol(correlator_number):
    """ Get ant/pol for a given correlator_number.
    """

    digitizer = correlator_number % 64
    location = correlator_number // 64 + 1

    return lwa_df[(lwa_df.snap2_location == location) & (lwa_df.pola_digitizer_channel == digitizer) | (lwa_df.polb_digitizer_channel == digitizer)]
