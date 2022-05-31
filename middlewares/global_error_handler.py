from flask import Response
import json

def error_handling_wrapper(controller):
    def wrapped_controller(**argc):
        try:
            return controller(**argc)
        except Exception as err:
            print(err)
            return Response(
                json.dumps({'info': 'internal error'}),
                status = 400,
                mimetype='application/json'
            )
    
    return wrapped_controller