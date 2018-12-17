import json
import websocket


def on_message(ws, message):
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


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    ws.send(
        '[1,"threatmap",{"roles":{"caller":{"features":{"caller_identification":true,"progressive_call_results":true}},"callee":{"features":{"caller_identification":true,"pattern_based_registration":true,"shared_registration":true,"progressive_call_results":true,"registration_revocation":true}},"publisher":{"features":{"publisher_identification":true,"subscriber_blackwhite_listing":true,"publisher_exclusion":true}},"subscriber":{"features":{"publisher_identification":true,"pattern_based_subscription":true,"subscription_revocation":true}}}}]')
    ws.send('[32,1201820522914946,{},"ips"]')


if __name__ == "__main__":
    # conn = psycopg2.connect(database="postgres", user="postgres", password="mysecretpassword", host="db")
    # cur = conn.cursor()
    # cur.execute("CREATE TABLE IF NOT EXISTS fortiguard(id serial PRIMARY KEY, attack json )")
    with open("data.csv", "w") as f:
        f.write("srclan,srclon,srccountrycode,dstlan,dstlon,dstcountrycode,type,severity\n")
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp("wss://threatmap.fortiguard.com/ws",
                                    on_open=on_open,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close,
                                    subprotocols=['wamp.2.json'])
        ws.run_forever()
