from flask import Flask, request
from tronapi import Tron
from flask_jsonschema_validator import JSONSchemaValidator
from datetime import datetime, timedelta

import json
import os

# https://api.shasta.trongrid.io - test net
# https://api.trongrid.io - main net

nodes_URL = os.getenv("NODES_URL","https://api.shasta.trongrid.io")

app = Flask(__name__)
JSONSchemaValidator( app = app, root = "schemas" )

full_node = nodes_URL
solidity_node = nodes_URL
event_server = nodes_URL

tron = Tron(full_node=full_node,
            solidity_node=solidity_node,
            event_server=event_server)

@app.before_request
def before_request():
    if not request.authorization:
        return

    tron.private_key = request.authorization['password']
    tron.default_address = request.authorization['username']

def require_auth(func):
	def wrapper():
		if not tron.private_key or tron.default_address:
				print('Credentials were not set')
				return wrapper
		func()
		return wrapper 

@app.route('/create-account', methods = ['POST'])
def create_account():
	account = tron.create_account
	body = {'result':'OK','address':account.address.hex,'public_key':account.public_key, 'private_key':account.private_key}

	return json.dumps(body), 200

@require_auth
@app.validate('send-tokens', 'send-tokens' )
@app.route('/send-tokens', methods = ['POST'])
def send_tokens():
	data = request.get_json()

	transaction = tron.transaction_builder.send_token(data['to'],data['amount'],data['tokenID'])
	return tron.trx.sign_and_broadcast(transaction), 200

@require_auth
@app.validate('send-trx', 'send-trx' )
@app.route('/send-trx', methods = ['POST'])
def send_trx():
	data = request.get_json()

	return tron.trx.send_transaction(data['to'], data['amount'])

@require_auth
@app.validate('create-token', 'create-token' )
@app.route('/create-token', methods = ['POST'])
def create_token():
	data = request.get_json()

	start = int(datetime.now().timestamp() * 1000)
	end = int((datetime.now() + timedelta(days=int(data['sale_period']))).timestamp() * 1000)

	transaction = tron.transaction_builder.create_token(name=data['name'],
														url=data['url'],
														abbreviation=data['abbreviation'],
														description=data['description'],
														totalSupply=data['total_supply'],
														frozenAmount=data['frozen_amount'],
														frozenDuration=data['frozen_duration'],
														freeBandwidth=data['free_bandwidth'],
														freeBandwidthLimit=data['free_bandwidth_limit'],
														saleStart=start,#data['sale_start'],
														saleEnd=end,#data['sale_end'],
														precision=data['precision'],
														voteScore=data['vote_score'])
	return tron.trx.sign_and_broadcast(transaction), 200

@app.validate('get-balance', 'get-balance' )
@app.route('/get-balance', methods = ['GET'])
def get_account_balance():
	data = request.get_json()
	result = {}
	for adr in data['addresses']:
		info = tron.trx.get_account(address=adr)
		result[adr] = {}
		result[adr]['TRX'] = tron.trx.get_balance(address=adr)
		if 'assetV2' in info:
			for token in info['assetV2']:
				result[adr][token['key']] = token['value']

	return json.dumps(result), 200

#getassetissuebyid
def handle_internal_server_error(e):
    return 'Internal server error', 500

def handle_bad_request(e):
    return 'Bad request', 400

app.register_error_handler(400, handle_bad_request)
app.register_error_handler(500, handle_internal_server_error)

app.run(host="0.0.0.0")