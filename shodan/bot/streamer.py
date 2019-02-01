# coding: utf-8
from models import Stream, Location
from shodan import stream
from db import Session
from re import sub
import logging


logging.basicConfig(filename='shodan_streamer.log', level=logging.ERROR)
logging.getLogger('sqlalchemy').setLevel(logging.ERROR)

bot = stream.Stream('qdH2Wz6Cpi14M2cVgnZ7AXOlf12FyCdT')

session = Session()


def clean(s):
    return s.replace('\0', '') if type(s) is str else s


for record in bot.countries(['US']):
    # a stream metadata
    id = clean(record.get('id'))
    product = clean(record.get('product'))
    hash = clean(record.get('hash'))
    ip = clean(record.get('ip'))
    org = clean(record.get('org'))
    data = clean(record.get('data'))
    port = clean(record.get('port'))
    transport = clean(record.get('transport'))
    isp = clean(record.get('isp'))
    timestamp = clean(record.get('timestamp'))
    ip_str = clean(record.get('ip_str'))

    s = Stream(
        product=product, hash=hash, ip=ip, org=org, data=data, port=port, 
        transport=transport, isp=isp, timestamp=timestamp, ip_str=ip_str
    )

    session.add(s)

    try:
        session.commit()
    except Exception as e:
        logging.exception(e)
        continue

    # location
    location = clean(record.get('location'))
    if type(location) is dict:
        stream_id = s.id
        longitude = clean(location.get('longitude'))
        latitude = clean(location.get('latitude'))
        country_code = clean(location.get('country_code'))
        country_code_3 = clean(location.get('country_code3'))
        country_name = clean(location.get('country_name'))
        city = clean(location.get('city'))
        postal_code = clean(location.get('postal_code'))
        region_code = clean(location.get('region_code'))
        area_code = clean(location.get('area_code'))
        dma_code = clean(location.get('dma_code'))

        l = Location(
            stream_id=stream_id, longitude=longitude, latitude=latitude,
            country_code=country_code, country_code_3=country_code_3,
            country_name=country_name, city=city, postal_code=postal_code,
            region_code=region_code, area_code=area_code, dma_code=dma_code
        )

        session.add(l)

        try:
            session.commit()
        except:
            logging.exception(e)
            continue
