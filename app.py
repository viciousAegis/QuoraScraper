from flask import Flask, request
from flask_cors import CORS, cross_origin
import subprocess

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

def run_scraper(post_count):
    # call scraper.py
    subprocess.Popen(['python3', 'run.py', '-c', str(post_count)])

@app.route('/scrape', methods=['POST'])
@cross_origin(supports_credentials=True, origins='*')
def scrape_data():
    # get params from request
    search_terms = request.json['search_terms']
    try:
        post_count = request.json['post_count']
    except:
        post_count = 10

    print(search_terms)
    # populate search.terms file
    with open('./search.terms', 'w') as f:
        for search_term in search_terms:
            f.write(search_term + '\n')

    # run scraper.py
    run_scraper(post_count)
    
    return 'running scraper.py'
