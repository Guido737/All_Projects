import unittest
from unittest.mock import patch, mock_open
from word_frequency_count import clean_text, read_file, filter_words, count_word_frequencies, print_most_common_words


stop_words = set([
    'он', 'бою', 'на', 'всегда', 'в', 'для', 'о', 'по', 'это', 'или', 'быть', 'забыл', 'добавить', 'подсказку', 
    'потому', 'что', 'опилки', 'вместо', 'мозгов', 'не'
])

class TestWordFrequencyFunctions(unittest.TestCase):

    def test_clean_text(self):
        """
        Function: test_clean_text
        Brief: Test text cleaning function.
        """
        text = "Hello, World! This is a Test."
        cleaned = clean_text(text)
        self.assertEqual(cleaned, "hello world this is a test")

    @patch("builtins.open", mock_open(read_data="Dummy file content here."))
    def test_read_file(self):
        """
        Function: test_read_file
        Brief: Test file reading function with mock.
        """
        text = read_file("dummy_path.txt")
        self.assertEqual(text, "Dummy file content here.")

    def test_filter_words(self):
        """
        Function: test_filter_words
        Brief: Test filtering stop words and non-alphabetic words.
        """
        text = "Это тест на Python и не был забыт"
        filtered_words = filter_words(text, stop_words)
        expected_words = ["тест", "python", "был", "забыт"]
        filtered_words_set = set(filtered_words)
        expected_words_set = set(expected_words)
        
        self.assertEqual(filtered_words_set, expected_words_set)

    def test_count_word_frequencies(self):
        """
        Function: test_count_word_frequencies
        Brief: Test the word frequency counting function.
        """
        filtered_words = ["тест", "python", "был", "забыт", "тест", "python"]
        word_counts = count_word_frequencies(filtered_words)
        self.assertEqual(word_counts["тест"], 2)
        self.assertEqual(word_counts["python"], 2)
        self.assertEqual(word_counts["был"], 1)
        self.assertEqual(word_counts["забыт"], 1)

    @patch("builtins.print")
    def test_print_most_common_words(self, mock_print):
        """
        Function: test_print_most_common_words
        Brief: Test printing the most common words.
        """
        word_counts = count_word_frequencies({"тест": 2, "python": 2, "был": 1, "забыт": 1})
        print_most_common_words(word_counts, top_n=2)
        mock_print.assert_any_call("Top 2 catchwords:")
        mock_print.assert_any_call("тест: 2")
        mock_print.assert_any_call("python: 2")

if __name__ == "__main__":
    unittest.main()
