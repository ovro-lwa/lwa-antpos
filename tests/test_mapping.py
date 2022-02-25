import pytest

from lwa_antpos import mapping, lwa_df

def test_hasants():
    assert len(lwa_df)

def test_antarx():
    arx = mapping.antpol_to_arx('LWA-300', 'A')
    print(arx)
    assert len(arx)

def test_snapant():
    antpol = mapping.snap2_to_antpol(3, 0)
    print(antpol)
    assert len(antpol)

def test_antcorr():
    corrnum = mapping.antname_to_correlator('LWA-300')
    assert isinstance(corrnum, int)

def corrant():
    antpol = mapping.correlator_to_antpol(300)
    print(type(antpol))
    assert isinstance(antpol, str)

