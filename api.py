from flask import Blueprint, render_template, request, redirect, url_for

import world


api = Blueprint('capitals', __name__)


@api.route('/', methods=['GET'])
def main_page():

    capitals = world.Capitals()
    results = capitals.fetch_countries_and_capitals()
    # x = list()
    # for k, v in results.items():
    #     x.append([k, v])
    if request.method == 'GET':
        return render_template('main.html', comment=None, results=sorted(results.items()))

@api.route('/map', methods=['GET'])
def map_page():

    capitals = world.Capitals()
    results = capitals.fetch_capital_locations()
    num_return = min(19, len(results))
    # first20orless = {k: results[k] for k in results.keys()[:num_return]}
    if request.method == 'GET':
        return render_template('googlemap.html', comment=None, results=results[:num_return])

