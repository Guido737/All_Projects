"""
Word Frequency Count
Created by: Creator/Eversor
Date: 30 Dec 2024
"""

import string
from collections import Counter
import os 

def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

stop_words = set([
    'он', 'бою', 'на', 'всегда', 'в', 'для', 'о', 'по', 'это', 'или', 'быть', 'забыл', 'добавить', 'подсказку', 
    'потому', 'что', 'опилки', 'вместо', 'мозгов', 'не'
])

def clean_text(text):
    """
    Function: clean_text
    Params: text (str)
    Brief: Remove punctuation and convert text to lowercase.
    """
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)
    return text.lower()

def read_file(file_path):
    """
    Function: read_file
    Params: file_path (str)
    Brief: Read file contents.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    return text

def filter_words(text, stop_words):
    """
    Function: filter_words
    Params: text (str), stop_words (set)
    Brief: Remove stop words, non-alphabetic words, and short words.
    """
    words = text.split()
    filtered_words = [word.lower() for word in words 
                      if len(word) > 1 and word.lower() not in stop_words and word.isalpha()]
    
    return filtered_words

def count_word_frequencies(filtered_words):
    """
    Function: count_word_frequencies
    Params: filtered_words (list)
    Brief: Count word frequencies using Counter.
    """
    word_counts = Counter(filtered_words)
    return word_counts

def print_most_common_words(word_counts, top_n=5):
    """
    Function: print_most_common_words
    Params: word_counts (Counter), top_n (int)
    Brief: Print top N most common words.
    """
    most_common_words = word_counts.most_common(top_n)
    print(f"Top {top_n} catchwords:")
    for word, count in most_common_words:
        print(f"{word}: {count}")

def main(file_path, top_n=5):
    """
    Function: main
    Params: file_path (str), top_n (int)
    Brief: Main function to process the file and print common words.
    """
    text = read_file(file_path)
    if text:
        clear_screen()
        cleaned_text = clean_text(text)
        filtered_words = filter_words(cleaned_text, stop_words)
        word_counts = count_word_frequencies(filtered_words)
        print_most_common_words(word_counts, top_n)

    
file_path = '/home/usernamezero00/Desktop/myprojects/All_Projects/Word_Frequency/newfile.txt' 
main(file_path, top_n=5)
