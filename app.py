from flask import Flask, render_template, request, json, jsonify, redirect
from flask_debugtoolbar import DebugToolbarExtension
from config import logger, DevelopmentConfig # or ProductionConfig, TestingConfig
from dotenv import load_dotenv, find_dotenv
#from forex_converter import forex_BTC
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


@app.route('/conversion')
def conversion():
    """Calls the API and returns values.  Redirects to convert.html"""
    return redirect('/convert')




if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)