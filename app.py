from flask import Flask, render_template, request, jsonify
from datetime import datetime
from pytz import timezone
from connector import facebook
import my_crypto
import atexit
import cf_deployment_tracker
import os
import json
import threading

# Emit Bluemix deployment event
cf_deployment_tracker.track()

app = Flask(__name__)

port = int(os.getenv('PORT', 8000))
my_crypto = my_crypto.MyCrypto()


@app.route('/', methods=['GET'])
def verify():
    resp = facebook.verify(request)
    if resp == None:
        return "ok", 200
    return resp


@app.route('/', methods=['POST'])
def hook():
    resp = facebook.handle(request)
    t = threading.Thread(target=handle, args=(resp,))
    t.start()
    return "ok", 200


def handle(resp):
    my_crypto.handle(resp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
