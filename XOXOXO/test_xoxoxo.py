import unittest
from unittest.mock import patch
from io import StringIO
import random

from XOXOXO import clear_screen, print_board, check_win, check_draw, player_move, computer_move, switch_player, handle_game_mode, play_game

class TestTicTacToe(unittest.TestCase):
    
    def setUp(self):
        """Set up the game board for testing."""
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
    
    @patch("builtins.input", side_effect=["1", "1", "1", "2", "3", "4", "5", "6"])
    @patch("builtins.print")
    def test_player_move(self, mock_print, mock_input):
        """Test the player's move input handling."""
        player = "X"
        player_move(self.board, player)
        self.assertEqual(self.board[0][0], "X")
        mock_print.assert_not_called()
        
    @patch("builtins.input", side_effect=["1", "1", "1", "2", "3", "4", "5", "6"])
    def test_player_move_invalid(self, mock_input):
        """Test the invalid player move input."""
        player = "X"
        self.board[0][0] = "O"
        with patch('sys.stdout', new_callable=StringIO) as fake_out:
            player_move(self.board, player)
            output = fake_out.getvalue()
            self.assertIn("This cell is already taken", output)
    
    def test_check_win(self):
        """Test winning conditions for both players."""
        player1 = "X"
        player2 = "O"
        self.board[0] = [player1, player1, player1]
        self.assertTrue(check_win(self.board, player1))
        self.board = [[' ', player2, ' '], [' ', player2, ' '], [' ', player2, ' ']]
        self.assertTrue(check_win(self.board, player2))
        self.board = [[' ', ' ', player1], [' ', player1, ' '], [player1, ' ', ' ']]
        self.assertTrue(check_win(self.board, player1))

        
    def test_check_draw(self):
        """Test the draw condition."""
        self.board = [
            ["X", "O", "X"],
            ["O", "X", "O"],
            ["O", "X", "O"]
        ]
        self.assertTrue(check_draw(self.board))
        self.board[0][0] = ' '
        self.assertFalse(check_draw(self.board))

    def test_switch_player(self):
        """Test the player switch functionality."""
        self.assertEqual(switch_player("X"), "O")
        self.assertEqual(switch_player("O"), "X")

    @patch("builtins.input", side_effect=["1", "2", "1", "2", "1"])
    def test_handle_game_mode(self, mock_input):
        """Test if game mode (player vs player and player vs computer) is working."""
        mode = 'player_vs_player'
        current_player = 'X'
        handle_game_mode(mode, current_player, self.board)
        self.assertEqual(self.board[0][0], 'X')
        mode = 'player_vs_computer'
        current_player = 'X'
        with patch('random.randint', return_value=0):
            handle_game_mode(mode, current_player, self.board)
        self.assertEqual(self.board[0][0], 'X')

    @patch("builtins.input", side_effect=["1", "2", "3", "4", "5", "6", "7", "8", "9"])
    def test_play_game(self, mock_input):
        """Test the play_game loop."""
        mode = 'player_vs_player'
        with patch("builtins.print") as mock_print:
            play_game(mode)
            mock_print.assert_any_call("Player X wins!")
            
if __name__ == "__main__":
    unittest.main()


