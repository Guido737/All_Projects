"""
Cryptocurrency Filter
Created by: Creator/Eversor
Date: 30 Dec 2024
"""

import requests
import time


def get_data():
    """
    Function: get_data
    Params: url(api)
    Brief: Fetch cryptocurrency data
    """
    url = "https://api.coincap.io/v2/assets"
    params = {"limit": 20}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        try:
            datas = response.json()
        except ValueError as e:
            print(f"Error parsing JSON response: {e}")
            return None
        
        if response.status_code == 200:
            return datas['data']
        else:
            print(f"Unexpected status code: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Request exception occurred: {e}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except requests.exceptions.Timeout as e:
        print(f"Timeout error occurred: {e}")
    except requests.exceptions.TooManyRedirects as e:
        print(f"Too many redirects occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while fetching data: {e}")
    
    return None

def filter_name(datas, name):
    """
    Function: filter_name
    Params: datas (list), name (str)
    Brief: Filter cryptocurrencies by name
    """
    try:
        if not datas:
            print("No data available to filter by name.")
            return []
        
        filtered_data = [i for i in datas if name.lower() in i.get("name", "").lower()]
        
        if not filtered_data:
            print(f"No cryptocurrencies found with name containing '{name}'.")
        return filtered_data
    
    except TypeError as e:
        print(f"Error with data type: {e}")
    except KeyError as e:
        print(f"KeyError: Missing expected key in data - {e}")
    except Exception as e:
        print(f"Unexpected error occurred while filtering by name: {e}")
    return []

def filter_value(datas, value):
    """
    Function: filter_value
    Params: datas (list), value (float)
    Brief: Filter cryptocurrencies by price
    """
    try:
        if not datas:
            print("No data available to filter by value.")
            return []
        
        filtered_data = [i for i in datas if float(i.get("priceUsd", 0)) > value]
        
        if not filtered_data:
            print(f"No cryptocurrencies found with price greater than {value}.")
        return filtered_data
    
    except ValueError as e:
        print(f"ValueError: Unable to convert priceUsd to float - {e}")
    except KeyError as e:
        print(f"KeyError: Missing expected key in data - {e}")
    except TypeError as e:
        print(f"TypeError: Error with data type - {e}")
    except Exception as e:
        print(f"Unexpected error occurred while filtering by value: {e}")
    return []

def output_data(datas):
    """
    Function: output_data
    Params: datas (list)
    Brief: Display cryptocurrency data
    """
    try:
        if not datas:
            print("No data available to output.")
            return
        
        for data in datas:
            name = data.get('name', 'N/A')
            symbol = data.get('symbol', 'N/A')
            price = data.get('priceUsd', 'N/A')
            market_cap = data.get('marketCapUsd', 'N/A')
            volume = data.get('volumeUsd24Hr', 'N/A')
            change_percent = data.get('changePercent24Hr', 'N/A')

            print(f"Name: {name}")
            print(f"Symbol: {symbol}")
            print(f"Current Price: ${price}")
            print(f"Market Cap: ${market_cap}")
            print(f"Total Volume: ${volume}")
            print(f"Price Change (24h): {change_percent}%")
            print("------------------------------------")
    
    except KeyError as e:
        print(f"KeyError: Missing expected key in data - {e}")
    except TypeError as e:
        print(f"TypeError: Error with data type - {e}")
    except Exception as e:
        print(f"Unexpected error occurred while displaying data: {e}")


def get_filter_choice():
    """
    Function: get_filter_choice
    Params: Take user choice
    Brief: Prompt user for filter choice
    """
    try:
        print("Select filter options:")
        print("1. Filter by name")
        print("2. Filter by value (price > XXX)")
        print("3. No filter, show all")
        choice = input("Enter your choice (1, 2, or 3): ")
        if choice not in ['1', '2', '3']:
            print("Invalid choice entered.")
            return None
        return choice
    except Exception as e:
        print(f"Unexpected error while getting filter choice: {e}")
    return None

def handle_filter_choice(choice, datas):
    """
    Function: handle_filter_choice
    Params: choice (str), datas (list)
    Brief: Handle user's filter choice and display data
    """
    try:
        if choice == "1":
            name = input("Enter the name of the cryptocurrency to search for (e.g., Bitcoin): ")
            if name:
                try:
                    data = filter_name(datas, name)
                    output_data(data)
                except KeyError:
                    print(f"No data found for cryptocurrency with name: {name}")
                except TypeError:
                    print("Error while processing the name filter. Please check the input data format.")
                except Exception as e:
                    print(f"Unexpected error while filtering by name: {e}")
            else:
                print("No name entered. Showing all data.")
                output_data(datas)

        elif choice == "2":
            value = input("Enter the price value to filter by (e.g., 1000): ")
            try:
                if value.isdigit():
                    data = filter_value(datas, float(value))
                    output_data(data)
                else:
                    print(f"Invalid value entered: {value}. Please enter a numeric value.")
            except ValueError:
                print(f"Error: The entered value '{value}' is not a valid number.")
            except Exception as e:
                print(f"Unexpected error while filtering by value: {e}")

        elif choice == "3":
            output_data(datas)

        else:
            print("Invalid choice! Please enter 1, 2, or 3.")

    except KeyboardInterrupt:
        print("\nOperation interrupted by the user.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")
    except TypeError:
        print("A type error occurred. Please check your input data.")
    except Exception as e:
        print(f"Unexpected error while handling filter choice: {e}")


def main():
    """
    Function: main
    Brief: Main loop to drive the program
    """
    while True:
        try:
            try:
                datas = get_data()
                if not datas:
                    print("No data received. Retrying...")
                    time.sleep(5)
                    continue 
            except requests.exceptions.RequestException as e:
                print(f"Network error while fetching data: {e}")
                time.sleep(5)
                continue
            except Exception as e:
                print(f"Unexpected error while fetching data: {e}")
                time.sleep(5)
                continue

            try:
                choice = get_filter_choice()
                if choice:
                    handle_filter_choice(choice, datas)
                else:
                    print("Invalid filter choice. Skipping this iteration.")
            except ValueError as e:
                print(f"Invalid filter choice format: {e}")
            except TypeError as e:
                print(f"Error while handling filter choice: {e}")
            except Exception as e:
                print(f"Unexpected error while handling filter choice: {e}")
            time.sleep(5)

        except KeyboardInterrupt:
            print("\nOperation interrupted by the user.")
            break

        except Exception as e:
            print(f"Unexpected error in main loop: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()