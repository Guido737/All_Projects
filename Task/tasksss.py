"""
Task
Created by: Creator/Eversor
Date: 30 Dec 2024
"""

import os

def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def display_tasks(task_dict):
    """
    Function: display_tasks
    Params: task_dict (dict)
    Brief: Display tasks grouped by their status.
    """
    for status, tasks in task_dict.items():
        print(f"{status}: {', '.join(tasks) if tasks else 'No tasks'}")

def display_menu():
    """
    Function: display_menu
    Params: None
    Brief: Show menu options.
    """
    print("\nWhat task do you want to see?")
    print("1. TO DO")
    print("2. IN PROGRESS")
    print("3. REVIEW")
    print("4. DONE")
    print("5. ALL")

def get_task_choice():
    """
    Function: get_task_choice
    Params: None
    Brief: Get user choice for tasks.
    """
    while True:
        choice = input("Choose a number (1-5): ")
        if choice in ["1", "2", "3", "4", "5"]:
            return choice
        print("Invalid choice. Please choose a number from 1 to 5.")

def display_task_list(choice, task_dict):
    """
    Function: display_task_list
    Params: choice (str), task_dict (dict)
    Brief: Display tasks based on choice.
    """
    print("\n" + "-"*50)
    status_map = {
        "1": "TO DO",
        "2": "IN PROGRESS",
        "3": "REVIEW",
        "4": "DONE",
        "5": None 
    }

    status = status_map.get(choice)
    if status:
        display_tasks({status: task_dict[status]})
    else:
        for status in ["TO DO", "IN PROGRESS", "REVIEW", "DONE"]:
            display_tasks({status: task_dict[status]})

    print("-"*50)

def get_task_to_deal(task_dict):
    """
    Function: get_task_to_deal
    Params: task_dict (dict)
    Brief: Ask user for task to move.
    """
    all_tasks = {task: status for status in task_dict for task in task_dict[status]}
    while True:
        task_to_deal = input("\nWhich task do you want to deal with? ").strip()
        if not task_to_deal:
            print("You didn't enter a task. Please try again.")
            continue
        if task_to_deal in all_tasks:
            return task_to_deal
        else:
            print(f"Task '{task_to_deal}' not found. Available tasks are: {', '.join(all_tasks.keys())}.")

def get_move_choice():
    """
    Function: get_move_choice
    Params: None
    Brief: Get move choice from user.
    """
    print("\nWhere to move?")
    print("1. TO DO")
    print("2. IN PROGRESS")
    print("3. REVIEW")
    print("4. DONE")

    return input("Choose a number (1-4): ")

def move_task_and_save(task_dict, task_to_deal, new_status, filename):
    """
    Function: move_task_and_save
    Params: task_dict (dict), task_to_deal (str), new_status (str), filename (str)
    Brief: Move task and save to file.
    """
    task_dict = move_task(task_dict, task_to_deal, new_status)
    print(f"\nTask '{task_to_deal}' has been moved to {new_status}.")
    save_to_file(task_dict, filename)
    print(f"\nChanges saved to {filename}.")

def should_continue():
    """
    Function: should_continue
    Params: None
    Brief: Ask user to continue or stop.
    """
    cont = input("\nDo you want to continue? (y/n): ").strip().lower()
    return cont == "y"

def move_task(task_dict, task_name, new_status):
    """
    Function: move_task
    Params: task_dict (dict), task_name (str), new_status (str)
    Brief: Move a task to a new status.
    """
    for status in task_dict:
        if task_name in task_dict[status]:
            task_dict[status].remove(task_name)
            task_dict[new_status].append(task_name)
            return task_dict
    print(f"Task '{task_name}' not found in any status.")
    return task_dict

def save_to_file(task_dict, filename):
    """
    Function: save_to_file
    Params: task_dict (dict), filename (str)
    Brief: Save tasks to a text file.
    """
    try:
        with open(filename, "w") as file:
            file.write("TO DO        IN PROGRESS    REVIEW       DONE\n")
            max_length = max(len(task_dict["TO DO"]), len(task_dict["IN PROGRESS"]), len(task_dict["REVIEW"]), len(task_dict["DONE"]))

            for i in range(max_length):
                line = ""
                for status in ["TO DO", "IN PROGRESS", "REVIEW", "DONE"]:
                    task = task_dict[status][i] if i < len(task_dict[status]) else ""
                    line += f"{task:<12}" if task else " " * 12
                file.write(line.rstrip() + "\n")
        print(f"\nChanges saved to {filename}.")

    except FileNotFoundError:
        print(f"Error: The file path '{filename}' does not exist.")
    except PermissionError:
        print(f"Error: Permission denied. You do not have the required permissions to write to '{filename}'.")
    except Exception as e:
        print(f"An unexpected error occurred while saving the file: {e}")

def main():
    """
    Function: main
    Params: None
    Brief: Run task management program.
    """
    filename = "/home/usernamezero00/Desktop/myprojects/Task/task.txt"
    task_dict = {
        "TO DO": ["task 2", "task 4", "task 5"],
        "IN PROGRESS": ["task 1", "task 6"],
        "REVIEW": ["task 3"],
        "DONE": []
    }

    while True:
        clear_screen()
        display_menu()
        choice = get_task_choice()
        if choice not in ["1", "2", "3", "4", "5"]:
            print("Invalid choice. Please choose a number from 1 to 5.")
            continue

        clear_screen()
        display_task_list(choice, task_dict)
        task_to_deal = get_task_to_deal(task_dict)
        if not task_to_deal:
            continue
        clear_screen()
        move_choice = get_move_choice()
        if move_choice not in ["1", "2", "3", "4"]:
            print("Invalid choice. Task not moved.")
            continue
        clear_screen()
        new_status = ["TO DO", "IN PROGRESS", "REVIEW", "DONE"][int(move_choice) - 1]
        move_task_and_save(task_dict, task_to_deal, new_status, filename)
        if not should_continue():
            print("\nEnding.....\n\nGoodbye!")
            break
        
if __name__ == "__main__":
    main()
