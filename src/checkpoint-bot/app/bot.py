from db import *
import logging

logging.basicConfig(filename='bot.log', level=logging.ERROR)
logging.getLogger('sqlalchemy').setLevel(logging.ERROR)

session = Session()
ws = SocketThread(session, debug=True)

if __name__ == '__main__':
    while True:
        try:
            ws.run()
        except Exception as e:
            logging.exception(e)
