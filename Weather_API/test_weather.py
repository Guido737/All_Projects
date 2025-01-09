import unittest
from unittest.mock import patch
from io import StringIO
import requests 

from weather import fetch_weather_data, display_weather_conditions, display_weather, get_arguments

class TestWeatherScript(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    @patch('logging.basicConfig')
    def test_display_weather(self, mock_logging, mock_stdout):
        """
        Function: Testing weather display
        Params: mock_logging, mock_stdout
        Brief: Test if temperature is displayed correctly
        """
        weather_data = {
            'main': {'temp': 20, 'humidity': 80},
            'wind': {'speed': 5}
        }

        display_weather(weather_data, 'temperature')
        output = mock_stdout.getvalue()
        self.assertIn("Temperature: 20 °C", output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('logging.basicConfig')
    def test_display_weather_conditions_invalid_option(self, mock_logging, mock_stdout):
        """
        Function: Invalid option
        Params: mock_logging, mock_stdout
        Brief: Test if invalid option triggers error
        """
        weather_data = {
            'main': {'temp': 20, 'humidity': 80},
            'wind': {'speed': 5}
        }

        display_weather_conditions(weather_data['main'], weather_data['wind'], 'invalid_option')
        output = mock_stdout.getvalue()
        self.assertIn("Invalid option selected. Choose 'temperature', 'humidity', or 'wind_speed'.", output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('logging.basicConfig')
    def test_display_weather_conditions_temperature(self, mock_logging, mock_stdout):
        """
        Function: Testing temperature display
        Params: mock_logging, mock_stdout
        Brief: Test if temperature is displayed correctly
        """
        weather_data = {
            'main': {'temp': 20, 'humidity': 80},
            'wind': {'speed': 5}
        }

        display_weather_conditions(weather_data['main'], weather_data['wind'], 'temperature')
        output = mock_stdout.getvalue()
        self.assertIn("Temperature: 20 °C", output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('logging.basicConfig')
    def test_fetch_weather_data_success(self, mock_logging, mock_stdout):
        """
        Function: Mocking weather data
        Params: mock_logging, mock_stdout
        Brief: Test for successful API response
        """
        with patch('requests.get') as mock_get:
            mock_get.return_value.json.return_value = {
                'main': {'temp': 20, 'humidity': 80},
                'wind': {'speed': 5}
            }
            mock_get.return_value.status_code = 200
            data = fetch_weather_data("London")
            self.assertIsNotNone(data)
            self.assertEqual(data['main']['temp'], 20)
            self.assertEqual(data['wind']['speed'], 5)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('logging.basicConfig')
    def test_fetch_weather_data_failure(self, mock_logging, mock_stdout):
        """
        Function: Mocking failure
        Params: mock_logging, mock_stdout
        Brief: Test if failure is handled properly
        """
        with patch('requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.RequestException("Request failed")
            
            data = fetch_weather_data("London")
            self.assertIsNone(data)
            output = mock_stdout.getvalue()
            self.assertIn("Request failed: Request failed", output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('logging.basicConfig')
    def test_get_arguments(self, mock_logging, mock_stdout):
        """
        Function: Mocking arguments
        Params: mock_logging, mock_stdout
        Brief: Test for argument parsing
        """
        with patch('sys.argv', ['weather.py', 'London', 'temperature']):
            args = get_arguments()
            self.assertEqual(args.city, 'London')
            self.assertEqual(args.option, 'temperature')

if __name__ == '__main__':
    unittest.main()