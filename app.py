from flask import Flask, render_template, request
# from flask_debugtoolbar import DebugToolbarExtension
from config import logger, DevelopmentConfig # or ProductionConfig, TestingConfig
from dotenv import load_dotenv, find_dotenv
# from forex import forex_BTC
import os



# load environment variables from the .env file
load_dotenv(find_dotenv())

app = Flask(__name__)

# Call config files
app.config.from_object(DevelopmentConfig)
# app.config['DEBUG'] = 'DEBUG_TB_INTERCEPT_REDIRECTS = True'
# debug = DebugToolbarExtension(app)

@app.route('/') # Home Page
def home():
    return render_template ('home.html')






if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)