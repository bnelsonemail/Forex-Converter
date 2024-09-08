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

        The API key is loaded from the environment using dotenv. The base URL is the
        endpoint for fetching the latest currency exchange rates.

        Attributes:
            apikey (str): The API key required to authenticate with the CurrencyAPI.
            base_url (str): The base URL for accessing the latest exchange rates.
            valid_currency_codes (callable): Method from the forex_python package that retrieves currency names.
            symbols (callable): Method from the forex_python package that retrieves currency symbols.
        """
        self.apikey = os.getenv('APIKEY')
        self.base_url = 'https://api.currencyapi.com/v3/latest'
        self.valid_currency_codes = CurrencyCodes().get_currency_name
        self.symbols = CurrencyCodes().get_symbol
    
    def validate_currency_code(self, currency_code: str) -> bool:
        """
        Validates the provided currency code.

        Checks if the given ISO 4217 currency code is valid using the forex_python package.

        Args:
            currency_code (str): The ISO 4217 currency code (e.g., 'USD', 'EUR').

        Returns:
            bool: True if the currency code is valid, False otherwise.
        """
        return bool(self.valid_currency_codes(currency_code.upper()))

    def get_symbols(self, from_currency: str, to_currency: str) -> tuple:
        """
        Retrieves the currency symbols for the provided currency codes.

        Validates the provided currency codes and fetches their symbols using the forex_python package.

        Args:
            from_currency (str): The currency code to convert from (e.g., 'USD').
            to_currency (str): The currency code to convert to (e.g., 'EUR').

        Returns:
            tuple: A tuple containing the symbols for the from_currency and to_currency.

        Raises:
            ValueError: If any of the provided currency codes are invalid.
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

        Makes an API request to fetch the exchange rate for the provided currencies.
        The exchange rate is rounded to 2 decimal places. Handles both ISO 8601 
        timestamps with and without a trailing 'Z' (UTC indicator).

        Args:
            from_currency (str): The currency code to convert from (e.g., 'USD').
            to_currency (str): The currency code to convert to (e.g., 'EUR').
            endpoint (str): The API endpoint to use (default: 'latest').

        Returns:
            tuple: A tuple containing:
                - float: The exchange rate, rounded to two decimal places.
                - str: The date the exchange rate was last updated, in 'YYYY-MM-DD' format.

        Raises:
            ValueError: If the exchange rate cannot be retrieved or if the API request fails.
        """
        # Validate the currency codes before proceeding
        if not self.validate_currency_code(from_currency):
            raise ValueError(f"Invalid currency code: {from_currency}")
        if not self.validate_currency_code(to_currency):
            raise ValueError(f"Invalid currency code: {to_currency}")

        # Prepare the API request
        url = f'{self.base_url}'
        querystring = {
            'base_currency': from_currency,
            'currencies': to_currency,
            'apikey': self.apikey,
        }

        # Make the API request
        response = requests.get(url, params=querystring)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Print the full API response for debugging
            print('********************************')
            print(response.json())  # Add this line to debug the full response
            print('********************************')
            
            data = response.json()

            # Validate the response structure
            if 'data' in data and data['data'].get(to_currency):
                exchange_info = data['data'][to_currency]

                # Make sure exchange_info is valid and contains the necessary fields
                if 'value' in exchange_info:
                    exchange_rate = exchange_info['value']
                else:
                    raise ValueError(f"Exchange rate data is missing for {to_currency}")

                # Check if last_updated_at exists and is valid
                last_updated_at = exchange_info.get('last_updated_at')
                if last_updated_at and isinstance(last_updated_at, str):
                    if last_updated_at.endswith("Z"):
                        as_of_date = datetime.strptime(last_updated_at, '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d')
                    else:
                        as_of_date = datetime.fromisoformat(last_updated_at).strftime('%Y-%m-%d')
                else:
                    # Fallback to current date if last_updated_at is missing or invalid
                    as_of_date = datetime.now().strftime('%Y-%m-%d')

                # Return the exchange rate and the last updated date
                return exchange_rate, as_of_date

            else:
                raise ValueError(f"Could not find exchange rate data for {from_currency} to {to_currency}. Full data: {data}")
        else:
            raise ValueError(f"API request failed with status code: {response.status_code}")




    def convert_currency(self, amount: float, from_currency: str, to_currency: str) -> tuple:
        """
        Converts the specified amount from one currency to another using the latest exchange rate.

        Fetches the exchange rate between the provided currencies and multiplies the amount
        by the exchange rate. The result is rounded to 2 decimal places.

        Args:
            amount (float): The amount of money to convert.
            from_currency (str): The currency to convert from (e.g., 'USD').
            to_currency (str): The currency to convert to (e.g., 'EUR').

        Returns:
            tuple: A tuple containing:
                - float: The converted amount in the target currency, rounded to two decimal places.
                - str: The date the exchange rate was last updated.

        Raises:
            ValueError: If the exchange rate cannot be retrieved or if the currency codes are invalid.
        """
        exchange_rate, as_of_date = self.get_exchange_rate(from_currency, to_currency)
        converted_amount = amount * exchange_rate
        return converted_amount, as_of_date





