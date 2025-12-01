
import unittest
import sys
import os

# Add the project root to import paths
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from app import app

class TestAppSmoke(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()
    
    def test_prediction_route_success(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_form(self):
        response = self.client.get('/')
        html = response.data.decode("utf-8").lower()

        # Checks if the form is rendered
        self.assertIn("<form", html)
        self.assertIn("temperature", html)

if __name__ == '__main__':
    unittest.main()

