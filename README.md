# lwa-antpos

# Requirements
* pandas
* numpy
* astropy
* dsa110-pyutils

# Installation

`python setup.py install`

# Usage

Station class with coordinates:

```
> from lwa_antpos import station
> st = station.ovrolwa
> print(st)
Station LWA-000 with 352 antennas
> print(st.casa_position)
('ITRF', '-2409261.733561m', '-4477916.567884m', '3839351.138694m')
> st2 = st.select_subset([0, 1, 2])
> print(st2.antennas)
[Antenna 1 in Station OVRO-LWA with 352 antennas,
 Antenna 2 in Station OVRO-LWA with 352 antennas,
 Antenna 3 in Station OVRO-LWA with 352 antennas]
> ant = st.antennas[0]
> print(ant.lat, ant.lon)
0.6499685035526378, -2.064391274631196
```

Mapping antenna name to ARX, SNAP2, etc:

```
> from lwa_antpos import mapping
Read antpos from xlsx file in repo
> mapping.ant_to_snap2loc('LWA-300')
(2, 11)
> mapping.antpol_to_arx('LWA-235', 'a')
```
