import pandas as pd
from pkg_resources import resource_filename

antposfile = resource_filename("lwa_antpos", "data/LWA-352 Antenna Status & System Configuration.xlsx")
# "data/LWA-352 Antenna Positions & System Status.xlsx"  # old name


def read_antpos_xlsx(filename=antposfile):
    df = pd.read_excel(filename, engine='openpyxl', header=1)
    df.drop(index=0, inplace=True)  # descriptive header should be dropped
    df.drop(columns='etcd key part', inplace=True)  # descriptive column should be dropped
    assert "antname" in df.columns
    df = df.set_index('antname')

    return df
