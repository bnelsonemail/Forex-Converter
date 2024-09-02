from forex_python.converter import CurrencyCodes, CurrencyRates 
from datetime import date, datetime
import os
import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class CurrencyConverter:
    """A class to handle currency conversion by fetching exchange rates from an external API."""
    def __init__(self):
        """Initializes the CurrencyConverter with an API access key and base URL."""
        self.access_key = os.getenv('ACCESS_KEY')
        self.base_url = 'https://api.exchangerate.host/'
        
    def get_exchange_rate(self, from_currency: str, to_currency: str, endpoint: str = 'live') -> tuple:
        """
        Fetches the exchange rate for the specified currencies using a specified endpoint.

        Args:
            from_currency (str): The currency to convert from (e.g., 'USD')
            to_currency (str): The currency to convert to (e.g., 'EUR')
            endpoint (str): The API endpoint to use (e.g., 'live'). Defaults to 'live'.

        Returns:
            tuple: A tuple containing the exchange rate (rounded to two decimal places) and the "as of" date.
        
        Raises:
            ValueError: If the exchange rate could not be retrieved from the API.
        """
        url = f'{self.base_url}/{endpoint}'
        params = {
            'base': from_currency,
            'symbols': to_currency,
            'access_key': self.access_key,
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            parse_currency = (from_currency + to_currency).upper()
            exchange_rate = data['quotes'].get(parse_currency)
            timestamp = data.get('timestamp')
            
            if exchange_rate:
                # Round to 2 decimal places
                exchange_rate = round(exchange_rate, 2)
                
                # Convert the timestamp to a readable date
                as_of_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                
                return exchange_rate, as_of_date
            else:
                raise ValueError(f'Could not find exchange rate for {parse_currency}. Full data: {data}')
        else:
            raise ValueError(f"API request failed with status code: {response.status_code}")

    def convert_currency(self, amount: float, from_currency: str, to_currency: str) -> tuple:
        """
        Converts the specified amount from one currency to another.

        Args:
            amount (float): The amount of money to convert.
            from_currency (str): The currency to convert from.
            to_currency (str): The currency to convert to.

        Returns:
            tuple: A tuple containing the converted amount and the "as of" date.
        """
        exchange_rate, as_of_date = self.get_exchange_rate(from_currency, to_currency)
        converted_amount = amount * exchange_rate
        return converted_amount, as_of_date

    

