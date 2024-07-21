import unittest
from unittest.mock import patch, Mock
import requests
import pandas as pd
from datetime import datetime
import get_spread  

class TestOrderbookFunctions(unittest.TestCase):

    @patch('requests.get')
    def test_fetch_orderbook(self, mock_get):
        # Mock response from the API
        mock_response = Mock()
        expected_json = {
            "success": True,
            "payload": {
                "bids": [{"price": "850000.00", "amount": "0.5"}],
                "asks": [{"price": "860000.00", "amount": "0.8"}],
                "updated_at": "2024-07-21T00:00:00+00:00"
            }
        }
        mock_response.json.return_value = expected_json
        mock_get.return_value = mock_response

        # Call the function
        book = "btc_mxn"
        data = get_spread.fetch_orderbook(book)

        # Verify the result
        self.assertEqual(data, expected_json)
        mock_get.assert_called_once_with(f"https://api.bitso.com/v3/order_book/?book={book}")
        print("TestOrderbookFunctions passed")

    def test_calculate_spread(self):
        bid = 850000.00
        ask = 860000.00
        expected_spread = (ask - bid) * 100 / ask

        # Call the function
        spread = get_spread.calculate_spread(bid, ask)

        # Verify the result
        self.assertEqual(spread, expected_spread)
        print("test_calculate_spread passed")

    @patch('get_spread.fetch_orderbook')
    @patch('get_spread.time.sleep', return_value=None)  # Mock time.sleep to skip delays
    @patch('pandas.DataFrame.to_csv')  # Mock to_csv to avoid file creation
    def test_main(self, mock_to_csv, mock_sleep, mock_fetch_orderbook):
        # Mock fetch_orderbook response
        mock_fetch_orderbook.return_value = {
            "payload": {
                "bids": [{"price": "850000.00"}],
                "asks": [{"price": "860000.00"}],
                "updated_at": "2024-07-21T00:00:00+00:00"
            }
        }

        # Set up mocks for os.makedirs
        with patch('os.makedirs') as mock_makedirs:
            with patch('get_spread.datetime') as mock_datetime:
                # Mock datetime to return a fixed current time
                mock_datetime.utcnow.return_value = datetime(2024, 7, 21, 0, 0, 0)
                mock_datetime.strftime = datetime.strftime

                # Run the main function for a limited number of iterations to test its behavior
                get_spread.main(iterations=600)

                # Verify to_csv was called
                self.assertTrue(mock_to_csv.called)
                self.assertTrue(mock_sleep.called)
                print("test_main passed")
                

if __name__ == '__main__':
    unittest.main()
