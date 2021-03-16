import pytest

from lwa_antpos import station

def test_ovrolwa():
    ovrolwa = station.ovrolwa
    assert len(ovrolwa.antennas) == 352

def test_station():
    st = station.Station('station', 0, 0, 0)
    ant = station.Antenna('antenna', 0, 0, 0)
    st.append(ant)
    assert len(st.antennas) == 1
    assert ant.parent == st
