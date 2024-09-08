from forex_python.converter import CurrencyCodes
from datetime import datetime
import os
import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class CurrencyConverter:
    """
    A class to handle currency conversion by fetching exchange rates from an external API.

    This class uses the CurrencyAPI to retrieve the latest exchange rates between different
    currencies. It can validate currency codes, fetch exchange rates, convert amounts between
    currencies, and retrieve currency symbols.
    """
    def __init__(self):
        """
        Initializes the CurrencyConverter with an API access key and base URL.
        """
        self.apikey = os.getenv('APIKEY')
        self.base_url = 'https://api.currencyapi.com/v3/latest'
        self.valid_currency_codes = CurrencyCodes().get_currency_name
        self.symbols = CurrencyCodes().get_symbol
    
    def validate_currency_code(self, currency_code: str) -> bool:
        """
        Validates the given currency code.
        """
        return bool(self.valid_currency_codes(currency_code.upper()))

    def get_symbols(self, from_currency: str, to_currency: str) -> tuple:
        """
        Fetches the currency symbols for the given currency codes.
        """
        if not self.validate_currency_code(from_currency):
            raise ValueError(f"Invalid currency code: {from_currency}")
        
        if not self.validate_currency_code(to_currency):
            raise ValueError(f"Invalid currency code: {to_currency}")

        from_symbol = self.symbols(from_currency.upper())
        to_symbol = self.symbols(to_currency.upper())
        
        return from_symbol, to_symbol

    def get_exchange_rate(self, from_currency: str, to_currency: str, endpoint: str = 'latest') -> tuple:
        """
        Fetches the exchange rate for the specified currency pair.
        """
        if not self.validate_currency_code(from_currency):
            raise ValueError(f"Invalid currency code: {from_currency}")
        if not self.validate_currency_code(to_currency):
            raise ValueError(f"Invalid currency code: {to_currency}")

        url = f'{self.base_url}'
        querystring = {
            'base_currency': from_currency,
            'currencies': to_currency,
            'apikey': self.apikey,
        }

        response = requests.get(url, params=querystring)
        if response.status_code == 200:
            data = response.json()

            if 'data' in data and to_currency in data['data']:
                exchange_rate = data['data'][to_currency]['value']
                last_updated_at = data['data'][to_currency].get('last_updated_at')

                # Convert ISO 8601 date to a human-readable format
                if last_updated_at:
                    as_of_date = datetime.fromisoformat(last_updated_at).strftime('%Y-%m-%d')
                else:
                    as_of_date = datetime.now().strftime('%Y-%m-%d')

                return exchange_rate, as_of_date
            else:
                raise ValueError(f'Could not find exchange rate for {from_currency} to {to_currency}. Full data: {data}')
        else:
            raise ValueError(f"API request failed with status code: {response.status_code}")

    def convert_currency(self, amount: float, from_currency: str, to_currency: str) -> tuple:
        """
        Converts the specified amount from one currency to another using the latest exchange rate.
        """
        exchange_rate, as_of_date = self.get_exchange_rate(from_currency, to_currency)
        converted_amount = amount * exchange_rate
        return converted_amount, as_of_date




