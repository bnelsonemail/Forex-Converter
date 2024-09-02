from flask import Flask, render_template, request, json, jsonify, redirect
from flask_debugtoolbar import DebugToolbarExtension
from config import logger, DevelopmentConfig # or ProductionConfig, TestingConfig
from dotenv import load_dotenv, find_dotenv
from forex_converter import CurrencyConverter # Import the CurrencyConverter Class
import requests
import os



# load environment variables from the .env file
load_dotenv(find_dotenv())

app = Flask(__name__)

# Call config files
app.config.from_object(DevelopmentConfig)
# app.config['DEBUG'] = 'DEBUG_TB_INTERCEPT_REDIRECTS = True'
debug = DebugToolbarExtension(app)

# Create an instance of the CurrencyConverter
converter = CurrencyConverter()

@app.route('/') # Home Page
def home():
    """
    Renders the home page with the currency conversion form. 
    Handles form submission to calculate and display the converted currency amount.
    """
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
    """
    Handles form submission from the home page, calls the CurrencyConverter 
    class to get the exchange rate, and calculates the converted amount.
    Redirects to convert.html to display the results.
    """
    # Retrieve values from home.html form
    from_currency = request.form.get('from_curr') 
    to_currency = request.form.get('to_curr')
    amount = float(request.form.get('amount'))
    
    try:
        # Get the exchange rate using the CurrencyConverter class
        exchange_rate = converter.get_exchange_rate(from_currency, to_currency)
        
        # Convert the amount to the target currency
        converted_amount = converter.convert_currency(amount, exchange_rate)
        
        # Pass the converted amount and other details to the template
        return render_template('convert.html', 
                               from_currency=from_currency,
                               to_currency=to_currency,
                               amount=amount,
                               converted_amount=converted_amount)
    except Exception as e:
        # Handle errors (e.g., invalid currencies or API errors)
        return f'Error: {str(e)}'
        
    

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)