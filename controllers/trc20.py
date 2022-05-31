from flask import request, Response
from configparser import ConfigParser
import requests
import json

config = ConfigParser()
config.read('config.cfg')

def trc20(coin):
    to, value, txid = request.json['to'], request.json['value'], request.json['txid']
    url = config['TRC20']['url'] + txid
    r = requests.get(url)

    def failed_transaction(status, info):
        return Response(
            json.dumps({'tx_status': status,'info': info}),
            status = 200,
            mimetype='application/json'
        )

    def satisfied_transaction(status):
        return Response(
            json.dumps({'tx_status': status}),
            status = 200,
            mimetype='application/json'
        )

    if r.status_code != 200 :
        return failed_transaction('UNREACHABLE', "can't connect to blockchain")
        
    content = json.loads(r._content)
    decimal = config['DECIMAL']['TRC20_' + coin]

    if content['revert'] != False or content['contractRet'] != "SUCCESS":
        return failed_transaction('NOT_PAID', 'transaction is reverted by the blockchain')

    trigget_info  = content['trigger_info']

    if trigget_info['contract_address'] != config['TRC20'][coin]:
        return failed_transaction('NOT_PAID', 'token does not match')
    
    if trigget_info['parameter']['_to'] != to: 
        return failed_transaction('NOT_PAID', 'wallet does not match')

    if float(trigget_info['parameter']['_value']) != float(value) * (10 ** int(decimal)): 
         return failed_transaction('NOT_PAID', 'value does not match')

    return satisfied_transaction('PAID')

