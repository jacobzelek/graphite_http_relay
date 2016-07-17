from flask import Flask, request
import json
import socket
import urllib2
from functools import wraps

app = Flask(__name__)

API_KEYS = {}


def requires_auth_key(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if request.args.get("api_key", None) not in API_KEYS:
            return "Unauthorized", 401
        return func(*args, **kwargs)
    return wrapped


@app.route('/carbon/metrics', methods=["POST"])
@requires_auth_key
def post_metric():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 2003))
    s.send(request.data)
    s.close()
    
    return "OK", 200


@app.route('/carbon/events', methods=["POST"])
@requires_auth_key
def post_event():
    req = urllib2.Request('http://127.0.0.1:8080/events', data=request.data, headers={'Content-type': 'text/plain'})
    urllib2.urlopen(req)
    
    return "OK", 200

if __name__ == "__main__":
    API_KEYS = json.load(open("config.json", "r"))["api_keys"]

    app.run(debug=False, use_reloader=False, host="127.0.0.1", port=8081, threaded=True)