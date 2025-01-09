import unittest
from unittest.mock import patch
from io import StringIO
from hangeddude import choose_word, display_word, update_guesses, check_win, draw_hangman

class TestHangmanGame(unittest.TestCase):

    @patch('requests.get')
    def test_choose_word_success(self, mock_get):
        """
        Function: test_choose_word_success
        Brief: Mocks successful API response and checks word selection.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = ["python"]
        word = choose_word()
        self.assertIsInstance(word, str)
        self.assertGreater(len(word), 0)

    @patch('requests.get')
    @patch('random.choice')
    def test_choose_word_failure_with_random_fallback(self, mock_random_choice, mock_get):
        """
        Function: test_choose_word_failure_with_random_fallback
        Brief: Mocks API failure and ensures fallback to random word selection works.
        """
        mock_get.return_value.status_code = 500  
        mock_random_choice.return_value = 'banana'
        
        word = choose_word()
        self.assertIsInstance(word, str)
        self.assertGreater(len(word), 0)
        self.assertEqual(word, "banana")

    def test_display_word(self):
        """
        Function: test_display_word
        Brief: Tests word display with guessed letters.
        """
        word = "python"
        guessed_letters = ['p', 'y', 't']
        displayed = display_word(word, guessed_letters)
        self.assertEqual(displayed, "pyt___")  

    def test_update_guesses_correct(self):
        """
        Function: test_update_guesses_correct
        Brief: Tests guess update when the guess is correct.
        """
        word = "python"
        guessed_letters = ['p', 'y']
        incorrect_guesses = 1
        guess = 't'  
        updated_incorrect_guesses = update_guesses(guess, word, guessed_letters, incorrect_guesses)
        self.assertIn('t', guessed_letters)  
        self.assertEqual(updated_incorrect_guesses, 1)  

    def test_update_guesses_incorrect(self):
        """
        Function: test_update_guesses_incorrect
        Brief: Tests guess update when the guess is incorrect.
        """
        word = "python"
        guessed_letters = ['p', 'y']
        incorrect_guesses = 1
        guess = 'a'  
        updated_incorrect_guesses = update_guesses(guess, word, guessed_letters, incorrect_guesses)
        self.assertIn('a', guessed_letters)  
        self.assertEqual(updated_incorrect_guesses, 2)  

    def test_check_win(self):
        """
        Function: test_check_win
        Brief: Tests if the word is fully guessed.
        """
        word = "python"
        guessed_letters = ['p', 'y', 't', 'h', 'o', 'n']
        self.assertTrue(check_win(word, guessed_letters))  

    def test_check_not_win(self):
        """
        Function: test_check_not_win
        Brief: Tests if the word is not fully guessed.
        """
        word = "python"
        guessed_letters = ['p', 'y', 't', 'h', 'o']  
        self.assertFalse(check_win(word, guessed_letters))  

    def test_draw_hangman(self):
        """
        Function: test_draw_hangman
        Brief: Tests hangman drawing for incorrect guesses.
        """
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            draw_hangman(1)  
            output = mock_stdout.getvalue().strip()
            self.assertIn("O", output)  

if __name__ == '__main__':
    unittest.main()