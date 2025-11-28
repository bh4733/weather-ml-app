import unittest
from app import app  # Import your Flask app instance


class TestModelAppIntegration(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        
    def test_model_app_integration(self):
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

        # Page loads successfully
        self.assertEqual(response.status_code, 200)

        html_text = response.data.decode('utf-8').lower()

        # Prediction must appear
        self.assertIn("prediction", html_text)

        # Prediction time must appear
        self.assertIn("time", html_text)

        valid_classes = [
            'clear', 'cloudy', 'drizzly', 'foggy', 'hazey',
            'misty', 'rainy', 'smokey', 'thunderstorm'
        ]
        found = any(weather in html_text for weather in valid_classes)

        # Classification must be within valid classes
        self.assertTrue(found, "Prediction did not match any expected classes")


if __name__ == '__main__':
    unittest.main()

