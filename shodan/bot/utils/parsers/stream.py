from helpers import clean, WrappedSession


class StreamRecorder(WrappedSession):
    def __init__(self, session):
        WrappedSession.__init__(self, session)

    def parse(self, record):
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

        self.session.add(s)
