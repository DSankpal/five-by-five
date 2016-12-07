"""Main Entrypoint for the Application"""
import base64
import logging
import json

from flask import Flask, request
from flask import jsonify

import world
import utility

app = Flask(__name__)

@app.route('/')
def hello_world():
    """hello world"""
    return 'Hello World!'


@app.route('/api/status')
def status():
    """service status"""
    statuses = {
          'insert': True,
          'fetch': False,
          'delete': False,
          'list': True
        }
    return json.dumps(statuses)



@app.route('/api/capitals/', methods=['PUT', 'GET', 'DELETE'])
def access_notes():
    """inserts captials to datastore"""
    if request.method == 'PUT':
        id = request.args.get('id')
        capitals = world.Capitals()
        print json.dumps(request.get_json())
        city = request.get_json()
        try:
            capitals.store_capital(id, city)
            return 'Successfully stored the capital', 200
        except Exception as e:
            logging.exception(e)
            return 'Unexpected error', 400


    elif request.method == 'GET':
        capitals = world.Capitals()
        try:
            results = capitals.fetch_capitals()
            return jsonify(results)
        except Exception as e:
            logging.exception(e)
            return 'Unexpected error', 400

    elif request.method == 'DELETE':
        id = request.args.get('id')
        cap = world.Capitals()
        try:
            cap.delete_capital(id)
            return "Capital object delete status", 200
        except AttributeError as e:
            logging.exception(e)
            return "Capital record not found", 404
        except:
            return "Unexpected error", 400


@app.route('/pubsub/receive', methods=['POST'])
def pubsub_receive():
    data = {}
    try:
        obj = request.get_json()
        utility.log_info(json.dumps(obj))
        data = base64.b64decode(obj['message']['data'])
        utility.log_info(data)
    except Exception as e:
        logging.exception(e)
    return jsonify(data), 200


@app.errorhandler(500)
def server_error(err):
    """Error handler"""
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(err), 500


if __name__ == '__main__':
    # Used for running locally
    app.run(host='127.0.0.1', port=8080, debug=True)
