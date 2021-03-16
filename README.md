# lwa-antpos

# Requirements
* pandas
* numpy
* astropy
* dsa110-pyutils

# Installation

`python setup.py install`

# Usage
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