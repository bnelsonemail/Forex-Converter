from flask import Flask, render_template, request, json, jsonify, redirect, session, Response
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
    # Retrieve the data from the session
    if 'converted_amount' in session:
        from_currency = session['from_currency']
        to_currency = session['to_currency']
        amount = session['amount']
        converted_amount = session['converted_amount']
        return render_template('convert.html', 
                                from_currency=from_currency,
                                to_currency=to_currency,
                                amount=amount,
                                converted_amount=converted_amount)
    else:
        return redirect('/') # Redirect to home if there is no conversion data


@app.route('/conversion', methods=['POST'])
def conversion():
    """
    Handles form submission from the home page, calls the CurrencyConverter 
    class to get the exchange rate, and calculates the converted amount.
    Redirects to /convert to display the results.
    """
    # Retrieve values from the form
    from_currency = request.form.get('from_curr') 
    to_currency = request.form.get('to_curr')
    amount = float(request.form.get('amount'))
    
    try:
        # Debugging: Print the form values
        print('****************************************')
        print(f"From Currency: {from_currency}, To Currency: {to_currency}, Amount: {amount}")
        print('****************************************')
        
                # Make the API request to exchangerate.host
        url = "https://api.exchangerate.host/live"
        params = {
            'base': from_currency,
            'symbols': to_currency
        }
        response = requests.get(url, params=params)  # This line defines `response`
        
        # Get the exchange rate using the CurrencyConverter class
        exchange_rate = converter.get_exchange_rate(from_currency, to_currency)
        
        # Debugging: Print the raw response text
        print(f"++++++++++++++++++++++++++++++++++++++++")
        print(f"API Response: {response.text}")
        print(f"+++++++++++++++++++++++++++++++++++++++++")
        
        # Check if the request was successful and parse JSON
        if response.status_code == 200:
            data = response.json()
            exchange_rate = data.get('end_rate', {}).get(to_currency)
            if not exchange_rate:
                raise ValueError(f"Could not find exchange rate for {to_currency}.")
        
        
        # Convert the amount to the target currency
        converted_amount = converter.convert_currency(amount, exchange_rate)
        
        # Store the results in the session
        session['from_currency'] = from_currency
        session['to_currency'] = to_currency
        session['amount'] = amount
        session['converted_amount'] = converted_amount
        
        # Redirect to /convert to display the results
        return redirect('/convert.html')
    except Exception as e:
        # Debugging: Print the error
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print(f"Error occurred: {str(e)}")
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        # Handle errors (e.g., invalid currencies or API errors)
        return render_template('error.html', error=str(e)), 500

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
        
