import unittest
from unittest.mock import patch, mock_open, MagicMock
from excel_file import parse_line, get_profession_color, read_data, write_data_to_excel, create_workbook, process_file

RUS_NUMBERS = {
    'ноль': 0, 'один': 1, 'два': 2, 'три': 3, 'четыре': 4, 'пять': 5, 'шесть': 6, 'семь': 7, 'восемь': 8, 'девять': 9,
    'десять': 10, 'одиннадцать': 11, 'двенадцать': 12, 'тринадцать': 13, 'четырнадцать': 14, 'пятнадцать': 15,
    'шестнадцать': 16, 'семнадцать': 17, 'восемнадцать': 18, 'девятнадцать': 19, 'двадцать': 20,
    'тридцать': 30, 'сорок': 40, 'пятьдесят': 50, 'шестьдесят': 60, 'семьдесят': 70, 'восемьдесят': 80, 'девяносто': 90
}

def parse_russian_number(word):
    return RUS_NUMBERS.get(word.lower(), None)

def parse_line(line):
    parts = line.split()
    
    if len(parts) < 5:
        print(f"Line does not have enough parts: {line}")
        return None

    full_name = " ".join(parts[:3])
    profession = parts[3] if parts[3] else None
    gender = parts[-1] if parts[-1] else None

    try:
        age = int(parts[4])
    except ValueError:
        age = parse_russian_number(parts[4])
        if age is None:
            print(f"Error processing age in line: {line}. Invalid age")
            return None

    if not profession or not gender:
        print(f"Error processing profession or gender in line: {line}")
        return None

    return full_name, profession, age, gender

class TestHangmanGame(unittest.TestCase):

    def test_parse_line_valid(self):
        """
        Test for valid line parsing
        """
        line = "Name1 Name2 Name3 программист 40 муж"
        result = parse_line(line)
        self.assertEqual(result, ("Name1 Name2 Name3", "программист", 40, "муж"))

    def test_parse_line_not_enough_parts(self):
        """
        Test for line with insufficient parts
        """
        line = "Name1 Name2"
        result = parse_line(line)
        self.assertIsNone(result)

    def test_parse_line_invalid_age(self):
        """
        Test for line with invalid age
        """
        line = "Name1 Name2 Name3 программист сорок муж"
        result = parse_line(line)
        self.assertEqual(result, ("Name1 Name2 Name3", "программист", 40, "муж"))

    def test_get_profession_color_valid(self):
        """
        Test for valid profession to color mapping
        """
        color = get_profession_color("программист")
        self.assertEqual(color, "green")

    def test_get_profession_color_unknown(self):
        """
        Test for unknown profession
        """
        color = get_profession_color("unknown profession")
        self.assertEqual(color, "gray")

    def test_get_profession_color_partial_match(self):
        """
        Test for profession that matches partially (should still return color)
        """
        color = get_profession_color("программист-разработчик")
        self.assertEqual(color, "green")

    def test_get_profession_color_invalid(self):
        """
        Test for invalid input to profession color mapping
        """
        color = get_profession_color(None)
        self.assertEqual(color, "gray")
        color = get_profession_color("")
        self.assertEqual(color, "gray")

    def test_read_data_valid(self):
        """
        Test for reading and parsing data from file
        """
        input_filename = 'people.txt'
        with patch("builtins.open", mock_open(read_data="Name1 Name2 Name3 программист 40 муж\n"
                                                      "Name4 Name5 Name6 певец 30 муж")):
            people = read_data(input_filename)
            self.assertEqual(len(people), 2)
            self.assertEqual(people[0], ("Name1 Name2 Name3", "программист", 40, "муж"))
            self.assertEqual(people[1], ("Name4 Name5 Name6", "певец", 30, "муж"))

    def test_read_data_file_not_found(self):
        """
        Test for file not found error
        """
        input_filename = 'dummy.txt'
        with patch("builtins.open", MagicMock(side_effect=FileNotFoundError)):
            people = read_data(input_filename)
            self.assertEqual(people, [])

    @patch("excel_file.create_workbook")
    @patch("excel_file.write_data_to_excel")
    def test_process_file(self, mock_write_data_to_excel, mock_create_workbook):
        """
        Test for the entire file processing pipeline
        """
        mock_create_workbook.return_value = (MagicMock(), MagicMock(), {})
        mock_write_data_to_excel.return_value = None
        input_filename = 'people.txt'
        output_filename = 'people_output.xlsx'
        
        with patch("excel_file.read_data", return_value=[("Name1 Name2 Name3", "программист", 40, "муж"),
                                                       ("Name4 Name5 Name6", "певец", 30, "муж")]):
            process_file(input_filename, output_filename)
            mock_create_workbook.assert_called_once_with(output_filename)
            mock_write_data_to_excel.assert_called_once()

    @patch("excel_file.create_workbook")
    def test_create_workbook(self, mock_create_workbook):
        """
        Test for workbook creation
        """
        mock_create_workbook.return_value = (MagicMock(), MagicMock(), {})
        output_filename = 'people_output.xlsx'
        workbook, worksheet, color_formats = create_workbook(output_filename)
        self.assertIsNotNone(workbook)
        self.assertIsNotNone(worksheet)

    def test_write_data_to_excel(self):
        """
        Test for writing data to excel
        """
        worksheet_mock = MagicMock()
        color_formats_mock = {}
        people = [("Name1 Name2 Name3", "программист", 40, "муж"),
                  ("Name4 Name5 Name6", "певец", 30, "муж")]
        
        write_data_to_excel(worksheet_mock, color_formats_mock, people)
        worksheet_mock.write_row.assert_called_once_with(0, 0, ["Full Name", "Profession", "Age", "Gender"])

if __name__ == "__main__":
    unittest.main()