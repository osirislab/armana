from helpers import clean, WrappedSession
from models import Location, HostName


class LocationRecorder(WrappedSession):
    def __init__(self, session, stream_id):
        WrappedSession.__init__(self, session, stream_id)

    def parse(self, record):
        location = clean(record.get('location'))

        if self.stream_id and type(location) is dict:
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
                stream_id=self.stream_id, longitude=longitude, latitude=latitude,
                country_code=country_code, country_code_3=country_code_3,
                country_name=country_name, city=city, postal_code=postal_code,
                region_code=region_code, area_code=area_code, dma_code=dma_code
            )

            self.session.add(s)


class HostNameRecorder(WrappedSession):
    def __init__(self, session, stream_id):
        WrappedSession.__init__(self, session, stream_id)

    def parse(self, record):
        hostname = clean(record.get('hostname'))

        if self.stream_id and type(hostname) is str:
            h = HostName(self.stream_id, hostname)
            self.session.add(h)
