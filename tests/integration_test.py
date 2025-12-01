import unittest
import sys
import os

# Add the project root to import paths
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app  # Import your Flask app instance


class TestModelAppIntegration(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_model_app_integration(self):
        # Valid test input that should work with the trained model
        form_data = {
            'temperature': '275.15',
            'pressure': '1013',
            'humidity': '85',
            'wind_speed': '3.6',
            'wind_deg': '180',
            'rain_1h': '0',
            'rain_3h': '0',
            'snow': '0',
            'clouds': '20'
        }

        response = self.client.post('/', data=form_data)

        # Response should be 200 OK
        self.assertEqual(response.status_code, 200)

        html_text = response.data.decode('utf-8').lower()

        valid_classes = [
            'clear', 'cloudy', 'drizzly', 'foggy', 'hazy',
            'misty', 'rainy', 'smokey', 'thunderstorm'
        ]

        # True if ANY valid weather class appears
        found = any(weather in html_text for weather in valid_classes)

        self.assertTrue(found, "No valid weather class found in HTML output")


if __name__ == '__main__':
    unittest.main()

