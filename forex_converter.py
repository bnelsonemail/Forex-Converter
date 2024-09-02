from forex_python.converter import CurrencyCodes, CurrencyRates 
from datetime import date, datetime # import the date and datetime modules from datetime library
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
        
    def get_exchange_rate(self, from_currency:str, to_currency: str, endpoint: str = 'live') -> float:
        """
        Fetches the exchange rate for the specified currencies using a specified endpoint.

        Args:
            from_currency (str): The currency to convert from (e.g., 'USD')
            to_currency (str): The currency to conver to (e.g., 'EUR')
            endpoint (str): The API endpoint to use (e.g., 'live'). Defaults to 'live'.

        Returns:
            float: The exchange rate between the two currencies.
        
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
        data = response.json()
        
        exchange_rate = data['rates'].get(to_currency)
        if exchange_rate:
            return exchange_rate
        else:
            raise ValueError('Could not retrieve exchange rate')


