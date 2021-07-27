from pandas import DataFrame

from . import lwa_df

def filter_df(columnname, value):
    """ Gets full DataFrame and filters by columnname == value.
    Returns new DataFrame
    """

    return lwa_df.loc[lambda lwa_df: lwa_df[columname] == value]


def get_unique(df, columnname):
    """ Return unique values for columnname in DataFrame
    """

    return np.unique(df[columnname].values)

