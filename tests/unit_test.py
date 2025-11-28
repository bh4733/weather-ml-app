import unittest
from app import app, classify_weather, load_model
import numpy as np
from unittest.mock import patch


class TestWeatherApp(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_post_missing_field(self):
        """Test that sending a form without all required fields returns an error (not 200)."""
        form_data = {
            'temperature': '270.277',
            'pressure': '1006',
            'humidity': '84',
            # 'wind_speed' intentionally missing
            'wind_deg': '274',
            'rain_1h': '0',
            'rain_3h': '0',
            'snow': '0',
            'clouds': '9'
        }
        response = self.client.post('/', data=form_data)

        # Most apps return 400 Bad Request when a required field is missing
        self.assertIn(response.status_code, [400, 422])

        # Optionally check that the response contains an error message
        self.assertIn(b"missing", response.data.lower())   # adjust according to your actual error message

    def test_model_can_be_loaded(self):
        """Ensure the model loads without raising an exception."""
        model = load_model()
        self.assertIsNotNone(model)

    @patch('app.load_model')  # <- mock the model so the test runs even if the file is missing
    def test_clear_classification_output(self, mock_load_model):
        """Test that a clear-sky example is classified as 'clear'."""
        dummy_model = mock_load_model.return_value
        # Assuming your classify_weather does something like model.predict(...)
        dummy_model.predict.return_value = np.array([[1.0, 0.0, 0.0]])  # example: first class is clear

        test_input = np.array([269.686, 1002, 78, 0, 23, 0, 0, 0, 0]).reshape(1, -1)
        class_result, _ = classify_weather(test_input)
        self.assertEqual(class_result.lower(), "clear")

    @patch('app.load_model')
    def test_rainy_classification_output(self, mock_load_model):
        """Test that a rainy example is classified as 'rainy'."""
        dummy_model = mock_load_model.return_value
        dummy_model.predict.return_value = np.array([[0.0, 1.0, 0.0]])  # second class = rainy

        test_input = np.array([279.626, 998, 99, 1, 314, 0.3, 0, 0, 88]).reshape(1, -1)
        class_result, _ = classify_weather(test_input)
        self.assertEqual(class_result.lower(), "rainy")

    @patch('app.load_model')
    def test_foggy_classification_output(self, mock_load_model):
        """Test that a foggy example is classified as 'foggy'."""
        dummy_model = mock_load_model.return_value
        dummy_model.predict.return_value = np.array([[0.0, 0.0, 1.0]])  # third class = foggy

        test_input = np.array([289.47, 1015, 88, 2, 300, 0, 0, 0, 20]).reshape(1, -1)
        class_result, _ = classify_weather(test_input)
        self.assertEqual(class_result.lower(), "foggy")


if __name__ == '__main__':
    unittest.main(verbosity=2)
