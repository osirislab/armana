from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
from pathlib import Path
from os import getenv

from models import *

load_dotenv(verbose=True, dotenv_path=Path('.')  / '.env')

dbuser = getenv('DB_USER')
dbpass = getenv('DB_PASS')
dbhost = getenv('DB_HOST')
dbname = getenv('DB_NAME')
dbport = getenv('DB_PORT')

if not dbport:
    dbport = 3306

link = 'mysql+mysqlconnector://{dbuser}:{dbpass}@{dbhost}:{dbport}/{dbname}'.format(
        dbuser=dbuser, dbpass=dbpass, dbhost=dbhost, dbname=dbname, dbport=dbport)

print('Checking the database.')
if not database_exists(link):
    print('Creating the database.')
    create_database(link)

print('Creating the engine.')
engine = create_engine(link, echo=True, pool_recycle=600)

print('Creating tables.')
Base.metadata.create_table(engine) # Base is from models

print('Creating a session.')
Session = sessionmaker(bind=engine)
