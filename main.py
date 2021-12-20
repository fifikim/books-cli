import json
import requests
import math 

# CLASSES
class Menu:
  def __init__(self, options):
    self.options = options

  def print(self):
    print(style_output('\n\nWhat would you like to do?', 'underline'))
    for (i, element) in enumerate(self.options, start=1):
      label = options_dict[element]['label']
      id = style_output(i, 'option')
      print(f'{id} - {label}')
    print('\n')
    self.select()

  def select(self):
    selection = input('Please enter your selection:  ')
    valid = validate_selection(selection, self.options)

    if valid: 
      option = self.options[int(selection) - 1]
      options_dict[option]['function']()
    else:
      print(style_output(f'Invalid selection. Please choose from Options #1-{len(self.options)}.\n', 'warning'))
      self.select()
    
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

# SHARED UTILITIES 
# validates that user-selected option is valid menu choice
def validate_selection(val, list):
  max = len(list)
  if val:
    try:
      num = int(val)
      if num in range(1, (max + 1)):
        return True
      else:
        return False
    except ValueError:
      return False

# formats & numbers books in a printed list
def display_books(list):
  for (i, book) in enumerate(list, start=1):
    print(style_output(f'ID {i}', 'success'))
    book.print()

# applies text decorations to terminal output
def style_output(string, style):
  reset = '\033[0;0m'
  styles = {
    'header': '\033[1;36m',
    'underline': '\033[4;37m',
    'border': '\033[0;35m',
    'title': '\033[3;36m',
    'option': '\033[0;33m',
    'success': '\033[1;32m',
    'warning': '\033[1;31m',
  }
  return f"{styles[style]}{string}{reset}"

# SEARCH FOR BOOKS
def search():
  header = Header('search')
  header.print()
  # TO DO: add escape key to cancel query

  q = validate_query()
  results = fetch_by(q)

  display_results(results)

# validates that search query is not blank
def validate_query():
  query = input('Search for books containing the query:  ')
  if query:
    return query
  else:
    print(style_output('Please enter a valid query.\n', 'warning'))
    validate_query()

# submits api get request & returns relevant data from response
def fetch_by(query):
  search_results.clear()
  response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=5').json()

  # if request fails, return false
  if response['totalItems'] == 0:
    return False
  
  # format data & save to local temp storage
  search_results.extend(format_search_results(response))
  return search_results

# formats response data & saves as Book instance
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

# prints formatted search results & new menu selections
def display_results(results):
  if results == False:
    print(style_output('Sorry, your search returned 0 results.', 'warning'))
  else: 
    print(style_output('\nResults matching your query:\n', 'underline'))
    display_books(search_results)

  menu = Menu(['save', 'new', 'view', 'exit'])
  menu.print()

# saves selected book to reading list
def save():
  selection = input('Please enter the ID of the book to save:   ')
  valid = validate_selection(selection, search_results)

  if valid: 
    selected_book = json.dumps(search_results[int(selection) - 1].__dict__, indent = 4)
    write_to_saved(selected_book)

    print(style_output(f'Saved: {selected_book}', 'success'))

    menu = Menu(['another', 'new', 'view', 'exit'])
    menu.print()

  else:
    print(style_output(f'Invalid selection. Please choose from IDs #1-{len(search_results)}.\n', 'warning'))
    save()

# appends book data to reading_list.json file
def write_to_saved(book):
  with open('reading_list.json','r+') as file:
    file_data = json.load(file)
    file_data["reading_list"].append(book)
    file.seek(0)
    json.dump(file_data, file, indent = 4)

# VIEW READING LIST PAGE
def view_saved():
  header = Header('reading list')
  header.print()

  reading_list = load_saved()

  #include handling for empty list
  if len(reading_list) == 0:
    print(style_output('There are no books in your reading list.', 'warning'))
  else:
    display_books(reading_list)

  menu = Menu(['search', 'exit'])
  menu.print()

# loads data from reading_list.json file & formats each entry as Book instance
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

# QUIT PAGE
def quit():
  quit_header = Header('quit')
  quit_header.print()
  print(style_output('\nThanks for using Books on 8th! Goodbye.\n', 'success'))

# HOME PAGE
def main():
  header = Header('home')
  header.print()

  print(style_output('      Welcome to Books on 8th!', 'header'))

  menu = Menu(['search', 'view', 'quit'])
  menu.print()

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


