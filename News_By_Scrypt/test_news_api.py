import unittest
from unittest.mock import patch, MagicMock
from news_scrypt import get_news, save_to_file, build_params, fetch_news_from_api, handle_response, retry_request

class TestNewsFetcher(unittest.TestCase):

    """API key for testing"""
    API_KEY = '8345c95a63644a2f92b60f44ebaa5d3c'

    @patch('news_scrypt.requests.get')
    def test_fetch_news_from_api_success(self, mock_get):
        """
        Test successful news fetching through the API.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'articles': ['test_article']}
        mock_get.return_value = mock_response

        """Request to fetch news"""
        response = fetch_news_from_api({'apiKey': self.API_KEY, 'q': 'test'})
        """Assert that the response is successful and contains articles"""
        self.assertEqual(response.status_code, 200)
        self.assertIn('articles', response.json())

    @patch('news_scrypt.requests.get')
    def test_fetch_news_from_api_failure(self, mock_get):
        """
        Test failed news fetching (server error).
        """
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        """Request to fetch news with server error"""
        response = fetch_news_from_api({'apiKey': self.API_KEY, 'q': 'test'})
        """Assert that the error code is 500"""
        self.assertEqual(response.status_code, 500)

    @patch('news_scrypt.requests.get')
    def test_retry_request(self, mock_get):
        """
        Test retrying a request after a 500 error.
        """
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        """Simulate a successful response after a 500 error"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'articles': ['retry_article']}

        """Assert that the request succeeds after retrying"""
        response = retry_request(mock_response, retries=3, delay=1)
        self.assertEqual(response.status_code, 200)

    def test_get_news_by_category(self):
        """
        Test fetching news by category.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'articles': [{'title': 'category_article', 'source': {'name': 'test_source'}, 'publishedAt': '2024-12-30', 'url': 'http://test.com'}]}

        """Test fetching news by category "business"""
        with patch('news_scrypt.requests.get', return_value=mock_response):
            news = get_news(self.API_KEY, query='tech', category='business')
            self.assertEqual(len(news), 1)
            self.assertIn('category_article', news[0]['title'])

    def test_get_news(self):
        """
        Test fetching news by query.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'articles': ['test_article']}
        with patch('news_scrypt.requests.get', return_value=mock_response):
            news = get_news(self.API_KEY, 'test_query', 'business')
            self.assertEqual(len(news), 1)

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_save_to_file(self, mock_file):
        """
        Test saving news to a file.
        """
        mock_news = [{'title': 'test_title', 'source': {'name': 'test_source'}, 'publishedAt': '2024-12-30', 'url': 'http://test.com'}]
        save_to_file(mock_news)
        mock_file.assert_called_once_with('news_today.txt', 'w', encoding='utf-8')

if __name__ == "__main__":
    unittest.main()