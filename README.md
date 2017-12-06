# Graphite/Carbon REST API

Relay that takes authenticated HTTP POSTs with Carbon metrics and pushes them to Carbon daemon

To start it, copy the wusgi-restapi.ini to /etc/wusgi/apps-enabled/ and restart wusgi. (if not used with docker).

app.py is a symlink to main.py - wusgi starts the app.py.
You can send multiple data lines like this:
curl -d "api_key=eede9899-3937-4116-97ba-31ac892ba780&data[]=\"local.random.testrest3 $((RANDOM % 100)) `date +%s`\"&data[]=\"local.random.testrest4 $((RANDOM % 1)) `date +%s`\"" http://relayhost/carbon/metrics
or like this:
or single lines data:
curl -d "api_key=eede9899-3937-4116-97ba-31ac892ba780&data[]=\"local.random.testrest3 $((RANDOM % 100)) `date +%s`\"" http://relayhost/carbon/metrics
or
curl -d "api_key=eede9899-3937-4116-97ba-31ac892ba780&data=\"local.random.testrest3 $((RANDOM % 100)) `date +%s`\"" http://relayhost/carbon/metrics

it's now parsing the data string and only a match "STR STR INT" is sent to the server.
