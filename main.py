from flask import Flask, request
import json
import socket
import urllib.request as urllib2
import re
from functools import wraps

application = Flask(__name__)

CONFIG = json.load(open("config.json", "r"))
API_KEYS = CONFIG["api_keys"]


def requires_auth_key(func):
    @wraps(func)
    def wrapplicationed(*args, **kwargs):
        api_key = request.form.get("api_key", None)
        if api_key not in API_KEYS:
            return "Unauthorized", 401
        else:
            if not API_KEYS[api_key]["enabled"]:
                return "Unauthorized", 401
        return func(*args, **kwargs)
    return wrapped


@application.route('/carbon/metrics', methods=["POST"])
@requires_auth_key
def post_metric():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((CONFIG["carbon"]["host"], int(CONFIG["carbon"]["port"])))
    except Exception as e:
        return "<h2>Error: %s</h2>" % e, 500
    else:
        data = request.form.get('data');
        if (data != None):
            data = re.findall("([\w\.]+\ [\S]+\ [\d]+)",request.form.get('data'), re.MULTILINE);
        else:
            data = request.form.getlist('data[]')

        sentCmd = 0
        for str in data:
            str = re.findall("([\w\.]+\ [\S]+\ [\d]+)",str);
            str = str[0]
            if (len(str) < 10):
                continue
            str += "\n"
            #print(("Send:"+str).encode('utf8'))
            s.send(b"%s" % str.encode('utf8'))
            sentCmd+=1
        s.close()
        if sentCmd < 1:
            return "NOTHING SENT TO SERVER. BAD FORMATED STRING/VAR?", 202
        return "OK", 200
    return "Unkown error", 500

@application.route('/carbon/events', methods=["POST"])
@requires_auth_key
def post_event():
    req = urllib2.Request('http://{host}:{port}/events'.format(**CONFIG["graphite"]),
        data=request.form.get('data').encode('utf8'), headers={'Content-type': 'application/json'})
    try:
        urllib2.urlopen(req)
    except Exception as e:
        return "<h2>Error: %s</h2>" % e, 500
    else:    
        return "OK", 200

    return "Unkown error", 500


if __name__ == "__main__":
    application.run(debug=False, use_reloader=False, host="127.0.0.1", port=8081, threaded=True)
