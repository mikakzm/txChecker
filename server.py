from operator import ne
from flask import Flask, request, jsonify, Response
from configparser import ConfigParser
import redis
import requests
import json
import controllers

config = ConfigParser()
config.read('config.cfg')

r = redis.StrictRedis(host='127.0.0.1', port=6379, charset="utf-8", decode_responses=True)

routes = [
    (['POST'], '/TRC20/<coin>', controllers.trc20),
    (['POST'], '/ERC20/<coin>', controllers.erc20),
]

app = Flask(__name__)

for route_configs in routes:
    methods, path, controller = route_configs
    app.add_url_rule(rule=path, view_func=controller, methods=methods)
