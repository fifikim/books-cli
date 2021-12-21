import unittest
import books.main as main

class UtilityTests(unittest.TestCase):
  def test_validate_selection(self):
    list = ['a', 'b', 'c', 'd']
    self.assertTrue(main.validate_selection('1', list))
    self.assertTrue(main.validate_selection('4', list))
    self.assertFalse(main.validate_selection(' ', list))
    self.assertFalse(main.validate_selection('dfdfd', list))

  def test_style_output(self):
    output = main.style_output('testing', 'success')
    self.assertEqual(output, '\033[1;32mtesting\033[0;0m')

class SearchTests(unittest.TestCase):
  def test_fetch_by(self):
    fetched = main.fetch_by('dog')
    notFetched = main.fetch_by('dkfjdkfje9run3m4n3m43')
    self.assertTrue(len(fetched) == 5)
    self.assertFalse(notFetched)

  def test_format_search_results(self):
    data = {
      "items": [
        {
        "volumeInfo": {
        "title": "Flowers for Algernon",
        "authors": [
          "Daniel Keyes"
        ],
        "publisher": "Houghton Mifflin Harcourt"
        }
        }
      ]
    }
    formatted = main.format_search_results(data)
    self.assertTrue(type(formatted[0]) == main.Book)

class ReadingListTests(unittest.TestCase):
  def test_load_saved(self):
    loaded = main.load_saved()
    self.assertEqual(loaded[0], "{\n    \"title\": \"Kindred\",\n    \"author\": \"Octavia E. Butler\",\n    \"publisher\": \"Beacon Press\"\n}")

  def test_format_loaded(self):
    loaded = main.load_saved()
    formatted = main.format_loaded(loaded)
    self.assertTrue(type(formatted[0]) == main.Book)
    self.assertTrue(formatted[0].title == 'Kindred')

# class MenuTests(unittest.TestCase):

# class SaveTests(unittest.TestCase):

# class QuitTests(unittest.TestCase):

# class OutputTests(unittest.TestCase):

if __name__ == '__main__':
  unittest.main()
