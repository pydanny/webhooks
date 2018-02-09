import os
import time
from datetime import datetime, timedelta
from flask import Flask, request, abort, jsonify
import json

def temp_token():
    import binascii
    temp_token = binascii.hexlify(os.urandom(24))
    return temp_token.decode('utf-8')

WEBHOOK_VERIFY_TOKEN = os.getenv('WEBHOOK_VERIFY_TOKEN')
CLIENT_AUTH_TIMEOUT = 24 # in Hours

app = Flask(__name__)

authorized_clients = {}
check_auth = False
delay_seconds = 0.020

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    time.sleep(delay_seconds)
    if request.method == 'GET':
        verify_token = request.headers.get('token', None)
        if verify_token == WEBHOOK_VERIFY_TOKEN:
            authorized_clients[request.remote_addr] = datetime.now()
            return jsonify({'status':'success'}), 200
        else:
            return jsonify({'status':'bad token'}), 401

    elif request.method == 'POST':
        client = request.remote_addr
        if not check_auth or client in authorized_clients:
            if check_auth and datetime.now() - authorized_clients.get(client) > timedelta(hours=CLIENT_AUTH_TIMEOUT):
                authorized_clients.pop(client)
                return jsonify({'status':'authorisation timeout'}), 401
            else:
                print(request.data)
                return jsonify({'status':'success' \
                                   , 'received_data: ' : request.data.decode('utf-8')
                                }), 200
        else:
            return jsonify({'status':'not authorised'}), 401

    else:
        abort(400)

if __name__ == '__main__':
    if WEBHOOK_VERIFY_TOKEN is None:
        print('WEBHOOK_VERIFY_TOKEN has not been set in the environment.\nGenerating random token...')
        token = temp_token()
        print('Token: %s' % token)
        WEBHOOK_VERIFY_TOKEN = token
    app.run(port=5001)



