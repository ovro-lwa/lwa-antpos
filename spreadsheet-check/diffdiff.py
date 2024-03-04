import pandas as pd
import sigtab

def diff_spreadsheets(s1, s2):
    df1 = pd.read_csv(s1, encoding='windows-1252', skiprows=[1])
    df2 = pd.read_csv(s2, encoding='windows-1252', skiprows=[1])

    # drop unused columns
    unused_cols = ['influx tag', 'Unnamed: 34', 'Unnamed: 35', 'Unnamed: 36']
    df1 = df1.drop(columns=unused_cols).fillna(
            value={'Notes': '', 'Pol A Ant cable status': '',
                'Pol B Ant cable status': ''})
    df2 = df2.drop(columns=unused_cols).fillna(
            value={'Notes': '', 'Pol A Ant cable status': '',
                'Pol B Ant cable status': ''})

    assert (df1.columns == df2.columns).all()
   
    df1 = df1.sort_values(by='Antenna\nname')
    df2 = df2.sort_values(by='Antenna\nname')

    # Row by row diff
    for (rownum1, row1), (rownum2, row2) in zip(df1.iterrows(), df2.iterrows()):
        if not ((row2.isna() & row1.isna()) | (row1 == row2)).all():
            print('=========diff truth value ============')
            print(row1==row2)
            print(f'--------{s1}--------')
            print(row1)
            print(f'--------{s2}--------')
            print(row2)
            print('======================')

    # check that there are no Online rows with NaNs
    for _, row in df1[df1['Online']=='YES'].iterrows():
        if row.isna().any():
            print(row)

    print(df1.dtypes)
    return df1, df2
    

def diff_config_sigtab(config_locked: pd.DataFrame):
    online = config_locked[config_locked['Online']=='YES']
    n_rows = 0
    for _, row in online.iterrows():
        for pol in ('A', 'B'):
            n_rows += 1
            asig, dsig = sigtab.name2sig(row['Antenna\nname'] + pol)
            assert (asig is not None) and (dsig is not None)
            assert dsig==sigtab.a2d(asig)
            assert asig==sigtab.d2a(dsig)
            snap, sig = sigtab.d2feng(dsig)
            adr, chan = sigtab.a2arx(asig)
            assert adr==int(row['ARX board address'])
            assert chan==int(row[f'Pol {pol} ARX\nchannel #'])
            assert snap==int(row['SNAP2\nlocation #'])
            assert sig==int(row[f'Pol {pol} FPGA Input #'])
    print(f'iterated over {n_rows} antpols')

    print((online['Antenna\nname'] == 'LWA-266').any())
    for ant in sigtab.antNames:
        if not (online['Antenna\nname']==ant[:-1]).any():
            print(f'{ant} in sigtab but not marked as online in configuration spreadsheet.')

if __name__ == '__main__':
    config_locked, _ = diff_spreadsheets('config-locked.csv', 'config-20240228.csv')
    diff_config_sigtab(config_locked)

