
from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS
import json
import sys
sys.path.append('../')  # nopep8
from functions.original_script import *


if "prod" in os.environ:
    load_dotenv('./.env')


app = Flask(__name__)
CORS(app, origins=[os.environ.get('frontend')])


@app.route('/apiv1', methods=["POST"])
def apiv1():
    # get request post body
    data = json.loads(request.data)
    if 'url' not in data:
        return {'ok': False, 'error': 'Invalid request.'}
    url = data['url'].lower()
    # if link is less that 10 characters or airbnb.com is not found within the first 25 characters
    if len(url) < 10 or 'airbnb.com' not in url[0:25]:
        return {'ok': False, 'error': 'Invalid link..'}

    # call scraper with the url
    scrape_results = main(url)
    if scrape_results[0] == False:
        return {'ok': False, 'error': scrape_results[1]}
    elif scrape_results[0] == True:
        return {'ok': True, 'link': scrape_results[1], 'data': scrape_results[2]}


@app.route('/')
def home():
    return 'Hello test path'
