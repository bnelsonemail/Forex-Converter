import unittest
from unittest.mock import patch, Mock
from forex_converter import CurrencyConverter

class CurrencyConverterTests(unittest.TestCase):
    
    def setUp(self):
        self.converter = CurrencyConverter()
        
    @patch('forex_converter.requests.get')
    def test_get_exchange_rate(self, mock_get):
        """Test fetching exchange rate for balid currency codes."""
        
        # Create a mock response object with sample exchange rate data
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'info': {'quotes': 1.2},
            'date': '2023-01-01'
        }
        
        # Mock the requests.get call to return the mock response
        mock_get.return_value = mock_response
        
        # Call the method being tested
        exchange_rate, as_of_date = self.converter.get_exchange_rate('USD', 'EUR')
        
        # Assert that the exchange rate and date were returned correctly
        self.assertEqual(exchange_rate, 1.2)
        self.assertEqual(as_of_date, '2023-01-01')
    
    def test_validate_currency_code(self):
        """Test validating a valid and invalid currency code."""
        self.assertTrue(self.converter.validate_currency_code('USD'))  # USD should be valid
        self.assertFalse(self.converter.validate_currency_code('XXX'))  # XXX should be invalid
    
    @patch('forex_converter.CurrencyConverter.get_exchange_rate')
    def test_convert_currency(self, mock_get_exchange_rate):
        """Test converting an amount of money from one currency to another."""
        
        # Mock the get_exchange_rate method to return a fake exchange rate
        mock_get_exchange_rate.return_value = (1.5, '2023-01-01')
        
        # Call the method being tested
        converted_amount, as_of_date = self.converter.convert_currency(100, 'USD', 'EUR')
        
        # Assert that the conversion was done correctly
        self.assertEqual(converted_amount, 150)  # 100 * 1.5 = 150
        self.assertEqual(as_of_date, '2023-01-01')

if __name__ == '__main__':
    unittest.main()        