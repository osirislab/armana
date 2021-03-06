import websocket
import threading
import datetime
import time
import json
import pycountry

from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
from pathlib import Path
from os import getenv

from models import *

load_dotenv(verbose=True, dotenv_path=Path('.') / '.env')

dbu = getenv('DB_USER')
dbp = getenv('DB_PASS')
dbh = getenv('DB_HOST')
dbn = getenv('DB_NAME')


link = 'postgresql+psycopg2://{u}:{p}@{h}/{n}'.format(
    u=dbu, p=dbp, h=dbh, n=dbn)


print('Checking the database.')
if not database_exists(link):
    print('Creating the database.')
    create_database(link)

print('Creating the engine.')
engine = create_engine(link, echo=True, pool_recycle=600)

print('Creating tables.')
Base.metadata.create_all(engine)  # Base is from models

print('Creating a session.')
Session = sessionmaker(bind=engine)


class SocketThread(threading.Thread):
    ''' Threaded Websocket for running in background '''

    scity = 'sourcecity'
    dcity = 'destinationcity'
    scountry = 'sourcecountry'
    dcountry = 'destinationcountry'
    timestamp = 'timestamp'
    attackname = 'attackname'
    attacktype = 'type'
    sstate = 'sourcestate'
    dstate = 'destinationstate'
    slong = 'sourcelongitude'
    dlong = 'destinationlongitude'
    slat = 'sourcelatitude'
    dlat = 'destinationlatitude'
    unknown = 'UNKNOWN'

    def __init__(self, session, debug=False):
        '''Going to need that DB'''
        threading.Thread.__init__(self)

        target_url = (
            'wss://threatmap.checkpoint.com/ThreatPortal/websocket?'
            'X-Atmosphere-tracking-id=0&X-Atmosphere-Framework=2.3.5-javascript&'
            'X-Atmosphere-Transport=websocket&X-Atmosphere-TrackMessageSize=true&'
            'Content-Type=application/json&X-atmo-protocol=true'
        )

        self.session = session
        self.checked = False
        self.debug = debug
        self.ws = websocket.WebSocketApp(
            target_url,
            on_message=self.handle_message,
            on_error=self.handle_error,
            on_close=self.handle_close
        )

    def handle_message(self, rawstr):
        if not self.checked:
            self.checked = True
            return

        message = json.loads(rawstr.strip().split('|')[1])
        scity = message.get(self.scity)
        dcity = message.get(self.dcity)
        scountry = message.get(self.scountry)
        dcountry = message.get(self.dcountry)
        timestamp = message.get(self.timestamp)
        attackname = message.get(self.attackname)
        attacktype = message.get(self.attacktype)
        sstate = message.get(self.sstate)
        dstate = message.get(self.dstate)
        slong = message.get(self.slong)
        dlong = message.get(self.dlong)
        slat = message.get(self.slat)
        dlat = message.get(self.dlat)

        if not scity:
            scity = self.unknown
        if not dcity:
            dcity = self.unknown
        if not scountry:
            scountry = self.unknown
        if not dcountry:
            dcountry = self.unknown
        if not timestamp:
            timestamp = self.unknown
        if not attacktype:
            attacktype = self.unknown
        if not attackname:
            attackname = self.unknown
        if not sstate:
            sstate = self.unknown
        if not dstate:
            dstate = self.unknown
        if not slong:
            slong = self.unknown
        if not dlong:
            dlong = self.unknown
        if not slat:
            slat = self.unknown
        if not dlat:
            dlat = self.unknown

        if scountry == self.unknown and dcountry == self.unknown:
            return

        scountry = pycountry.countries.get(alpha_2=scountry).name
        dcountry = pycountry.countries.get(alpha_2=dcountry).name

        if 'USA' in dcountry:
            self.session.add(
                Threat(
                    scity, scountry,
                    dcity, dcountry,
                    sstate, dstate,
                    slong, dlong,
                    slat, dlat,
                    int(timestamp / 1000),
                    attackname, attacktype
                )
            )
            try:
                self.session.commit()
            except:
                self.session.rollback()
                raise

            if self.debug:
                l = 32
                n = datetime.datetime.fromtimestamp(
                    timestamp / 1000
                ).strftime('%Y-%m-%d %H:%M:%S')
                print('{}{} ︻╦╤─ {}\n'.format(
                    n.ljust(l), scountry.ljust(l), dcountry.rjust(l)
                ))

    def handle_error(self, error):
        print(error)

    def handle_close(self):
        print('WebSocketApp terminated')

    def run(self):
        print('WebSocketApp started')
        self.ws.run_forever()
