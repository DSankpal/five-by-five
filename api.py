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
        return render_template('main.html', comment=None, results=results)

@api.route('/map', methods=['GET'])
def map_page():

    capitals = world.Capitals()
    results = capitals.fetch_captial_locations()
    if request.method == 'GET':
        return render_template('googlemap.html', comment=None, results=results)