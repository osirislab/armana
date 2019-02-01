from sqlalchemy import Table, Column, Integer, BigInteger, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base as base


Base = base()


class Stream(Base):
    __tablename__ = 'stream'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    product = Column(Text)
    hash = Column(BigInteger)
    ip = Column(BigInteger)
    org = Column(Text)
    data = Column(Text)
    port = Column(Integer)
    transport = Column(Text)
    isp = Column(Text)
    timestamp = Column(Text)
    ip_str = Column(Text)

class HostName(Base):
    __tablename__ = 'hostname'

    stream_id = Column(BigInteger, ForeignKey("stream.id"), primary_key=True)
    hostname = Column(Text)

class CPE(Base): # TODO: figure out what this actually does
    __tablename__ = 'cpe'

    stream_id = Column(BigInteger, ForeignKey("stream.id"), primary_key=True)
    cpe = Column(Text)

class Location(Base):
    __tablename__ = 'location'

    stream_id = Column(BigInteger, ForeignKey("stream.id"), primary_key=True)
    longitude = Column(Text)
    latitude = Column(Text)
    country_code = Column(Text)
    country_code_3 = Column(Text)
    country_name = Column(Text)
    city = Column(Text)
    postal_code = Column(Text)
    region_code = Column(Text)
    area_code = Column(Text)
    dma_code = Column(Text)


class _Shodan(Base):
    __tablename__ = '_shodan'

    stream_id = Column(BigInteger, ForeignKey("stream.id"), primary_key=True)

    # TODO: parse `options`

    crawler = Column(Text)
    module = Column(Text)
    id = Column(Text)


class Option(Base):
    __tablename__ = 'opts'

    # TODO: Parse `opts`
    stream_id = Column(BigInteger, ForeignKey("stream.id"), primary_key=True)


class HTTP(Base):
    __tablename__ = 'http'

    # TODO: Parse the HTTP objects properly
    stream_id = Column(BigInteger, ForeignKey("stream.id"), primary_key=True)
    http = Column(Text)

class SSL(Base):
    __tablename__ = 'ssl'

    # TODO: Parse the HTTP objects properly
    stream_id = Column(BigInteger, ForeignKey("stream.id"), primary_key=True)
    ssl = Column(Text)
