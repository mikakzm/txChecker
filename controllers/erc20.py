from flask import request, Response
from configparser import ConfigParser
import requests
import json

config = ConfigParser()
config.read('config.cfg')

    
transferMethod = "a9059cbb000000000000000000000000"

def erc20(coin):
    to, value, txid = request.json['to'], request.json['value'], request.json['txid']
    url = config['ERC20']['url'] + txid
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

    if 'execution_error' in content:
        return failed_transaction('NOT_PAID', 'transaction is reverted by the blockchain')

    outputs  = content['outputs'][0]

    if outputs['addresses'][0] != config['ERC20'][coin]:
        return failed_transaction('NOT_PAID', 'token does not match')
    
    transactionData = outputs['script']
    _method = transactionData[0:32]
    _to = '0x'+ transactionData[32:72]
    _value = int(transactionData[72:], 16)
    decimal = config['DECIMAL']['ERC20_' + coin]

    if _method != transferMethod: 
        return failed_transaction('NOT_PAID', 'wallet does not match')

    if _to != to: 
        return failed_transaction('NOT_PAID', 'wallet does not match')

    if _value != float(value) * (10 ** int(decimal)): 
         return failed_transaction('NOT_PAID', 'value does not match')

    return satisfied_transaction('PAID')

