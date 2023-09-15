import base64
import json
import threading

from flask import Flask, render_template
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

HTTP_SERVER_PORT = 8080
app = Flask(__name__)
sockets = Sockets(app)

@app.route("/test", methods=["GET"])
def test_server():
    return "<h1>Hello World</h1>"

@app.route("/twiml", methods=["GET", "POST"])
def return_twiml():
    print("POST TwiML")
    # TODO: make this bidirectional
    return render_template("streams.xml")

@sockets.route("/")
def transcript(ws):
    print("WS connection opened")
    while not ws.closed:
        message = ws.receive()
        if message is None:
            print("Empty message")
            break

        data = json.loads(message)
        if data["event"] in ("connected", "start"):
            print(f"Media WS: Received event '{data['event']}': {message}")
            continue
        if data["event"] == "media":
            print("Received media")
            media = data["media"]
            chunk = base64.b64decode(media["payload"])
        if data["event"] == "stop":
            print(f"Media WS: Received event 'stop': {message}")
            print("Stopping...")
            break

    print("WS connection closed")

if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(
        ("", HTTP_SERVER_PORT), app, handler_class=WebSocketHandler
    )
    print("Server listening on: http://localhost:" + str(HTTP_SERVER_PORT))
    server.serve_forever()

# can stream back same text each time to test