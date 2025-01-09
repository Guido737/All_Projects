"""
Get Weather By API
Created by: Creator/Eversor
Date: 30 Dec 2024
"""

import requests
import argparse

API_KEY = '40e151f43a8da63402abb3c21eaeabbb'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'
AVAILABLE_OPTIONS = {
    'temperature': 'Temperature (in Celsius)',
    'humidity': 'Humidity (%)',
    'wind_speed': 'Wind Speed (m/s)',
}

def fetch_weather_data(city):
    """
    Function: Fetch data
    Params: city (str) - City name
    Brief: Fetch weather from API
    """
    try:
        url = f'{BASE_URL}?q={city}&appid={API_KEY}&units=metric'
        response = requests.get(url)
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None

def display_weather_conditions(weather, wind, option):
    """
    Function: Display conditions
    Params: weather (dict), wind (dict), option (str)
    Brief: Display selected weather
    """
    try:
        if option == 'temperature':
            print(f"Temperature: {weather.get('temp', 'N/A')} °C")
        elif option == 'humidity':
            print(f"Humidity: {weather.get('humidity', 'N/A')} %")
        elif option == 'wind_speed':
            print(f"Wind Speed: {wind.get('speed', 'N/A')} m/s")
        else:
            print("Invalid option selected. Choose 'temperature', 'humidity', or 'wind_speed'.")
    
    except KeyError as e:
        print(f"KeyError: Missing expected data for {e}")
    except Exception as e:
        print(f"Error displaying weather: {e}")

def display_weather(data, option):
    """
    Function: Process data
    Params: data (dict), option (str)
    Brief: Process and display data
    """
    try:
        if not data:
            print("Error: No data received.")
            return
        weather = data.get('main', {})
        wind = data.get('wind', {})
        if not weather or not wind:
            print("Error: Weather or wind data is missing.")
            return
        display_weather_conditions(weather, wind, option)
    
    except KeyError as e:
        print(f"KeyError: Missing expected key {e}")
    except TypeError as e:
        print(f"TypeError: Incorrect data format encountered. {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def get_arguments():
    """
    Function: Parse args
    Brief: Parse command-line arguments
    """
    try:
        parser = argparse.ArgumentParser(description="Fetch and display weather data.")
        parser.add_argument("city", type=str, help="The city to fetch weather for.")
        parser.add_argument("option", choices=AVAILABLE_OPTIONS.keys(), help="The weather parameter to display.")
        return parser.parse_args()
    
    except argparse.ArgumentTypeError as e:
        print(f"Argument type error: {e}. Please check the input types.")
    except argparse.ArgumentError as e:
        print(f"Argument error: {e}. Please ensure all arguments are correctly specified.")
    except Exception as e:
        print(f"Unexpected error during argument parsing: {e}")

def main():
    """
    Function: Main entry
    Brief: Main program to fetch and display weather
    """
    try:
        args = get_arguments()
        if not args.city.strip():
            print("Error: City name cannot be empty.")
            return
        data = fetch_weather_data(args.city)
        if data:
            display_weather(data, args.option)
        else:
            print("Failed to retrieve weather data.")
    except requests.exceptions.RequestException as e:
        print(f"Error with the API request: {e}. Please check your internet connection or try again later.")
    except ValueError as e:
        print(f"Value error occurred: {e}. Please verify the input data.")
    except KeyError as e:
        print(f"Missing expected data: {e}. Ensure the response contains all required fields.")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")

if __name__ == '__main__':
    main()