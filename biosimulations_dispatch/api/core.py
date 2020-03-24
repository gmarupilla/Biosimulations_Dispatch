import json
import os
from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, request, redirect, url_for, abort, jsonify
from flask_cors import CORS, cross_origin
from biosimulations_dispatch.config import Config
from biosimulations_dispatch.hpc_manager import HPCManager

class PrefixMiddleware:
    def __init__(self, app, prefix=''):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):
        if environ['PATH_INFO'].startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
            return self.app(environ, start_response)
        else:
            start_response('404', [('Content-Type', 'text/plain')])
            return ["This url does not belong to the app.".encode()]


app = Flask(__name__)
cors = CORS(app)

app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='')
app.wsgi_app = ProxyFix(app.wsgi_app)
@app.route('/dispatch', methods=['POST'])
@cross_origin()
def dispatch_to_hpc():
    if request.method == 'POST' and request.remote_addr in Config.ALLOWED_ORIGINS:
        try:
            hpc_manager = HPCManager(username=Config.HPC_USER, password=Config.HPC_PASS, server=Config.HPC_HOST, sftp_server=Config.HPC_SFTP_HOST)
            data = request.get_json()
            hpc_manager.dispatch_job(
                # TODO: parse simulator from sim spec within dispatch_job
                    simulator = data['simSpec']['simulator'],
                    value_dict = data['simSpec'],
                    sedml = data['sedml'],
                    sedml_name = data['sedmlName'],
                    sbml = data['sbml'],
                    temp_dir = Config.TEMP_DIR
                )
            return jsonify({"message": 'Simulation has been successfully dispatched to HPC'}), 200
        except BaseException as ex:
            return jsonify({'message': "Error occured: " + str(ex)}), 400
    elif request.remote_addr not in Config.ALLOWED_ORIGINS:
        return jsonify({'message': 'Requester origin \'{}\' is not allowed'.format(request.remote_addr)}), 400
    else:
        return jsonify({'message': 'Bad request'}), 400