from pandas import DataFrame
import numpy as np

from . import lwa_df

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

    return lwa_df.loc[antname][f'pol{polname}_arx_channel']


def antpol_to_digitizer(antname, polname):
    """ Given antname and polname, return digitizer channel
    """

    return lwa_df.loc[antname][f'pol{polname}_digitizer_channel']


def ant_to_snap2(antname):
    """ Given antname, return snap2 (chassis, location) as tuple
    """

    return (lwa_df.loc[antname]['snap2_chassis'], lwa_df.loc[antname]['snap2_location'])
