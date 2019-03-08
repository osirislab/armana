from dotenv import load_dotenv
from pathlib import Path
from redis import Redis
from os import getenv

load_dotenv(verbose=True, dotenv_path=Path('.') / '.env')


class Config:
    # database variables
    dbuser = getenv('DB_USER')
    dbpass = getenv('DB_PASS')
    dbhost = getenv('DB_HOST')
    dbname = getenv('DB_NAME')
    dbport = 3306

    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://'

    if getenv('DB_PORT'):
        port = int(getenv('DB_PORT'))

    SQLALCHEMY_DATABASE_URI += '{u}:{p}@{h}:{pt}/{n}'.format(
        u=dbuser, p=dbpass, h=dbhost, pt=dbport, n=dbname
    )

    if getenv('DEVELOPMENT_MODE'):
        SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    elif not (dbuser and dbhost and dbname):
        print('.env configuration incomplete')
        exit(1)

    # session
    # https://pythonhosted.org/Flask-Session/
    # 'filesystem' is an alternative if you don't want to use Redis
    SESSION_TYPE = 'redis'
    SESSION_REDIS = Redis(host='oingo_cache', port=6379)

    # template autoreload
    TEMPLATES_AUTO_RELOAD = True

    # track DB mod
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Google Maps API Key
    GOOGLEMAPS_KEY = getenv('GOOGLEMAPS_KEY')
    if not GOOGLEMAPS_KEY:
        print('Environment variable `GOOGLEMAPS_KEY` incomplete')
        exit(1)
