from flask_sqlalchemy import SQLAlchemy
from time import time

db = SQLAlchemy()

class Visitor(db.Model):
    visitor_id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(15))
    port = db.Column(db.INTEGER)
    timestamp = db.Column(db.BIGINT)
    method = db.Column(db.String(7))
    path = db.Column(db.Text)
    params = db.Column(db.Text)
    user_agent = db.Column(db.Text)
    host = db.Column(db.Text)
    origin = db.Column(db.Text)
    referer = db.Column(db.Text)
    content_type = db.Column(db.Text)

    def __init__(self, ip, port, method, path, 
            params, user_agent, host, origin, 
            referer, content_type):

        self.ip = ip
        self.port = port
        self.method = method
        self.path = path
        self.params = params
        self.user_agent = user_agent
        self.host = host
        self.origin = origin
        self.referer = referer
        self.content_type = content_type

    def __repr__(self):
        return 'Visitor {}:{} - {} {}'.format(self.ip, self.port, self.method, self.path)

class Threat_Source_Stat(db.Model):
    str_len = 32
    threat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country = db.Column(db.String(str_len), primary_key=True)
    state = db.Column(db.String(str_len))
    city = db.Column(db.String(str_len))
    longitude = db.Column(db.String(str_len))
    latitude = db.Column(db.String(str_len))
    count = db.Column(db.BIGINT)

    def __init__(self, country, state, city, longitude, latitude, count):
        self.country = country
        self.state = state
        self.city = city
        self.longitude = longitude
        self.latitude = latitude
        self.count = count

    def __repr__(self):
        return 'Source Threat Count - {}: {}'.format(self.country, self.count)

class Threat_Destination_Stat(db.Model):
    str_len = 32
    threat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country = db.Column(db.String(str_len), primary_key=True)
    state = db.Column(db.String(str_len))
    city = db.Column(db.String(str_len))
    longitude = db.Column(db.String(str_len))
    latitude = db.Column(db.String(str_len))
    count = db.Column(db.BIGINT)

    def __init__(self, country, state, city, longitude, latitude, count):
        self.country = country
        self.state = state
        self.city = city
        self.longitude = longitude
        self.latitude = latitude
        self.count = count

    def __repr__(self):
        return 'Destination Threat Count - {}: {}'.format(self.country, self.count)

class Threat(db.Model):
    str_len = 32
    threat_id = db.Column(db.Integer, primary_key=True)
    src_city = db.Column(db.String(str_len))
    dst_city = db.Column(db.String(str_len))
    src_state = db.Column(db.String(str_len))
    dst_state = db.Column(db.String(str_len))
    src_country = db.Column(db.String(str_len))
    dst_country = db.Column(db.String(str_len))
    src_longitude = db.Column(db.String(str_len))
    dst_longitude = db.Column(db.String(str_len))
    src_latitude = db.Column(db.String(str_len))
    dst_latitude = db.Column(db.String(str_len))
    atk_time = db.Column(db.String(str_len))
    atk_type = db.Column(db.Text)
    atk_name = db.Column(db.Text)

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
