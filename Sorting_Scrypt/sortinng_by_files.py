"""
File Sorter
Created by: Creator/Eversor
Date: 30 Dec 2024
"""

import os
import shutil
import argparse

FILE_CATEGORIES = {
    'docs': ['.doc', '.docx', '.txt', '.rtf'],
    'pdf': ['.pdf'],
    'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
    'videos': ['.mp4', '.mkv', '.avi', '.mov', '.flv'],
    'audio': ['.mp3', '.wav', '.aac', '.flac'],
    'spreadsheets': ['.xls', '.xlsx', '.csv'],
    'presentations': ['.ppt', '.pptx'],
    'archives': ['.zip', '.tar', '.tar.gz', '.rar', '.7z'],
}

def create_extension_directory(source_dir, category, extension):
    """
    Function: create_extension_directory
    Params: source_dir (str), category (str), extension (str)
    Brief: Creates a directory for each file extension within its category.
    """
    extension_dir = os.path.join(source_dir, category, extension.lstrip('.'))
    if not os.path.exists(extension_dir):
        try:
            os.makedirs(extension_dir)
            print(f'Created directory {extension_dir}')
        except OSError as e:
            print(f'Error creating directory "{extension_dir}": {e}')
            return None
    return extension_dir

def move_file(file, category_dir, extension):
    """
    Function: move_file
    Params: file (str), category_dir (str), extension (str)
    Brief: Moves the file to its corresponding extension directory.
    """
    try:
        destination = os.path.join(category_dir, extension.lstrip('.'), os.path.basename(file))
        shutil.move(file, destination)
        print(f"Moved: {file} -> {destination}")
    except Exception as e:
        print(f'Error moving file "{file}": {e}')

def create_others_directory(source_dir):
    """
    Function: create_others_directory
    Params: source_dir (str)
    Brief: Creates 'others' directory for unmatched files.
    """
    others_dir = os.path.join(source_dir, "others")
    if not os.path.exists(others_dir):
        try:
            os.makedirs(others_dir)
            print(f'Created directory {others_dir}')
        except OSError as e:
            print(f'Error creating directory "{others_dir}": {e}')
            return None
    return others_dir

def get_file_extension(filename):
    """
    Function: get_file_extension
    Params: filename (str)
    Brief: Returns the file extension (e.g., '.txt').
    """
    return os.path.splitext(filename)[1].lower()

def get_category_for_extension(file_extension):
    """
    Function: get_category_for_extension
    Params: file_extension (str)
    Brief: Returns category for the file based on its extension.
    """
    for category, extensions in FILE_CATEGORIES.items():
        if file_extension in extensions:
            return category
    return None

def sort_and_move_file(file_path, source_dir, others_dir):
    """
    Function: sort_and_move_file
    Params: file_path (str), source_dir (str), others_dir (str)
    Brief: Sorts and moves the file to the correct directory.
    """
    file_extension = get_file_extension(file_path)
    category = get_category_for_extension(file_extension)

    if category:
        category_dir = os.path.join(source_dir, category)
        if not os.path.exists(category_dir):
            os.makedirs(category_dir)
        extension_dir = create_extension_directory(source_dir, category, file_extension)
        if extension_dir:
            move_file(file_path, category_dir, file_extension)
    else:
        move_file(file_path, others_dir)

def sort_files(source_dir):
    """
    Function: sort_files
    Params: source_dir (str)
    Brief: Sorts files into category directories based on their extension.
    """
    if not os.listdir(source_dir):
        print("The source directory is empty.")
        return
    
    others_dir = create_others_directory(source_dir)
    if not others_dir:
        return

    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)
        if not os.path.isfile(file_path) or filename.startswith("."):
            continue
        sort_and_move_file(file_path, source_dir, others_dir)

def get_arguments():
    """
    Function: get_arguments
    Brief: Parses and returns the source directory argument.
    """
    parser = argparse.ArgumentParser(description="Sort files by type.")
    parser.add_argument("source_dir", help="Source directory to sort.")
    args = parser.parse_args()
    return args.source_dir

def main():
    """
    Function: main
    Brief: Main entry point. Starts the file sorting process.
    """
    source_dir = get_arguments()
    if not os.path.isdir(source_dir):
        print(f"Error: The source directory '{source_dir}' does not exist.")
        return
    sort_files(source_dir)
    print("Files have been sorted.")

if __name__ == '__main__':
    main()