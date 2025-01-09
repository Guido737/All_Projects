"""
News By API
Created by: Creator/Eversor
Date: 30 Dec 2024
"""

import requests
import time
import argparse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def build_params(api_key, query=None, category=None):
    """
    Function: build parameters
    Params: api_key (str), query (str), category (str)
    Brief: Build request parameters for API request.
    """
    try:
        params = {
            'apiKey': api_key,
            'language': 'en',
            'pageSize': 5,
            'q': query,
            'category': category
        }
        
        return {k: v for k, v in params.items() if v}
    except TypeError as e:
        logging.error(f"TypeError occurred while building parameters: {e}")
        return {}
    except Exception as e:
        logging.error(f"Unexpected error occurred while building parameters: {e}")
        return {}

def fetch_news_from_api(params):
    """
    Function: fetch news
    Params: params (dict)
    Brief: Make API request to NewsAPI and return response.
    """
    try:
        logging.info(f"Making request to NewsAPI with params: {params}")
        response = requests.get('https://newsapi.org/v2/top-headlines', params=params)
        response.raise_for_status()
        logging.info(f"Response received with status code: {response.status_code}")
        return response
    except requests.exceptions.Timeout as e:
        logging.error(f"Request timed out: {e}")
    except requests.exceptions.TooManyRedirects as e:
        logging.error(f"Too many redirects: {e}")
    except requests.exceptions.RequestException as e:
        logging.error(f"General request exception: {e}")
    except Exception as e:
        logging.error(f"Unexpected error occurred during the API request: {e}")
    return None

def handle_response(response):
    """
    Function: handle response
    Params: response (requests.Response)
    Brief: Process API response and return articles.
    """
    try:
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            logging.info(f"Successfully fetched {len(articles)} articles.")
            return articles
        else:
            logging.error(f"Failed to fetch news. Status code: {response.status_code}")
            logging.debug(f"Response content: {response.text}")
            return []
    except ValueError as e:
        logging.error(f"Error parsing JSON response: {e}")
    except KeyError as e:
        logging.error(f"KeyError: Expected key not found in response: {e}")
    except Exception as e:
        logging.error(f"Unexpected error processing response: {e}")
    return []

def retry_request(response, retries, delay):
    """
    Function: retry request
    Params: response (requests.Response), retries (int), delay (int)
    Brief: Retry failed requests on 500 server error with exponential backoff.
    """
    attempt = 0
    while response and response.status_code == 500 and attempt < retries:
        try:
            logging.warning(f"Retrying in {delay} seconds... Attempt {attempt + 1}")
            time.sleep(delay)
            delay *= 2
            response = fetch_news_from_api(response.request.params)
            attempt += 1
        except Exception as e:
            logging.error(f"Error during retrying request: {e}")
            break
    if not response or response.status_code != 200:
        logging.error("Final retry failed or returned non-200 status.")
    return response

def get_news(api_key, query=None, category=None, retries=3, delay=5):
    """
    Function: get news
    Params: api_key (str), query (str), category (str), retries (int), delay (int)
    Brief: Fetch the news articles from the NewsAPI, with retry logic.
    """
    try:
        params = build_params(api_key, query, category)
        if not params:
            logging.error("Error building request parameters. Exiting.")
            return []

        response = fetch_news_from_api(params)

        if response:
            response = retry_request(response, retries, delay)
            return handle_response(response)
        else:
            logging.error("Failed to fetch news after retries.")
            return []

    except requests.exceptions.RequestException as e:
        logging.error(f"RequestException occurred while fetching news: {e}")
    except Exception as e:
        logging.error(f"Unexpected error occurred while fetching news: {e}")
    return []

def save_to_file(news):
    """
    Function: save news
    Params: news (list)
    Brief: Save news articles to a text file.
    """
    try:
        if not news:
            raise ValueError("No news to save.")
        
        with open('news_today.txt', 'w', encoding='utf-8') as f:
            for idx, article in enumerate(news, 1):
                f.write(f"{idx}. {article['title']}\nSource: {article['source']['name']}\nPublished: {article['publishedAt']}\nLink: {article['url']}\n\n")
        logging.info("News saved to file.")
    except ValueError as e:
        logging.warning(f"Warning: {e}")
    except IOError as e:
        logging.error(f"File I/O error occurred: {e}")
    except Exception as e:
        logging.error(f"Unexpected error saving to file: {e}")

def get_arguments():
    """
    Function: get arguments
    Brief: Parse command-line arguments.
    """
    try:
        parser = argparse.ArgumentParser(description="Fetch and save the top news articles.")
        parser.add_argument("api_key", help="API key for NewsAPI")
        parser.add_argument("-q", "--query", help="Keyword to search for in the news articles", default=None)
        parser.add_argument("-c", "--category", help="Category of the news (e.g. business, technology)", default=None)
        return parser.parse_args()
    except argparse.ArgumentError as e:
        logging.error(f"Argument parsing error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error parsing arguments: {e}")
    return None

def validate_api_key(args):
    """
    Function: validate key
    Params: args (namespace)
    Brief: Validate if API key is provided.
    """
    try:
        if not args.api_key:
            logging.error("API key is required.")
            return False
        return True
    except Exception as e:
        logging.error(f"Unexpected error validating API key: {e}")
        return False

def process_news(news):
    """
    Function: process news
    Params: news (list)
    Brief: Process and print news articles to the screen.
    """
    try:
        if news:
            save_to_file(news)
            for idx, article in enumerate(news, 1):
                logging.info(f"{idx}. {article['title']}\n{article['source']['name']} - {article['publishedAt']}\n{article['url']}\n")
        else:
            logging.warning("No news found.")
    except Exception as e:
        logging.error(f"Unexpected error during news processing: {e}")

def main():
    """
    Function: main
    Brief: Orchestrate the entire process.
    """
    try:
        args = get_arguments()
        if args and validate_api_key(args):
            news = get_news(args.api_key, args.query, args.category)
            process_news(news)
        else:
            logging.error("Invalid arguments or missing API key.")
    except Exception as e:
        logging.error(f"Unexpected error in main function: {e}")

if __name__ == "__main__":
    main()