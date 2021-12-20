import json
import requests
import math 

# CLASSES
class Menu:
  def __init__(self, options):
    self.options = options

  def select(self):
    print(style_output('\n\nWhat would you like to do?', 'underline'))
    for (i, element) in enumerate(self.options, start=1):
      label = options_dict[element]['label']
      id = style_output(i, 'option')
      print(f'{id} - {label}')
    print('\n')

    val = validate_selection('Please enter your selection:  ', self.options)
    print(f'value {val}')
    option = self.options[(val - 1)]
    options_dict[option]['function']()

class Header:
  def __init__(self, name):
    self.name = name.upper()
  
  def print(self):
    margin = math.floor((35 - len(self.name)) / 2) * ' '
    border = '=' * 30
    border2 = '=' * 34
    heading = style_output(self.name, 'header')
    print(f'\n\n   {border}')
    print(f" {style_output(border2, 'border')}")
    print(f'={margin}{heading}{margin}=')
    print(f" {style_output(border2, 'border')}")
    print(f'   {border}\n\n')

class Book:
  def __init__(self, title, author, publisher):
    self.title = title
    self.author = author
    self.publisher = publisher
  
  def print(self):
    title = style_output(self.title, 'title')
    print(f'    Title: {title}')
    print(f'    Author(s): {self.author}')
    print(f'    Publisher: {self.publisher}')

# UTILITIES 
def validate_selection(message, list):
  max = len(list)
  alert = style_output(f'Invalid selection. Please choose from Options 1 - {max}.\n', 'warning')

  selection = input(message)
  print(f'list {list}')
  if selection:
    try:
      val = int(selection)
      if val in range(1, (max + 1)):
        print(f'val {val}')
        return val
    except ValueError:
      print(alert)
      validate_selection(message, list)
  print(alert)
  validate_selection(message, list)

def display_books(list):
  for (i, book) in enumerate(list, start=1):
    print(style_output(f'ID {i}', 'success'))
    book.print()

def style_output(string, style):
  styles = {
    'header': '\033[1;36m',
    'underline': '\033[4;37m',
    'border': '\033[0;35m',
    'title': '\033[3;36m',
    'option': '\033[0;33m',
    'success': '\033[1;32m',
    'warning': '\033[1;31m',
    'reset': '\033[0;0m'
  }
  return f"{styles[style]}{string}{styles['reset']}"

# SEARCH FOR BOOKS
def search():
  header = Header('search')
  header.print()
  # TO DO: add escape key to cancel query

  q = validate_query()
  results = fetch_by(q)

  display_results(results)

def validate_query():
  query = input('Search for books containing the query:  ')
  if query:
    return query
  else:
    print(style_output('Please enter a valid query.\n', 'warning'))
    validate_query()

def fetch_by(query):
  search_results.clear()
  response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=5').json()

  # if request fails, return false
  if response['totalItems'] == 0:
    return False
  
  # print(response)
  # format data & save to local temp storage
  search_results.extend(format_search_results(response))
  return search_results

def format_search_results(data):
  results = []
  for item in data['items']:
    if 'title' not in item['volumeInfo']:
      title = ''
    else:
      title = item['volumeInfo']['title']
    if 'authors' not in item['volumeInfo']:
      author = ''
    else:
      author = ', '.join(item['volumeInfo']['authors'])
    if 'publisher' not in item['volumeInfo']:
      publisher = ''
    else: 
      publisher = item['volumeInfo']['publisher']
    result = Book(title, author, publisher)
    results.append(result)
  return results

def display_results(results):
  if results == False:
    print(style_output('Sorry, your search returned 0 results.', 'warning'))
  else: 
    print(style_output('\nResults matching your query:\n', 'underline'))
    display_books(search_results)

  menu = Menu(['save', 'new', 'view', 'exit'])
  menu.select()

def save():
  num = validate_selection('Please enter the ID of the book to save:   ', search_results)
  selected_book = json.dumps(search_results[(num - 1)].__dict__, indent = 4)
  # TO DO: add validation to prevent duplicate records?
  # (use list comprehension to check if ID is in reading_list)

  write_to_saved(selected_book)
  print(style_output(f'Saved: {selected_book}', 'success'))

  menu = Menu(['another', 'new', 'view', 'exit'])
  menu.select()

def write_to_saved(book):
  with open('reading_list.json','r+') as file:
    file_data = json.load(file)
    file_data["reading_list"].append(book)
    file.seek(0)
    json.dump(file_data, file, indent = 4)

# VIEW READING LIST 
def view_saved():
  header = Header('reading list')
  header.print()

  reading_list = load_saved()

  #include handling for empty list
  if len(reading_list) == 0:
    print(style_output('There are no books in your reading list.', 'warning'))
  else:
    # saved_books = format_saved_books(reading_list)
    display_books(reading_list)

  menu = Menu(['search', 'exit'])
  menu.select()

def load_saved():
  # open JSON file & extract list
  f = open('reading_list.json')
  data = json.load(f)
  list = data['reading_list']

  # format JSON strings as list of Book instances
  books = []
  for record in list:
    book = json.loads(record)
    books.append(Book(book['title'], book['author'], book['publisher']))
  return books

# QUIT 
def quit():
  quit_header = Header('quit')
  quit_header.print()
  print(style_output('Thanks for using Books on 8th! Goodbye.', 'success'))

# MAIN
def main():
  header = Header('home')
  header.print()

  print(style_output('      Welcome to Books on 8th!', 'header'))

  menu = Menu(['search', 'view', 'quit'])
  menu.select()

# GLOBAL VARIABLES
search_results = []
options_dict = {
  'search': {
    'label': 'Search for books',
    'function': search
  }, 
  'new': {
    'label': 'Start a new search',
    'function': search
  }, 
  'save': {
    'label': 'Save a book to my reading list',
    'function': save
  },
  'another': {
    'label': 'Save another book to my reading list',
    'function': save
  },
  'view': {
    'label': 'View my reading list',
    'function': view_saved
  }, 
  'exit': {
    'label': 'Exit to home',
    'function': main
  },
  'quit': {
    'label': 'Quit',
    'function': quit
  }
}

if __name__ == '__main__': main()


