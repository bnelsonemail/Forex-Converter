import unittest
from app import app 

class FlaskAppTests(unittest.TestCase):
    
    def setUp(self):
        # Create a test client for the Flask app
        self.app = app.test_client()
        self.app.testing = True #Enable testing mode (disables error catching)
        
    def test_home(self):
        """ Test if the home route loads correctly."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200) # Expecting HTTP 200 ok
        self.assertIn(b'Currency Converter', response.data) # Check if 'Currency Conversion Form' is in the HTML response
        
    def test_table(self):
        """Test if the table route loads corrects"""
        response = self.app.get('/table')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Currency Table', response.data)
        
    def test_invalid_convert(self):
        """Test that the /convert route redirects if no data is in the session."""
        response = self.app.get('/convert', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Convert', response.data) # Check redirection back to the home form
        
if __name__ == '__main__':
    unittest.main()
        
    

