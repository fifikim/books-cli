import json
import requests
import math 

# CLASSES
class Menu:
  def __init__(self, options):
    self.options = options

  def print(self):
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

    print(f'\n{border}')
    print(f'{margin}{self.name}{margin}')
    print(f'{border}\n')

class Book:
  def __init__(self, title, author, publisher):
    self.title = title
    self.author = author
    self.publisher = publisher
  
  def print(self):
    print(f'    Title: {self.title}')
    print(f'    Author(s): {self.author}')
    print(f'    Publisher: {self.publisher}\n')

  def json(self):
    return {
      "title": f"{self.title}",
      "author": f"{self.author}",
      "publisher": f"{self.author}"
    }

# UTILITIES 
def format_books(data):
  books = []
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
    book = Book(title, author, publisher)
    books.append(book)
  return books

def display_books(list):
  for (i, book) in enumerate(list, start=1):
    print(f'ID {i}')
    book.print()

# SEARCH 
def search():
  header = Header('search')
  header.print()

  query = input('Search for books containing the query:  ').lower()

  # TO DO: add escape key to cancel query
  results = get_search_results(query)

  if results == False:
    print('Sorry, your search returned 0 results.')
    menu = Menu(['search', 'view', 'exit'])
    menu.print()
  else:
    display_search_results()

def get_search_results(query):
  search_results.clear()
  response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=5').json()

  # if request fails, return false
  if response['totalItems'] == 0:
    return False
  
  # convert response obj to dictionary & format data
  search_results.extend(format_books(response))
  return search_results

def display_search_results():
  print('\nMatching Results:')
  print('------------------\n')
  display_books(search_results)

  menu = Menu(['save', 'new', 'view', 'exit'])
  menu.print()

def save():
  num = input('Enter the ID of the book to save:  ')
  book = search_results[int(num) - 1].json()
  # TO DO: add validation to prevent duplicate records?
  
  with open('reading_list.json','r+') as file:
    file_data = json.load(file)
    file_data["reading_list"].append(book)
    file.seek(0)
    json.dump(file_data, file, indent = 4)

  print(f'Saved: {book}')

  menu = Menu(['another', 'new', 'view', 'exit'])
  menu.print()

# READING LIST 
def view_list():
  # open JSON reading list file
  f = open('reading_list.json')

  # return JSON object as dictionary & extract list
  data = json.load(f)
  reading_list = data['reading_list']

  # include handling for empty list
  if len(reading_list) == 0:
    print('There are no books in your reading list.')
  else:
    header = Header('reading list')
    header.print()

    formatted = []
    for book in reading_list:
      formatted.append(Book(book['title'], book['author'], book['publisher']))
    display_books(formatted)

  menu = Menu(['search', 'exit'])
  menu.print()

# QUIT 
def quit():
  quit_header = Header('quit')
  quit_header.print()
  print("Thanks for using Books on 8th!\n")

# MAIN
def main():
  header = Header('main')
  header.print()

  print('\n     Welcome to Books on 8th!')
  print('     ~~~~~~~~~~~~~~~~~~~~~~~~\n')

  menu = Menu(['search', 'view', 'quit'])
  menu.print()

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
    'function': view_list
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


