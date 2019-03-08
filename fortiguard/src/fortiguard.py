import json
import websocket
import threading
import time
import pycountry


class SocketThread(threading.Thread):
    ''' Threaded Websocket for running in the background '''

    def __init__(self, session):
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp(
            "wss://threatmap.fortiguard.com/ws",
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            subprotocols=['wamp.2.json']
        )

    def on_message(self, message):
        j = json.loads(message)
        if j[0] == 36:
            msg = j[4][0]
            # cur.execute("INSERT INTO fortiguard (data) VALUES (%(data)s)", {"data": Json(data)})
            data = [
                str(msg['src']['latitude']),
                str(msg['src']['longitude']),
                msg['src']['countrycode'],
                str(msg['dst']['latitude']),
                str(msg['dst']['longitude']),
                msg['dst']['countrycode'],
                msg['type'],
                msg['severity']
            ]
            f.write(",".join(data) + "\n")

    def on_error(self, error):
        print(error)

    def on_close(self):
        print("### closed ###")

    def on_open(self):
        self.ws.send('[1,"threatmap",{"roles":{"caller":{"features":{"caller_identification":true,"progressive_call_results":true}},"callee":{"features":{"caller_identification":true,"pattern_based_registration":true,"shared_registration":true,"progressive_call_results":true,"registration_revocation":true}},"publisher":{"features":{"publisher_identification":true,"subscriber_blackwhite_listing":true,"publisher_exclusion":true}},"subscriber":{"features":{"publisher_identification":true,"pattern_based_subscription":true,"subscription_revocation":true}}}}]')
        self.ws.send('[32,1201820522914946,{},"ips"]')

    def run(self):
        print('WebSocketApp started')
        self.ws.run_forever()


if __name__ == "__main__":
    # conn = psycopg2.connect(database="postgres", user="postgres", password="mysecretpassword", host="db")
    # cur = conn.cursor()
    # cur.execute("CREATE TABLE IF NOT EXISTS fortiguard(id serial PRIMARY KEY, attack json )")
    with open("data.csv", "w") as f:
        f.write(
            "srclan,srclon,srccountrycode,dstlan,dstlon,dstcountrycode,type,severity\n")
