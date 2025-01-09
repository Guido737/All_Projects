import unittest
from unittest.mock import patch
from joke_rater import fetch_joke, get_jokes, rate_jokes, save_jokes_to_file

class TestJokeFetcher(unittest.TestCase):

    @patch('requests.get')
    def test_fetch_joke_success(self, mock_get):
        """
        Test successful joke fetch.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'setup': 'Why did the chicken cross the road?',
            'punchline': 'To get to the other side.'
        }

        url = "https://official-joke-api.appspot.com/random_joke"
        joke = fetch_joke(url)
        
        self.assertIsNotNone(joke)
        self.assertEqual(joke['setup'], 'Why did the chicken cross the road?')
        self.assertEqual(joke['punchline'], 'To get to the other side.')

    @patch('requests.get')
    def test_fetch_joke_failure(self, mock_get):
        """
        Test failed joke fetch (server error).
        """
        mock_get.return_value.status_code = 500
        mock_get.return_value.json.side_effect = lambda: None

        url = "https://official-joke-api.appspot.com/random_joke"
        joke = fetch_joke(url)

        self.assertIsNone(joke)

    def test_get_jokes(self):
        """
        Test fetching multiple jokes.
        """
        mock_jokes = [
            {'setup': 'Why did the chicken cross the road?', 'punchline': 'To get to the other side.'},
            {'setup': 'Why don\'t skeletons fight each other?', 'punchline': 'They don\'t have the guts.'}
        ]
        
        with patch('joke_rater.fetch_joke', side_effect=lambda url: mock_jokes.pop(0) if mock_jokes else None):
            jokes = get_jokes("https://official-joke-api.appspot.com/random_joke", 2)
        
        self.assertEqual(len(jokes), 2)
        for joke in jokes:
            joke_str = joke
            self.assertTrue(any(phrase in joke_str for phrase in [
                'Why did the chicken cross the road? To get to the other side.',
                'Why don\'t skeletons fight each other? They don\'t have the guts.'
            ]))

    def test_rate_jokes(self):
        """
        Test random ratings for jokes.
        """
        jokes = [
            "Why did the chicken cross the road? To get to the other side.",
            "Why don't skeletons fight each other? They don't have the guts."
        ]
        
        rated_jokes = rate_jokes(jokes)

        self.assertEqual(len(rated_jokes), 2)
        for rated_joke in rated_jokes:
            self.assertIn('joke', rated_joke)
            self.assertIn('rating', rated_joke)
            self.assertGreaterEqual(rated_joke['rating'], 1)
            self.assertLessEqual(rated_joke['rating'], 10)

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_save_jokes_to_file(self, mock_file):
        """
        Test saving jokes to a file.
        """
        rated_jokes = [
            {"joke": "Why did the chicken cross the road? To get to the other side.", "rating": 8},
            {"joke": "Why don't skeletons fight each other? They don't have the guts.", "rating": 5}
        ]
        
        save_jokes_to_file(rated_jokes)

        mock_file.assert_called_once_with('top_jokes.txt', 'w', encoding='utf-8')
        mock_file().write.assert_any_call("Joke: Why did the chicken cross the road? To get to the other side.\nRating: 8\n")
        mock_file().write.assert_any_call("Joke: Why don't skeletons fight each other? They don't have the guts.\nRating: 5\n")

if __name__ == '__main__':
    unittest.main()