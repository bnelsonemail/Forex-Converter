from flask import Flask, render_template, request, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from config import TestingConfig # Use DevelopmentConfig, TestingConfig or ProductionConfig
from dotenv import load_dotenv, find_dotenv
from forex_python.converter import CurrencyCodes
from forex_converter import CurrencyConverter
import os

# Load environment variables from the .env file
load_dotenv(find_dotenv())

app = Flask(__name__)

# Call config files
app.config.from_object(TestingConfig) # Use DevelopmentConfig, TestingConfig or ProductionConfig
from dotenv import load_dotenv, find_dotenv
debug = DebugToolbarExtension(app)

# Create an instance of the CurrencyConverter
converter = CurrencyConverter()
c = CurrencyCodes()

@app.route('/')
def home():
    """Renders the home page with the currency conversion form."""
    return render_template('home.html')

@app.route('/table')
def table():
    """Renders table.html which provides a link for users to look up currency codes."""
    return render_template('table.html')

@app.route('/convert')
def convert():
    """Renders the page to display the converted currency requested by the user."""
    if 'converted_amount' in session:
        return render_template('convert.html',
                               from_currency=session['from_currency'],
                               to_currency=session['to_currency'],
                               amount=session['amount'],
                               converted_amount=session['converted_amount'],
                               as_of_date=session['as_of_date'],
                               from_symbol=session['from_symbol'],
                               to_symbol=session['to_symbol'])  # Fixed indentation

    else:
        return redirect('/')

@app.route('/conversion', methods=['POST'])
def conversion():
    """Handles form submission, calls the CurrencyConverter to get the exchange rate, and redirects to /convert."""
    from_currency = request.form.get('from_curr').upper()  # Moved above
    to_currency = request.form.get('to_curr').upper()
    from_symbol = c.get_symbol(from_currency)  # Symbols retrieved after currency extraction
    to_symbol = c.get_symbol(to_currency)
    amount = float(request.form.get('amount'))
    
    try:
        # Convert the amount to the target currency and get the "as of" date
        converted_amount, as_of_date = converter.convert_currency(amount, from_currency, to_currency)
        
        # Store the results in the session
        session['from_currency'] = from_currency
        session['to_currency'] = to_currency
        session['amount'] = amount
        session['converted_amount'] = converted_amount
        session['as_of_date'] = as_of_date
        session['from_symbol'] = from_symbol
        session['to_symbol'] = to_symbol
        
        # Redirect to /convert to display the results
        return redirect('/convert')
    except ValueError as e:
        # Handle invalid currency codes or other conversion errors
        return render_template('home.html', error=str(e)), 400
    except Exception as e:
        # Handle other errors and display them on the error page
        return render_template('error.html', error=str(e)), 500

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)

        
