import unittest
from unittest.mock import patch, MagicMock
import crypto_status

class TestCryptoStatus(unittest.TestCase):

    @patch('crypto_status.requests.get')
    def test_get_data_success(self, mock_get):
        """Test successful API response"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': [
                {'name': 'Bitcoin', 'symbol': 'BTC', 'priceUsd': '40000', 'marketCapUsd': '700000000000', 'volumeUsd24Hr': '50000000000', 'changePercent24Hr': '3.5'},
                {'name': 'Ethereum', 'symbol': 'ETH', 'priceUsd': '3000', 'marketCapUsd': '400000000000', 'volumeUsd24Hr': '40000000000', 'changePercent24Hr': '2.5'}
            ]
        }
        mock_get.return_value = mock_response

        result = crypto_status.get_data()
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)

    @patch('crypto_status.requests.get')
    def test_get_data_failure(self, mock_get):
        """Test API failure"""
        mock_get.side_effect = Exception("API request failed")

        result = crypto_status.get_data()
        self.assertIsNone(result)

    def test_filter_name_valid(self):
        """Test filter by valid name"""
        sample_data = [
            {'name': 'Bitcoin', 'symbol': 'BTC', 'priceUsd': '40000', 'marketCapUsd': '700000000000', 'volumeUsd24Hr': '50000000000', 'changePercent24Hr': '3.5'},
            {'name': 'Ethereum', 'symbol': 'ETH', 'priceUsd': '3000', 'marketCapUsd': '400000000000', 'volumeUsd24Hr': '40000000000', 'changePercent24Hr': '2.5'}
        ]
        result = crypto_status.filter_name(sample_data, 'Bitcoin')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'Bitcoin')

    def test_filter_name_invalid(self):
        """Test filter by invalid name"""
        sample_data = [
            {'name': 'Bitcoin', 'symbol': 'BTC', 'priceUsd': '40000', 'marketCapUsd': '700000000000', 'volumeUsd24Hr': '50000000000', 'changePercent24Hr': '3.5'},
            {'name': 'Ethereum', 'symbol': 'ETH', 'priceUsd': '3000', 'marketCapUsd': '400000000000', 'volumeUsd24Hr': '40000000000', 'changePercent24Hr': '2.5'}
        ]
        result = crypto_status.filter_name(sample_data, 'NonExistingCoin')
        self.assertEqual(len(result), 0)

    def test_filter_value_valid(self):
        """Test filter by value (price > 5000)"""
        sample_data = [
            {'name': 'Bitcoin', 'symbol': 'BTC', 'priceUsd': '40000', 'marketCapUsd': '700000000000', 'volumeUsd24Hr': '50000000000', 'changePercent24Hr': '3.5'},
            {'name': 'Ethereum', 'symbol': 'ETH', 'priceUsd': '3000', 'marketCapUsd': '400000000000', 'volumeUsd24Hr': '40000000000', 'changePercent24Hr': '2.5'}
        ]
        result = crypto_status.filter_value(sample_data, 5000)
        self.assertEqual(len(result), 1)

    def test_filter_value_no_results(self):
        """Test filter by value with no results"""
        sample_data = [
            {'name': 'Bitcoin', 'symbol': 'BTC', 'priceUsd': '40000', 'marketCapUsd': '700000000000', 'volumeUsd24Hr': '50000000000', 'changePercent24Hr': '3.5'},
            {'name': 'Ethereum', 'symbol': 'ETH', 'priceUsd': '3000', 'marketCapUsd': '400000000000', 'volumeUsd24Hr': '40000000000', 'changePercent24Hr': '2.5'}
        ]
        result = crypto_status.filter_value(sample_data, 50000)
        self.assertEqual(len(result), 0)

    @patch('builtins.print')
    def test_output_data(self, mock_print):
        """Test output data function"""
        sample_data = [
            {'name': 'Bitcoin', 'symbol': 'BTC', 'priceUsd': '40000', 'marketCapUsd': '700000000000', 'volumeUsd24Hr': '50000000000', 'changePercent24Hr': '3.5'},
            {'name': 'Ethereum', 'symbol': 'ETH', 'priceUsd': '3000', 'marketCapUsd': '400000000000', 'volumeUsd24Hr': '40000000000', 'changePercent24Hr': '2.5'}
        ]
        crypto_status.output_data(sample_data)
        mock_print.assert_any_call("Name: Bitcoin")
        mock_print.assert_any_call("Price Change (24h): 3.5%")
        mock_print.assert_any_call("Market Cap: $700000000000")
        
    @patch('builtins.input', return_value='1')
    def test_get_filter_choice(self, mock_input):
        """Test filter choice input"""
        choice = crypto_status.get_filter_choice()
        self.assertEqual(choice, '1')

    @patch('builtins.input', return_value='Bitcoin')
    @patch('crypto_status.filter_name', return_value=[])
    def test_handle_filter_choice_name(self, mock_filter, mock_input):
        """Test handling filter choice for name"""
        sample_data = [{'name': 'Bitcoin', 'symbol': 'BTC', 'priceUsd': '40000'}]
        crypto_status.handle_filter_choice('1', sample_data)
        mock_filter.assert_called_with(sample_data, 'Bitcoin')

if __name__ == '__main__':
    unittest.main()