from flask import Flask
from app.models import db, Threat, Threat_Source_Stat, Threat_Destination_Stat
from app.views import views
from app.db_bot import SocketThread
from sqlalchemy_utils import database_exists, create_database
from os import getenv
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(verbose=True, dotenv_path=Path('.')  / '.env')

dbu = getenv('DB_USER')
dbp = getenv('DB_PASS')
dbh = getenv('DB_HOST')
dbn = getenv('DB_NAME')

if dbu and dbh and dbn:
    db_url = 'postgresql://{u}:{p}@{h}/{n}'.format(u=dbu, p=dbp, h=dbh, n=dbn)
else:
    print('ERROR: Need valid .env file')
    exit(1)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

if not database_exists(db_url):
    create_database(db_url)

with app.app_context():
    db.create_all()

app.register_blueprint(views)
app.db = db

ws = SocketThread(app, debug=True)
