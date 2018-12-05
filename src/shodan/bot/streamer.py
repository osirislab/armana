# coding: utf-8
from models import Stream, Location
from shodan import stream
from db import Session
from re import sub
import logging


logging.basicConfig(filename='shodan_streamer.log',level=logging.ERROR)

bot = stream.Stream('qdH2Wz6Cpi14M2cVgnZ7AXOlf12FyCdT')

session = Session()


# TODO: handle exceptions better
for record in bot.countries(['US']):
    # a stream metadata
    id = record.get('id')
    product = record.get('product')
    hash = record.get('hash')
    ip = record.get('ip')
    org = record.get('org')
    data = record.get('data')
    port = record.get('port')
    transport = record.get('transport')
    isp = record.get('isp')
    timestamp = record.get('timestamp')
    ip_str = record.get('ip_str')

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
    location = record.get('location')
    if type(location) is dict:
        stream_id = s.id
        longitude = location.get('longitude')
        latitude = location.get('latitude')
        country_code = location.get('country_code')
        country_code_3 = location.get('country_code3')
        country_name = location.get('country_name')
        city = location.get('city')
        postal_code = location.get('postal_code')
        region_code = location.get('region_code')
        area_code = location.get('area_code')
        dma_code = location.get('dma_code')

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
