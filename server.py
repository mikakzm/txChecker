from flask import Flask
from configparser import ConfigParser
import controllers
import middlewares

config = ConfigParser()
config.read('config.cfg')

routes = [
    (['POST'], '/TRC20/<coin>', controllers.trc20, [
        middlewares.error_handling_wrapper
    ]),
    (['POST'], '/ERC20/<coin>', controllers.erc20, [
        middlewares.error_handling_wrapper
    ]),
]

app = Flask(__name__)

for route_configs in routes:
    methods, path, controller, middlewares_to_apply = route_configs
    for mw in middlewares_to_apply:
        controller = mw(controller)
    app.add_url_rule(rule=path, view_func=controller, methods=methods)
