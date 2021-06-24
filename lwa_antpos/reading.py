import pandas as pd
from pkg_resources import resource_filename

antposfile = resource_filename("lwa_antpos", "data/LWA-352 Antenna Status & System Configuration.xlsx")
# "data/LWA-352 Antenna Positions & System Status.xlsx"  # old name


def read_antpos_xlsx(filename=antposfile):
    df = pd.read_excel(filename, engine='openpyxl', header=1)
    assert "Name" in df.columns
    return df
