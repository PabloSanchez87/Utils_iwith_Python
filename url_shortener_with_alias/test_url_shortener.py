import unittest
from unittest.mock import patch, MagicMock
import requests

from url_shortener import url_shortener, is_valid_url

class TestURLShortener(unittest.TestCase):

    def test_is_valid_url_success(self):
        url = "https://www.example.com"
        with patch('requests.head') as mocked_head:
            mocked_head.return_value.status_code = 200
            self.assertTrue(is_valid_url(url))

    def test_is_valid_url_failure(self):
        url = "https://www.invalidurl.com"
        with patch('requests.head') as mocked_head:
            mocked_head.return_value.status_code = 404
            self.assertFalse(is_valid_url(url))

    def test_url_shortener_success(self):
        original_url = "https://www.example.com"
        nick_url = "example"

        response_data = {
            'shorturl': 'https://is.gd/example'
        }

        with patch('requests.get') as mocked_get:
            mocked_get.return_value.json.return_value = response_data
            shorted_url = url_shortener(original_url, nick_url)
            self.assertEqual(shorted_url, 'https://is.gd/example')

    def test_url_shortener_alias_exists(self):
        original_url = "https://www.example.com"
        nick_url = "existing_alias"

        response_data = {
            'errorcode': 2,
            'errormessage': 'The shortened URL you picked already exists, please choose another.'
        }

        with patch('requests.get') as mocked_get:
            mocked_get.return_value.json.return_value = response_data
            shorted_url = url_shortener(original_url, nick_url)
            self.assertIsNone(shorted_url)

if __name__ == '__main__':
    unittest.main()
