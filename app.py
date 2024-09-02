from flask import Flask, render_template, request, json, jsonify, redirect
from flask_debugtoolbar import DebugToolbarExtension
from config import logger, DevelopmentConfig # or ProductionConfig, TestingConfig
from dotenv import load_dotenv, find_dotenv
#from forex_converter import forex_BTC
import requests
import os



# load environment variables from the .env file
load_dotenv(find_dotenv())

app = Flask(__name__)

# Call config files
app.config.from_object(DevelopmentConfig)
# app.config['DEBUG'] = 'DEBUG_TB_INTERCEPT_REDIRECTS = True'
debug = DebugToolbarExtension(app)

@app.route('/') # Home Page
def home():
    """Renders Home Page with a form for user input to convert currency rates"""
    return render_template ('home.html')


@app.route('/table')
def table():
    """Renders table.html which provides a link for user to look up currency codes"""
    return render_template('table.html')


@app.route('/convert')
def convert():
    """Renders Page to display the converted currency requested by user"""
    return render_template('convert.html')


@app.route('/conversion', methods=['GET', 'POST'])
def conversion():
    """Calls the API and returns values. Redirects to convert.html"""

    
        
    
    # Get the access key from the .env file
    access_key = os.getenv('ACCESS_KEY')

    # Define the URL and parameters
    url = 'https://api.exchangerate.host/live'
    params = {
        'access_key': access_key
    }

    # Make the GET request to the API
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        
        # Process the data from user
        # Retrieve values from home.html form
        from_currency = request.form.get('from_curr') 
        to_currency = request.form.get('to_curr')
        amount = request.form.get('amount') 
    
        # TODO: perform calculation from forex_converter.py script
        
        
        # redirect to convert.html
        return render_template('convert.html', data=data)
    else:
        # Handle the error
        return f"Error: {response.status_code}"




if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)