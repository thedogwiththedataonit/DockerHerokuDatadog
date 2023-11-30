from ddtrace import tracer, patch, patch_all
from flask import Flask, request, jsonify, logging
from flask_cors import CORS
import requests as req
import time
import os
import logging
import sys
patch(logging=True)
patch_all()

port = int(os.environ.get("PORT"))
#DD_LOGS_INJECTION=true DD_SERVICE="giants" DD_ENV="officehours" DD_VERSION="1" ddtrace-run python3 application.py
#DD_LOGS_INJECTION=true DD_VERSION="1" ddtrace-run python3 application.py

FORMAT = ('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] '
          '[dd.service=%(dd.service)s dd.env=%(dd.env)s dd.version=%(dd.version)s dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] '
          '- %(message)s')

#logging.basicConfig(format=FORMAT, stream=sys.stdout)
logging.basicConfig(format=FORMAT, filename='logfile.log')
log = logging.getLogger(__name__)
log.level = logging.INFO



requests = req.Session()
application = Flask(__name__)
CORS(application)
tracer.configure(hostname='localhost', port=8126) #USE LOCAL HOST FOR FARGATE

#DD_SERVICE="sdr" DD_ENV="dev" DD_LOGS_INJECTION=true ddtrace-run python my_app.py


## Routes ##
@application.route('/', methods=['GET'])
def home():
    return jsonify("Welcome to the home page!")

@application.route('/api/getRequest', methods=['GET'])
@tracer.wrap(service="getRequest", resource="getRequest")
def get_request():
    
    #add logging info msg
    log.info('get request called!')
    span = tracer.current_span()
    span.set_tags({'information': 'This is a custom value from a get request'})
    data = database_query("this is a get request")
    return jsonify(data)

@application.route('/api/snack', methods=['POST'])
@tracer.wrap(service="snack", resource="snack")
def snack():
    data = request.json
    name = data['name']
    snack = data['snack']
    
    log.info(f'{name} likes {snack}')
    asc_time = time.asctime()
    level_name = logging.getLevelName(log.level)
    log_string = f'{asc_time} {level_name} [{__name__}] [application.py:420] - {name} likes {snack}'
    tracer.set_tags({'information': f'{name} likes {snack}'})

    
    return jsonify({"status":"success", "log":log_string})


@application.route('/api/postRequest', methods=['POST'])
@tracer.wrap(service="postRequest", resource="postRequest")
def post_request():
    log.info('post request called!')
    tracer.set_tags({'information': 'This is a custom value from a post request'})
    data = request.json
    database_query(data)
    return jsonify("The data sent was " + data)


@application.route('/api/getErrorRequest', methods=['GET'])
@tracer.wrap(service="errorRequest", resource="errorRequest")
def error_request():
    log.error('error request called!')
    tracer.set_tags({'information': 'ERROR ERROR!!'})
    tracer.set_tags({'data': "some kind of error here..."})
    error_trigger()
    return jsonify("error triggered")

## Functions ##

@tracer.wrap(service="database", resource="query")
def database_query(data):
    time.sleep(1)
    log.info('database called!')
    tracer.set_tags({'data': data,
                    "test": "yes"})
    return "This is a database query"

@tracer.wrap(service="perculiar_function", resource="SOS")
def error_trigger():
    time.sleep(1)
    log.info('strange function called...')
    tracer.set_tags({'data': "error"})
    raise ValueError("error!")


if __name__ == '__main__':
    application.run(port=port, host="0.0.0.0", threaded=True)# host="0.0.0.0") #debug=True for tracing client debug logs
