from sqlalchemy import Table, Column, BigInteger, BigInteger, Text, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base as base
from time import time


Base = base()


class ThreatSourceStat(Base):
    __tablename__ = 'threat_source_stat'

    str_len = 32
    threat_id = Column(BigInteger, primary_key=True, autoincrement=True)
    country = Column(String(str_len), primary_key=True)
    state = Column(String(str_len))
    city = Column(String(str_len))
    longitude = Column(String(str_len))
    latitude = Column(String(str_len))
    count = Column(BigInteger)

    def __init__(self, country, state, city, longitude, latitude, count):
        self.country = country
        self.state = state
        self.city = city
        self.longitude = longitude
        self.latitude = latitude
        self.count = count

    def __repr__(self):
        return 'Source Threat Count - {}: {}'.format(self.country, self.count)

class ThreatDestinationStat(Base):
    __tablename__ = 'threat_destination_stat'

    str_len = 32
    threat_id = Column(BigInteger, primary_key=True, autoincrement=True)
    country = Column(String(str_len), primary_key=True)
    state = Column(String(str_len))
    city = Column(String(str_len))
    longitude = Column(String(str_len))
    latitude = Column(String(str_len))
    count = Column(BigInteger)

    def __init__(self, country, state, city, longitude, latitude, count):
        self.country = country
        self.state = state
        self.city = city
        self.longitude = longitude
        self.latitude = latitude
        self.count = count

    def __repr__(self):
        return 'Destination Threat Count - {}: {}'.format(self.country, self.count)

class Threat(Base):
    __tablename__ = 'threat'

    str_len = 32
    threat_id = Column(BigInteger, primary_key=True)
    src_city = Column(String(str_len))
    dst_city = Column(String(str_len))
    src_state = Column(String(str_len))
    dst_state = Column(String(str_len))
    src_country = Column(String(str_len))
    dst_country = Column(String(str_len))
    src_longitude = Column(String(str_len))
    dst_longitude = Column(String(str_len))
    src_latitude = Column(String(str_len))
    dst_latitude = Column(String(str_len))
    atk_time = Column(String(str_len))
    atk_type = Column(Text)
    atk_name = Column(Text)

    def __init__(self, scity, scountry, 
            dcity, dcountry, sstate, dstate, 
            slong, dlong, slat, dlat, 
            timestamp, atk_name, atk_type):

        self.src_city = scity
        self.dst_city = dcity
        self.src_country = scountry
        self.dst_country = dcountry
        self.src_state = sstate
        self.dst_state = dstate
        self.src_longitude = slong
        self.dst_longitude = dlong
        self.src_latitude = slat
        self.dst_latitude = dlat
        self.atk_time = timestamp
        self.atk_type = atk_type
        self.atk_name = atk_name

    def __repr__(self):
        l = self.str_len
        s = self.scountry
        d = self.dcountry
        n = self.atk_time
        return '{}{} ︻╦╤─ {}'.format(n.ljust(l), s.ljust(l), d.rjust(l))
