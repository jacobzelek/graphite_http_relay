from flask import Flask, request
app = Flask(__name__)

API_KEY = "1234567890"

@app.route('/metrics', methods=["POST"])
def post_metric():
    if request.headers.get("x-auth-token", None) == API_KEY:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", 2003))
        s.send(request.body)
        s.close()

    return "OK", 200
