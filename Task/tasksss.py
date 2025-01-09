"""
Task
Created by: Creator/Eversor
Date: 30 Dec 2024
"""

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
    return input("Choose a number (1-5): ")

def display_task_list(choice, task_dict):
    """
    Function: display_task_list
    Params: choice (str), task_dict (dict)
    Brief: Display tasks based on choice.
    """
    if choice == "1":
        display_tasks({"TO DO": task_dict["TO DO"]})
    elif choice == "2":
        display_tasks({"IN PROGRESS": task_dict["IN PROGRESS"]})
    elif choice == "3":
        display_tasks({"REVIEW": task_dict["REVIEW"]})
    elif choice == "4":
        display_tasks({"DONE": task_dict["DONE"]})
    elif choice == "5":
        display_tasks(task_dict)

def get_task_to_deal(task_dict):
    """
    Function: get_task_to_deal
    Params: task_dict (dict)
    Brief: Ask user for task to move.
    """
    task_to_deal = input("\nWhich task do you want to deal with? ")
    task_found = False
    for status in task_dict:
        if task_to_deal in task_dict[status]:
            task_found = True
            break
    if not task_found:
        print("Task not found. Please choose a valid task.")
        return None
    return task_to_deal

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
    return task_dict

def save_to_file(task_dict, filename):
    """
    Function: save_to_file
    Params: task_dict (dict), filename (str)
    Brief: Save tasks to a text file.
    """
    with open(filename, "w") as file:
        file.write("TO DO    IN PROGRESS     REVIEW      DONE\n")
        max_length = max(len(task_dict["TO DO"]), len(task_dict["IN PROGRESS"]), len(task_dict["REVIEW"]), len(task_dict["DONE"]))
        
        for i in range(max_length):
            line = ""
            for status in ["TO DO", "IN PROGRESS", "REVIEW", "DONE"]:
                task = task_dict[status][i] if i < len(task_dict[status]) else ""
                line += f"{task:<12}"
            file.write(line.rstrip() + "\n")

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
        display_menu()
        choice = get_task_choice()
        if choice not in ["1", "2", "3", "4", "5"]:
            print("Invalid choice. Please choose a number from 1 to 5.")
            continue
        
        display_task_list(choice, task_dict)

        task_to_deal = get_task_to_deal(task_dict)
        if not task_to_deal:
            continue

        move_choice = get_move_choice()
        if move_choice not in ["1", "2", "3", "4"]:
            print("Invalid choice. Task not moved.")
            continue
        
        new_status = ["TO DO", "IN PROGRESS", "REVIEW", "DONE"][int(move_choice) - 1]

        move_task_and_save(task_dict, task_to_deal, new_status, filename)

        if not should_continue():
            break
        
if __name__ == "__main__":
    main()