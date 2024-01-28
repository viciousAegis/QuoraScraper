from flask import Flask, request
import os
import requests

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/scrape', methods=['POST'])
def scrape_data():
    # get params from request
    search_terms = request.args.get('search_terms')

    print(search_terms)

    # call scraper.py
    # return json
