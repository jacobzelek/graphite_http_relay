from flask import Flask, request
import json
import socket
import urllib2

app = Flask(__name__)

API_KEYS = {}

CARBON_SOCKET = None


def connect_to_carbon():
    CARBON_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CARBON_SOCKET.connect(("127.0.0.1", 2003))


def close_carbon():
    CARBON_SOCKET.close()


@app.route('/metrics', methods=["POST"])
def post_metric():
    if request.args.get("api_key", None) in API_KEYS:
        try:
            CARBON_SOCKET.send(request.body)
        except:
            connect_to_carbon()
            CARBON_SOCKET.send(request.body)
        
        return "OK", 200

    return "Unauthorized", 401


@app.route('/events', methods=["POST"])
def post_event():
    if request.args.get("api_key", None) in API_KEYS:
        req = urllib2.Request('http://127.0.0.1:8080/events',
            data=request.body, headers={'Content-type': 'text/plain'})
        
        r = urllib2.urlopen(req)
        
        return "OK", 200

    return "Unauthorized", 401

if __name__ == "__main__":
    API_KEYS = json.load(open("config.json", "r"))["api_keys"]

    connect_to_carbon()

    app.run(debug=False, use_reloader=False, host="127.0.0.1", port=8081, threaded=True)

    close_carbon()