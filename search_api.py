import flask
from flask import request, jsonify
import search

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Search API</h1>"

@app.route('/amazon/', methods=['GET'])
def amazon_search():
    if 'text' in request.args:
        searchText = request.args['text']
    return jsonify(search.search("amazon",searchText))

@app.route('/flipkart/', methods=['GET'])
def flipkart_search():
    if 'text' in request.args:
        searchText = request.args['text']
    return jsonify(search.search("flipkart",searchText))

@app.route('/all/', methods=['GET'])
def all_search():
    if 'text' in request.args:
        searchText = request.args['text']
    return jsonify(search.search("allSites",searchText))

app.run()