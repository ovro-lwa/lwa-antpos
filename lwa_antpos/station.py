import os
import sys
import copy
import numpy
import weakref

from pandas import DataFrame
from astropy.coordinates import EarthLocation
import astropy.units as u

from . import lwa_cnf, lwa_df, antnames

__all__ = ['Station', 'Antenna', 'parse_config', 'ovro']

center = lwa_df.loc['LWA-000']
ovro_lat = float(center.latitude) * numpy.pi/180
ovro_lon = float(center.longitude) * numpy.pi/180
ovro_elev = 1222.0        # TODO: get from cnf


def _smart_int(s, positive_only=False):
    i = 0
    v = None
    while i < len(s):
        try:
            if positive_only and s[i] == '-':
                raise ValueError
            v = int(s[i:], 10)
            break
        except ValueError:
            pass
        i += 1
    if v is None:
        raise ValueError("Cannot convert '%s' to int" % s)
    return v
    

class Station(object):
    """
    Class to represent the OVRO-LWA station and its antennas.
    """
    
    def __init__(self, name, lat=ovro_lat, lon=ovro_lon, elev=ovro_elev, antennas=None):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.elev = elev
        
        self.antennas = []
        if antennas is not None:
            self.antennas = antennas

    def __repr__(self):
        return f'Station {self.name} with {len(self.antennas)} antennas'

    @classmethod
    def from_df(cls, df):
        # TODO: Use OVRO_MMA as the telescope name until CASA knows about OVRO-LWA
        st = cls('OVRO_MMA', ovro_lat, ovro_lon, ovro_elev)

        for antname in antnames:
            row = df.loc[antname]
            ant = Antenna.from_df(row)
            st.append(ant)

        return st
        
    @classmethod
    def from_line(cls, line):
        """
        Create a new Station instance from a line in an antenna positions file.
        """
        
        name, lat, lon, x, y, active = line.split(None, 5)
        lat = float(lat) * numpy.pi/180
        lon = float(lon) * numpy.pi/180
        elev = 1222.0        # TODO: get from cnf
        return cls(name, lat, lon, elev)
        
    def append(self, ant):
        """
        Add an antenna to the array.
        """
        
        if not isinstance(ant, Antenna):
            raise TypeError("Expected an antenna")
        ant.parent = weakref.proxy(self)
        self.antennas.append(ant)
        
    def select_subset(self, ids):
        """
        Given a list of antenna IDs (either as integer index or name), return a
        new Station instance that only contains those antennas.
        """
        
        subset = Station(self.name+"-fast", self.lat*1.0, self.lon*1.0, self.elev*1.0)
        
        all_ids = [ant.id for ant in self.antennas]
        for id in ids:
            if isinstance(id, int):
                subset.append(copy.deepcopy(self.antennas[id]))
            else:
                subset.append(copy.deepcopy(self.antennas[all_ids.index(id)]))
        return subset
        
    @property
    def ecef(self):
        """
        Return the Earth centered, Earth fixed location of the array in meters.
        """
        
        e =  EarthLocation(lat=self.lat*u.rad, lon=self.lon*u.rad, height=self.elev*u.m)
        return (e.x.to_value(u.m), e.y.to_value(u.m), e.z.to_value(u.m))
        
    @property
    def topo_rot_matrix(self):
        """
        Return the rotation matrix that takes a difference in an Earth centered,
        Earth fixed location relative to the Station and rotates it into a
        topocentric frame that is south-east-zenith.
        """
        
        r = numpy.array([[ numpy.sin(self.lat)*numpy.cos(self.lon), numpy.sin(self.lat)*numpy.sin(self.lon), -numpy.cos(self.lat)],
                         [-numpy.sin(self.lon),                     numpy.cos(self.lon),                      0                  ],
                         [ numpy.cos(self.lat)*numpy.cos(self.lon), numpy.cos(self.lat)*numpy.sin(self.lon),  numpy.sin(self.lat)]])
        return r
        
    @property
    def casa_position(self):
        """
        Return a four-element tuple of (CASA position reference, CASA position 1,
        CASA position 2, CASA position 3, CASA position 4) that is suitable for
        use with casacore.measures.measures.position.
        """
        
        x, y, z = self.ecef
        return 'ITRF', '%fm' % x, '%fm' % y, '%fm' % z


class Antenna(object):
    """
    Class to represent an antenna in the OVRO-LWA.
    """
    
    def __init__(self, id, lat, lon, elev):
        if isinstance(id, str):
            id = _smart_int(id, positive_only=True)
        self.id = id
        self.lat = lat
        self.lon = lon
        self.elev = elev
        self.parent = None

    def __repr__(self):
        return f'Antenna {self.id} in {self.parent}'

    @classmethod
    def from_df(cls, row):
        """
        Create a new Antenna instance from df row (Series).
        """
        lat = float(row.latitude) * numpy.pi/180
        lon = float(row.longitude) * numpy.pi/180
        elev = float(row.elevation)
        if elev > 999990:
            elev = 1222.0
        return cls(row.name, lat, lon, elev)
        
    @classmethod
    def from_line(cls, line):
        """
        Create a new Antenna instance from a line in an antenna positions file.
        """
        
        name, lat, lon, x, y, active = line.split(None, 5)
        lat = float(lat) * numpy.pi/180
        lon = float(lon) * numpy.pi/180
        elev = 1222.0   # TODO: This will need to come from somewhere
        return cls(name, lat, lon, elev)
        
    @property
    def ecef(self):
        """
        Return the Earth centered, Earth fixed location of the antenna in meters.
        """
        
        e = EarthLocation(lat=self.lat*u.rad, lon=self.lon*u.rad, height=self.elev*u.m)
        return (e.x.to_value(u.m), e.y.to_value(u.m), e.z.to_value(u.m))
        
    @property
    def enz(self):
        """
        Return the topocentric east-north-zenith coordinates for the antenna 
        relative to the center of its associated Station in meters.
        """
        
        if self.parent is None:
            raise RuntimeError("Cannot find east-north-zenith without an associated Station")
            
        ecefFrom = numpy.array(self.parent.ecef)
        ecefTo = numpy.array(self.ecef)

        rho = ecefTo - ecefFrom
        rot = self.parent.topo_rot_matrix
        sez = numpy.dot(rot, rho)

        # Convert from south, east, zenith to east, north, zenith
        enz = 1.0*sez[[1,0,2]]
        enz[1] *= -1.0
        return enz
        
    
def parse_config(etcdserver=None, filename=None):
    """
    Parse OVRO-LWA configuration and return a Station instance.
    Without arguments, it will use lwa_cnf.
    Can optionally get data from etcd server or static file.
    """

    # TODO: Use OVRO_MMA as the telescope name until CASA knows about OVRO-LWA
    st = Station('OVRO_MMA', ovro_lat, ovro_lon, ovro_elev)

    if etcdserver is not None:
        pass
    elif filename is not None:
        with open(filename, 'r') as fh:
            for line in fh:
                if len(line) < 3:
                    continue
                elif line[0] == '#':
                    continue
                
                if line.find('NO') == -1:
                    ant = Antenna.from_line(line)
                    st.append(ant)
    else:
        connected = lwa_df[lwa_df.pola_fpga_num != -1]
        st = Station.from_df(connected)
        
    return st


# A ready-made Station instance, filled with Antennas
ovro = parse_config() # or use arg OVRO_CONFIG_FILENAME for text file
