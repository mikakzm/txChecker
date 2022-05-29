from operator import ne
from flask import Flask, request, jsonify, Response
from configparser import ConfigParser
import redis
import requests
import json

config = ConfigParser()
config.read('config.cfg')

def trc20(coin):
    to, value, txid = request.json['to'], request.json['value'], request.json['txid']
    url = config['TRC20']['url'] + txid
    r = requests.get(url)
    if r.status_code != 200 :
        return Response(
            json.dumps({'tx_status': "UNREACHABLE",'info': 'transaction is reverted by the evm'}),
            status = 200,
            mimetype='application/json'
        )

    content = json.loads(r._content)

    if content['revert'] != False or content['contractRet'] != "SUCCESS":
        return Response(
            json.dumps({'tx_status': "NOT_PAID",'info': 'transaction is reverted by the evm'}),
            status = 200,
            mimetype='application/json'
        )
    trigget_info  = content['trigger_info']

    if trigget_info['contract_address'] != config['TRC20'][coin]:
        return Response(
            json.dumps({'tx_status': "NOT_PAID",'info': 'token does not match'}),
            status = 200,
            mimetype='application/json'
        )
    
    if trigget_info['parameter']['_to'] != to: 
        return Response(
            json.dumps({'tx_status': "NOT_PAID",'info': 'wallet does not match'}),
            status = 200,
            mimetype='application/json'
        )

    if trigget_info['parameter']['_value'] != value: 
        return Response(
            json.dumps({'tx_status': "NOT_PAID",'info': 'value does not match'}),
            status = 200,
            mimetype='application/json'
        )

    return Response(
        json.dumps({'tx_status': 'PAID'}),
        status = 200,
        mimetype='application/json'
    )

