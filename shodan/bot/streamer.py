# coding: utf-8
from models.meta import Location, HostName, CPE, _Shodan, Option
from models.http import HTTP, SSL
from models.stream import Stream
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
    break
