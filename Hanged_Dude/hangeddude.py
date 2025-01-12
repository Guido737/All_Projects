"""
Hangman Game
Created by: Creator/Eversor
Date: 30 Dec 2024
"""

import requests
import os
import random

BASE_URL = "https://random-word-api.herokuapp.com/word"
PARAMS = {"number": 5}

def choose_word():
    """
    Function: choose_word
    Brief: Fetches or selects word.
    """
    try:
        response = requests.get(BASE_URL, params=PARAMS)
        if response.status_code == 200:
            try:
                words = response.json()
                if words:
                    return random.choice(words).lower()
                else:
                    raise Exception("No words found in response.")
            except (ValueError, IndexError) as e:
                raise Exception(f"Error parsing JSON response: {e}")
        else:
            raise Exception(f"Failed to fetch word: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Network error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("Using fallback word list.")
    return random.choice(["apple", "banana", "cherry", "orange", "grape"]).lower()

def display_word(word, guessed_letters):
    """
    Function: display_word
    Brief: Returns word with underscores.
    Params: word (str), guessed_letters (list)
    """
    return ''.join([letter if letter in guessed_letters else '_' for letter in word])

def draw_hangman(incorrect_guesses):
    """
    Function: draw_hangman
    Brief: Draws hangman figure.
    Params: incorrect_guesses (int)
    """
    hangman_pics = [
        '''
         ------
         |    |
              |
              |
              |
              |
              |
        =========
        ''',
        '''
         ------
         |    |
         O    |
              |
              |
              |
              |
        =========
        ''',
        '''
         ------
         |    |
         O    |
         |    |
              |
              |
              |
        =========
        ''',
        '''
         ------
         |    |
         O    |
        /|    |
              |
              |
              |
        =========
        ''',
        '''
         ------
         |    |
         O    |
        /|\\   |
              |
              |
              |
        =========
        ''',
        '''
         ------
         |    |
         O    |
        /|\\   |
        /     |
              |
              |
        =========
        ''',
        '''
         ------
         |    |
         O    |
        /|\\   |
        / \\   |
              |
              |
        =========
        '''
    ]
    print(hangman_pics[incorrect_guesses])

def get_guess(guessed_letters):
    """
    Function: get_guess
    Brief: Prompts for letter.
    Params: guessed_letters (list)
    """
    guess = input("Enter a letter: ").lower()
    if len(guess) != 1 or not guess.isalpha() or guess in guessed_letters:
        print("Invalid guess.")
        input("Press Enter...")
        return None
    return guess

def update_guesses(guess, word, guessed_letters, incorrect_guesses):
    """
    Function: update_guesses
    Brief: Updates guesses and incorrect count.
    Params: guess (str), word (str), guessed_letters (list), incorrect_guesses (int)
    """
    if guess in word:
        print(f"Correct! '{guess}' is in the word.")
    else:
        incorrect_guesses += 1
        print(f"Incorrect! '{guess}' is not in the word.")
    guessed_letters.append(guess)
    return incorrect_guesses

def check_win(word, guessed_letters):
    """
    Function: check_win
    Brief: Checks if word is guessed.
    Params: word (str), guessed_letters (list)
    """
    return display_word(word, guessed_letters) == word

def handle_game_over(incorrect_guesses, max_incorrect_guesses, word):
    """
    Function: handle_game_over
    Brief: Handles end of game.
    Params: incorrect_guesses (int), max_incorrect_guesses (int), word (str)
    """
    if incorrect_guesses == max_incorrect_guesses:
        os.system('cls' if os.name == 'nt' else 'clear')
        draw_hangman(incorrect_guesses)
        print(f"Out of guesses. The word was: {word}")

def setup_game():
    """
    Function: setup_game
    Brief: Initializes game.
    Params: None
    """
    word = choose_word()
    if not word:
        print("Game cannot proceed. Exiting.")
        exit()
    return word, [], 0, 6

def game_loop(word, guessed_letters, incorrect_guesses, max_incorrect_guesses):
    """
    Function: game_loop
    Brief: Main game loop.
    Params: word (str), guessed_letters (list), incorrect_guesses (int), max_incorrect_guesses (int)
    """
    while incorrect_guesses < max_incorrect_guesses:
        os.system('cls' if os.name == 'nt' else 'clear')
        draw_hangman(incorrect_guesses)
        print(f"Word: {display_word(word, guessed_letters)}")
        guess = get_guess(guessed_letters)
        if not guess:
            continue
        incorrect_guesses = update_guesses(guess, word, guessed_letters, incorrect_guesses)
        if check_win(word, guessed_letters):
            print(f"Congratulations! You guessed the word: {word}")
            break
        input("Press Enter to continue...")
    return incorrect_guesses

def play_hangman():
    """
    Function: play_hangman
    Brief: Starts game.
    Params: None
    """
    word, guessed_letters, incorrect_guesses, max_incorrect_guesses = setup_game()
    incorrect_guesses = game_loop(word, guessed_letters, incorrect_guesses, max_incorrect_guesses)
    handle_game_over(incorrect_guesses, max_incorrect_guesses, word)

if __name__ == "__main__":
    play_hangman()
