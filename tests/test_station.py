import pytest

from lwa_antpos import station

def test_ovrolwa():
    ovro = station.ovro
    assert len(station.ovro.antennas)

def test_station():
    st = station.Station('station', 0, 0, 0)
    ant = station.Antenna('LWA-1', 0, 0, 0)
    st.append(ant)
    assert len(st.antennas) == 1
    assert ant.parent == st
