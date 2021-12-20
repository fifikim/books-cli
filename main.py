import json
import requests
import math 

# CLASSES
class Menu:
  def __init__(self, options):
    self.options = options

  def select(self):
    print('\nWhat would you like to do?')
    print('--------------------------')
    for (i, element) in enumerate(self.options, start=1):
      label = options_dict[element]['label']
      print(f'{i} - {label}')
    print('\n')

    selection = input('Please enter your selection:  ')

    # to-do: display error message if invalid type is entered (not int)
    if int(selection) not in range(1, len(self.options) + 1):
      input('Please choose a number from the selections listed:  ')
    
    option = self.options[int(selection) - 1]
    options_dict[option]['function']()

class Header:
  def __init__(self, name):
    self.name = name.upper()
  
  def print(self):
    margin = math.floor((35 - len(self.name)) / 2) * ' '
    border = '=' * 35
    print(f'\n\n{border}')
    print(f'{margin}{self.name}{margin}')
    print(f'{border}\n\n')

class Book:
  def __init__(self, title, author, publisher):
    self.title = title
    self.author = author
    self.publisher = publisher
  
  def print(self):
    print(f'    Title: {self.title}')
    print(f'    Author(s): {self.author}')
    print(f'    Publisher: {self.publisher}\n')

# UTILITIES 
def display_books(list):
  for (i, book) in enumerate(list, start=1):
    print(f'ID {i}')
    book.print()

# SEARCH 
def search():
  header = Header('search')
  header.print()

  query = input('Search for books containing the query:  ').lower()
  # TO DO: handle empty query 
  # TO DO: add escape key to cancel query
  results = fetch_by(query)

  if results == False:
    print('Sorry, your search returned 0 results.\n')
    menu = Menu(['search', 'view', 'exit'])
    menu.select()
  else:
    display_results()

def fetch_by(query):
  search_results.clear()
  response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=5').json()

  # if request fails, return false
  if response['totalItems'] == 0:
    return False
  
  # convert response obj to dictionary & format data
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

def display_results():
  print('\nMatching Results:')
  print('------------------\n')
  display_books(search_results)

  menu = Menu(['save', 'new', 'view', 'exit'])
  menu.select()

def save():
  num = int(input('Enter the ID of the book to save:  '))
  selection = json.dumps(search_results[num - 1].__dict__, indent = 4)
  # TO DO: add validation to prevent duplicate records?

  write_to_saved(selection)
  print(f'Saved: {selection}')

  menu = Menu(['another', 'new', 'view', 'exit'])
  menu.select()

def write_to_saved(book):
  with open('reading_list.json','r+') as file:
    file_data = json.load(file)
    file_data["reading_list"].append(book)
    file.seek(0)
    json.dump(file_data, file, indent = 4)

# READING LIST 
def view_saved():
  header = Header('reading list')
  header.print()

  reading_list = load_saved()

  #include handling for empty list
  if len(reading_list) == 0:
    print('There are no books in your reading list.')
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
  print("Thanks for using Books on 8th! Goodbye.")

# MAIN
def main():
  header = Header('main')
  header.print()

  print('\n     Welcome to Books on 8th!')
  print('     ~~~~~~~~~~~~~~~~~~~~~~~~\n')

  menu = Menu(['search', 'view', 'quit'])
  menu.select()

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


