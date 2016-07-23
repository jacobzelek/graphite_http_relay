from flask import Flask, request
import json
import socket
import urllib2
from functools import wraps

app = Flask(__name__)

CONFIG = json.load(open("config.json", "r"))
API_KEYS = CONFIG["api_keys"]


def requires_auth_key(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        api_key = request.args.get("api_key", None)
        if api_key not in API_KEYS:
            return "Unauthorized", 401
        else:
            if not API_KEYS[api_key]["enabled"]:
                return "Unauthorized", 401
        return func(*args, **kwargs)
    return wrapped


@app.route('/carbon/metrics', methods=["POST"])
@requires_auth_key
def post_metric():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((CONFIG["carbon"]["host"], int(CONFIG["carbon"]["port"])))
    s.send("%s\n" % request.data)
    s.close()
    
    return "OK", 200


@app.route('/carbon/events', methods=["POST"])
@requires_auth_key
def post_event():
    req = urllib2.Request('http://{host}:{port}/events'.format(**CONFIG["graphite"]),
        data=request.data, headers={'Content-type': 'application/json'})
    urllib2.urlopen(req)
    
    return "OK", 200

if __name__ == "__main__":
    app.run(debug=False, use_reloader=False, host="127.0.0.1", port=8081, threaded=True)