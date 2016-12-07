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


@app.route('/notes', methods=['POST', 'GET'])
def access_notes():
    """inserts and retrieves notes from datastore"""

    book = world.Capitals()
    if request.method == 'GET':
        results = book.fetch_notes()
        result = [world.parse_note_time(obj) for obj in results]
        return jsonify(result)
    elif request.method == 'POST':
        print json.dumps(request.get_json())
        text = request.get_json()['text']
        book.store_note(text)
        return "done"


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
