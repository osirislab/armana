from sqlalchemy import Table, Column, Integer, String, BigInteger, Text, Foreignkey
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Stream(Base):
    __tablename__ = 'stream'

    id = Column(BigInteger, primary_key=True)
    product = Column(String)
    hash = Column(BigInteger, nullable=False)
    ip = Column(BigInteger, nullable=False)
    org = Column(String)
    data = Column(Text)
    port = Column(Integer)
    transport = Column(String)
    isp = Column(String)
    timestamp = Column(String)
    ip_str = Column(String)

class HostName(Base):
    __tablename__ = 'hostname'

    stream_id = Column(BigInteger, primary_key=True, ForeignKey("stream.id"))
    hostname = Column(String, primary_key=True)

class CPE(Base): # TODO: figure out what this actually does
    __tablename__ = 'cpe'

    stream_id = Column(Integer, primary_key=True, ForeignKey("stream.id"))
    cpe = Column(String, primary_key=True)

class Location(Base):
    __tablename__ = 'location'

    stream_id = Column(BigInteger, primary_key=True, ForeignKey("stream.id"))
    longitude = Column(String)
    latitude = Column(String)
    country_code = Column(String)
    country_code_3 = Column(String)
    country_name = Column(String)
    city = Column(String)
    postal_code = Column(String)
    region_code = Column(String)
    area_code = Column(String)
    dma_code = Column(String)


class _Shodan(Base):
    __tablename__ = '_shodan'

    stream_id = Column(BigInteger, primary_key=True, ForeignKey("stream.id"))

    # TODO: parse `options`

    crawler = Column(String, nullable=False)
    module = Column(String, nullable=False)
    id = Column(String, nulltable=False)


class Option(Base):
    __tablename___ = 'opts'

    # TODO: Parse `opts`
    stream_id = Column(BigInteger, primary_key=True, ForeignKey("stream.id"))


class HTTP(Base):
    __tablename__ = 'http'

    # TODO: Parse the HTTP objects properly
    stream_id = Column(BigInteger, primary_key=True, ForeignKey("stream.id"))
    http = Column(Text)
