"""
Joke Fetcher and Rater
Created by: Creator/Eversor
Date: 30 Dec 2024
"""

import requests
import random
import time

def fetch_joke(url):
    """
    Function: fetch_joke
    Params: url (str)
    Brief: Fetches a single joke from the given URL and returns it in JSON format.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request exception occurred: {e}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except requests.exceptions.Timeout as e:
        print(f"Timeout error occurred: {e}")
    except requests.exceptions.TooManyRedirects as e:
        print(f"Too many redirects occurred: {e}")
    except ValueError as e:
        print(f"Error parsing JSON response: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None

def get_jokes(url, num_jokes=10):
    """
    Function: get_jokes
    Params: url (str), num_jokes (int)
    Brief: Fetches a list of jokes from the API by calling fetch_joke multiple times.
    """
    jokes = []
    for i in range(num_jokes):
        try:
            joke_data = fetch_joke(url)
            if joke_data:
                joke = joke_data.get('setup') + " " + joke_data.get('punchline')
                if joke:
                    jokes.append(joke)
            else:
                print(f"Failed to retrieve joke {i+1}. Skipping...")
        except Exception as e:
            print(f"Error during joke fetch operation {i+1}: {e}")
        time.sleep(1)
    return jokes

def rate_jokes(jokes):
    """
    Function: rate_jokes
    Params: jokes (list)
    Brief: Rates each joke randomly on a scale from 1 to 10.
    """
    try:
        if not jokes:
            raise ValueError("The joke list is empty. Cannot rate jokes.")
        
        ratings = random.sample(range(1, 11), len(jokes))
        rated_jokes = []
        for joke, rating in zip(jokes, ratings):
            rated_jokes.append({"joke": joke, "rating": rating})
        return rated_jokes
    except ValueError as e:
        print(f"Error: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error occurred while rating jokes: {e}")
        return []

def save_jokes_to_file(rated_jokes, filename='top_jokes.txt'):
    """
    Function: save_jokes_to_file
    Params: rated_jokes (list), filename (str)
    Brief: Saves the rated jokes to a text file, sorted by rating in descending order.
    """
    try:
        if not rated_jokes:
            raise ValueError("No rated jokes to save.")
        
        rated_jokes.sort(key=lambda x: x['rating'], reverse=True)
        with open(filename, 'w', encoding='utf-8') as f:
            for joke in rated_jokes:
                f.write(f"Joke: {joke['joke']}\nRating: {joke['rating']}\n")
        print(f"Jokes have been rated and saved in {filename}.")
    except ValueError as e:
        print(f"Error: {e}")
    except IOError as e:
        print(f"File I/O error occurred: {e}")
    except Exception as e:
        print(f"Unexpected error occurred while saving jokes: {e}")

def main():
    """
    Function: main
    Brief: The main function that coordinates fetching, rating, and saving the jokes.
    """
    url = "https://official-joke-api.appspot.com/random_joke"
    filename = "top_jokes.txt"
    try:
        jokes = get_jokes(url, num_jokes=10)
        if jokes:
            rated_jokes = rate_jokes(jokes)
            if rated_jokes:
                save_jokes_to_file(rated_jokes, filename)
            else:
                print("No jokes to rate.")
        else:
            print("No jokes fetched.")
    except Exception as e:
        print(f"Unexpected error in the main function: {e}")

if __name__ == "__main__":
    main()