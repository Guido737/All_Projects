import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import tasksss 

class TestTaskManagement(unittest.TestCase):

    @patch('builtins.print')
    def test_display_tasks(self, mock_print):
        """
        Function: test_display_tasks
        Params: mock_print (MagicMock)
        Brief: Test display of tasks.
        """
        task_dict = {
            "TO DO": ["task 1", "task 2"],
            "IN PROGRESS": ["task 3"],
            "REVIEW": [],
            "DONE": ["task 4"]
        }

        tasksss.display_tasks(task_dict)
        mock_print.assert_any_call("TO DO: task 1, task 2")
        mock_print.assert_any_call("IN PROGRESS: task 3")
        mock_print.assert_any_call("REVIEW: No tasks")
        mock_print.assert_any_call("DONE: task 4")

    @patch('builtins.input', side_effect=["task 1"])
    @patch('builtins.print')
    def test_get_task_to_deal(self, mock_print, mock_input):
        """
        Function: test_get_task_to_deal
        Params: mock_print (MagicMock), mock_input (MagicMock)
        Brief: Test getting task from user to deal with.
        """
        task_dict = {
            "TO DO": ["task 1", "task 2"],
            "IN PROGRESS": ["task 3"],
            "REVIEW": [],
            "DONE": ["task 4"]
        }

        task_to_deal = tasksss.get_task_to_deal(task_dict)

        self.assertEqual(task_to_deal, "task 1")

    @patch('builtins.input', side_effect=["2", "task 1", "3", "y"])
    @patch('builtins.print')
    @patch('builtins.open', new_callable=MagicMock)
    def test_move_task_and_save(self, mock_open, mock_print, mock_input):
        """
        Function: test_move_task_and_save
        Params: mock_print (MagicMock), mock_input (MagicMock), mock_open (MagicMock)
        Brief: Test moving task and saving it to file.
        """
        task_dict = {
            "TO DO": ["task 1", "task 2"],
            "IN PROGRESS": ["task 3"],
            "REVIEW": [],
            "DONE": ["task 4"]
        }

        filename = "tasks.txt"
        task_to_deal = "task 1"
        new_status = "IN PROGRESS"

        tasksss.move_task_and_save(task_dict, task_to_deal, new_status, filename)
        mock_open.assert_called_once_with(filename, "w")
        self.assertIn("task 1", task_dict["IN PROGRESS"])
        self.assertNotIn("task 1", task_dict["TO DO"])

    @patch('builtins.input', side_effect=["n"])
    @patch('builtins.print')
    def test_should_continue(self, mock_print, mock_input):
        """
        Function: test_should_continue
        Params: mock_print (MagicMock), mock_input (MagicMock)
        Brief: Test user input for continuation.
        """
        continue_choice = tasksss.should_continue()
        self.assertFalse(continue_choice)

    @patch('builtins.input', side_effect=["2", "task 1", "3", "2"])
    @patch('builtins.print')
    def test_get_move_choice(self, mock_print, mock_input):
        """
        Function: test_get_move_choice
        Params: mock_print (MagicMock), mock_input (MagicMock)
        Brief: Test user input for move choice.
        """
        move_choice = tasksss.get_move_choice()
        self.assertEqual(move_choice, "2")

if __name__ == '__main__':
    unittest.main()