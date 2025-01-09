"""
Excel File
Created by: Creator/Eversor
Date: 30 Dec 2024
"""

import xlsxwriter

def parse_line(line):
    """
    Function: parse_line
    Params: line (str) - input line
    Brief: Parse data
    """
    try:
        parts = line.strip().split()
        if len(parts) >= 4:
            name = ' '.join(parts[:-3])
            profession = parts[-3]
            try:
                age = int(parts[-2])
                gender = parts[-1]
                return name, profession, age, gender
            except ValueError as e:
                print(f"Error processing age in line: {line}. Error: {e}")
                return None
        else:
            print(f"Line does not have enough parts: {line}")
            return None
    except (AttributeError, TypeError) as e:
        print(f"Error with line data structure: {line}. Error: {e}")
        return None
    except Exception as e:
        print(f"Error parsing line: {line}. Error: {e}")
        return None

def get_profession_color(profession):
    """
    Function: get_profession_color
    Params: profession (str) - profession
    Brief: Return color
    """
    try:
        profession_colors = {
            'программист': "green",
            'певец': "yellow",
            'музыкант': "pink",
            'писатель': "red",
            'горняк': "brown",
            'стоматолог': "blue",
            'официантка': "white",
            'продавец': "tomato"
        }
        
        profession = profession.lower()
        for key, color in profession_colors.items():
            if key in profession:
                return color
        return "gray"
    except (AttributeError, TypeError) as e:
        print(f"Error processing profession: {profession}. Error: {e}")
        return "gray"
    except Exception as e:
        print(f"Unexpected error while determining color for profession: {profession}. Error: {e}")
        return "gray"
    
def read_data(input_filename):
    """
    Function: read_data
    Params: input_filename (str) - file path
    Brief: Read file
    """
    people = []
    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            for line in f:
                parsed_data = parse_line(line.strip())
                if parsed_data:
                    people.append(parsed_data)
    except FileNotFoundError as e:
        print(f"Error: File not found. Error: {e}")
    except IOError as e:
        print(f"Error reading file: {input_filename}. Error: {e}")
    except (PermissionError, OSError) as e:
        print(f"Permission error or OS error while accessing file: {input_filename}. Error: {e}")
    except Exception as e:
        print(f"Unexpected error while reading data: {e}")
    return people

def create_workbook(output_filename):
    """
    Function: create_workbook
    Params: output_filename (str) - file path
    Brief: Create workbook
    """
    try:
        workbook = xlsxwriter.Workbook(output_filename)
        worksheet = workbook.add_worksheet()
        color_formats = {
            "green": workbook.add_format({'bg_color': 'green', 'font_color': 'black'}),
            "yellow": workbook.add_format({'bg_color': 'yellow', 'font_color': 'black'}),
            "red": workbook.add_format({'bg_color': 'red', 'font_color': 'black'}),
            "brown": workbook.add_format({'bg_color': 'brown', 'font_color': 'black'}),
            "blue": workbook.add_format({'bg_color': 'blue', 'font_color': 'black'}),
            "white": workbook.add_format({'bg_color': 'white', 'font_color': 'black'}),
            "tomato": workbook.add_format({'bg_color': 'tomato', 'font_color': 'black'}),
            "gray": workbook.add_format({'bg_color': 'gray', 'font_color': 'black'}),
        }
        return workbook, worksheet, color_formats
    except (PermissionError, OSError) as e:
        print(f"Error creating or writing to workbook: {output_filename}. Error: {e}")
        return None, None, None
    except Exception as e:
        print(f"Unexpected error creating workbook: {output_filename}. Error: {e}")
        return None, None, None

def write_data_to_excel(worksheet, color_formats, people):
    """
    Function: write_data_to_excel
    Params: worksheet - worksheet
            color_formats (dict) - color formats
            people (list) - people data
    Brief: Write data
    """
    try:
        worksheet.write_row(0, 0, ["Full Name", "Profession", "Age", "Gender"])
        row = 1
        for person in people:
            name, profession, age, gender = person
            color = get_profession_color(profession)
            format_for_row = color_formats[color]
            worksheet.write(row, 0, name, format_for_row)
            worksheet.write(row, 1, profession, format_for_row)
            worksheet.write(row, 2, age, format_for_row)
            worksheet.write(row, 3, gender, format_for_row)
            row += 1

    except (ValueError, TypeError) as e:
        print(f"Error writing data: Invalid data. Error: {e}")
    except Exception as e:
        print(f"Unexpected error writing data to Excel. Error: {e}")

def process_file(input_filename, output_filename):
    """
    Function: process_file
    Params: input_filename (str) - input file
            output_filename (str) - output file
    Brief: Process data
    """
    try:
        people = read_data(input_filename)
        if not people:
            print(f"No valid data found in file: {input_filename}")
            return
        people.sort(key=lambda x: x[1])
        workbook, worksheet, color_formats = create_workbook(output_filename)
        if workbook and worksheet:
            write_data_to_excel(worksheet, color_formats, people)
            workbook.close()
            print(f"Data saved: {output_filename}")
        else:
            print("Error: Failed to create Excel workbook.")
    except (FileNotFoundError, IOError) as e:
        print(f"File error processing: {e}")
    except (PermissionError, OSError) as e:
        print(f"Permission error processing file: {e}")
    except Exception as e:
        print(f"Unexpected error processing file: {e}")

def main():
    """
    Function: main
    Brief: Run process
    """
    try:
        input_filename = '/home/usernamezero00/Desktop/myprojects/All_Projects/Excel_File/people.txt'
        output_filename = '/home/usernamezero00/Desktop/people_output.xlsx'
        process_file(input_filename, output_filename)
    except Exception as e:
        print(f"Error in main function: {e}")

if __name__ == "__main__":
    main()