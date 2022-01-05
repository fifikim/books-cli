import unittest
from unittest import mock
from unittest.mock import patch
import io
import sys

from requests import status_codes
from main import *


class UtilityTests(unittest.TestCase):
    def test_validate_selection(self):
        list = ['a', 'b', 'c', 'd']
        self.assertTrue(validate_selection('1', list))
        self.assertTrue(validate_selection('4', list))
        self.assertFalse(validate_selection(' ', list))
        self.assertFalse(validate_selection('dfdfd', list))

    def test_style_output(self):
        output = style_output('testing', 'success')
        self.assertEqual(output, '\033[1;32mtesting\033[0;0m')

    def test_list_all_lists(self):
        actual = list_all_lists()
        expected = ['Reading List', 'My Favorites']
        self.assertEqual(actual, expected)

class BookTests(unittest.TestCase):
    def test_repr(self):
        book = Book('id23', 'My Title', 'Sophia Kim', 'Fifi Publishing Co.')
        expected = "\n    Title: My Title\n    Author(s): Sophia Kim\n    Publisher: Fifi Publishing Co."
        self.assertEqual(repr(book), expected)

class ApiTests(unittest.TestCase):
    def test_get_response_returns_reponse(self):
        with patch('requests.get') as mock_request:
            url = 'https://www.googleapis.com/books/v1/volumes?q=unittest&maxResults=5&startIndex=0'
            s = Search()
            mock_request.return_value = 'mock content'
            response = s.get_response(url)
            self.assertIsNotNone(response)
            mock_request.assert_called_once_with(url)

    def test_returns_200_if_ok_response(self):
        with patch('requests.get') as mock_request:
            url = 'https://www.googleapis.com/books/v1/volumes?q=unittest&maxResults=5&startIndex=0'
            s = Search()
            mock_request.return_value.status_code = 200
            self.assertEqual(s.get_response(url).status_code, 200)
            mock_request.assert_called_once_with(url)
    
    def test_returns_404_if_bad_response(self):
        with patch('requests.get') as mock_request:
            url = 'https://www.googleapis.com/books/v1/volumes?q=unittest&maxResults=5&startIndex=0'
            s = Search()
            mock_request.return_value.status_code = 404
            self.assertEqual(s.get_response(url).status_code, 404)
            mock_request.assert_called_once_with(url)

    @patch('requests.get')
    def test_returns_connection_error_exception(self, mock_request):
        url = 'https://www.googleapis.com/books/v1/volumes?q=unittest&maxResults=5&startIndex=0'
        mock_request.side_effect = requests.exceptions.ConnectionError()
        s = Search()
        response = s.get_response(url)
        self.assertEqual(response, 'Connection Error')
        mock_request.assert_called_once_with(url)

    @patch('requests.get')
    def test_returns_HTTPError_exception(self, mock_request):
        url = 'https://www.googleapis.com/books/v1/volumes?q=unittest&maxResults=5&startIndex=0'
        mock_request.side_effect = requests.exceptions.HTTPError()
        s = Search()
        response = s.get_response(url)
        self.assertEqual(response, 'HTTP Error')
        mock_request.assert_called_once_with(url)

    @patch('requests.get')
    def test_returns_exception(self, mock_request):
        url = 'https://www.googleapis.com/books/v1/volumes?q=unittest&maxResults=5&startIndex=0'
        mock_request.side_effect = requests.exceptions.RequestException()
        s = Search()
        response = s.get_response(url)
        self.assertEqual(response, 'Exception')
        mock_request.assert_called_once_with(url)

    @patch('requests.get')
    def test_returns_timeout_exception(self, mock_request):
        url = 'https://www.googleapis.com/books/v1/volumes?q=unittest&maxResults=5&startIndex=0'
        mock_request.side_effect = requests.exceptions.Timeout()
        s = Search()
        response = s.get_response(url)
        self.assertEqual(response, 'Time Out')
        mock_request.assert_called_once_with(url)

# '''These output tests are not working properly!'''
# class TestHeaderPrint(unittest.TestCase):

#     def test_header_gets_to_stdout(self):
#         expected_output = '''==============================
# #  ==================================
# # =               HOME               =
# #  ==================================
# #    =============================='''

#         with patch('sys.stdout', new = io.StringIO()) as fake_out:
#             print_header('home')
#             self.assertEqual(fake_out.getvalue(), expected_output)

#   def test_output(self, function, arg):
#       captured_output = io.StringIO()
#       sys.stdout = captured_output
#       function(arg)
#       string = captured_output.getvalue().strip()
#       sys.stdout = sys.__stdout__
#       return string

#   def test_(self):
#     expected = '''==============================
#  ==================================
# =               HOME               =
#  ==================================
#    =============================='''
#     output = self.test_output(print_header, 'home')
#     self.assertEqual(expected, output)

if __name__ == '__main__':
    unittest.main()
