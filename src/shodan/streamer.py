# coding: utf-8
from shodan import stream
from json import loads

bot = stream.Stream('qdH2Wz6Cpi14M2cVgnZ7AXOlf12FyCdT')

for record in bot.countries(['US']):
    for key in record:
        print(key, record[key])
    break
