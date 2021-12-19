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

class Query:
  def __init__(self, query):
    self.query = query.lower()

  def format(self):
    # TO DO: use regex to remove special chars from query, make lowercase
    # TO DO: convert spaces to '+'s
    return self.query

class Book:
  def __init__(self, book):
    self.book = book
    self.title = book['title']
    self.author = book['author']
    self.publisher = book['publisher']
  
  def print(self):
    print(f'    Title: {self.title}')
    print(f'    Author(s): {self.author}')
    print(f'    Publisher: {self.publisher}\n')

# UTILITIES 
def format_book(book):
  multiple_authors = isinstance(book['authors'], list)
  if multiple_authors:
    author = ', '.join(book['authors'])
  else:
    author = book['authors']
  return {
      'title': book['title'],
      'author': author,
      'publisher': book['publisher']
    }

def display_books_in_list(books):
  for (i, book) in enumerate(books, start=1):
    print(f'ID {i}')
    current_book = Book(book)
    current_book.print()

def confirm(action):
  confirm = input(f'Are you sure you want to {action}? (Enter "y"/"n")')
  if confirm == 'y':
    pass
  elif confirm == 'n':
    pass
  else:
    print('Please enter "y" or "n"')

# SEARCH 
def search():
  search_header = Header('search')
  search_header.print()

  query = input('Search for books containing the query:  ').lower()

  # TO DO: add escape key to cancel query
  results = get_search_results(query)
  display_search_results(results)

def get_search_results(query):
  '''
  Connect to the API using the requests library
  and return up to five books matching search query.
  '''
  # format query
  # TO DO: implement format query fn to handle special chars, spaces, convert case


  # construct endpoint URL
  api_prefix = 'https://www.googleapis.com/books/v1/volumes'
  api_key = 'AIzaSyBRv9nNOtXCLqu36oPqB8OsWwy5MfaCcBs'
  api_endpoint = f'{api_prefix}?q={query}&key={api_key}&maxResults=5'

  # use requests lib to fetch data from endpoint
  response = requests.get(api_endpoint)

  # if request fails, return false
  if response.status_code != 200:
    return False
  
  # convert response obj to dictionary
  response_dict = response.json()

  # create new dictionary for relevant data 
  result_list = []

  # extract from response
  results = response_dict['items']
  for record in results:
    book = record['volumeInfo']
    newBook = format_book(book)
    result_list.append(newBook)
  
  return(result_list)

def display_search_results(books):
  """
  Print entries for up to five matching books.
  Display menu with available actions.
  """
  # TO-DO include error handling if no matches found
  if len(books) == 0:
    print('Sorry, your search returned 0 books.')
  else:
    print('\nMatching Results:')
    print('------------------\n')
    display_books_in_list(books)

  search_menu = Menu(['save', 'start', 'exit'])
  search_menu.print()

    # TO DO: would you like to save another? 
    # - yes: prompt user for book id
    # - no: select new search or go home

### READING LIST ###
def save_to_reading_list(book):

  # TO DO: add validation to prevent duplicate records?
  with open('reading_list.json','r+') as file:
    # load existing data into a dict
    file_data = json.load(file)
    # join book with file_data inside reading_list 
    file_data["reading_list"].append(book)
    # sets file's current position at offset
    file.seek(0)
    # convert back to json.
    json.dump(file_data, file, indent = 4)

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
    reading_list_header = Header('reading list')
    reading_list_header.print()
    display_books_in_list(reading_list)

  reading_list_menu = Menu(['search', 'exit'])
  reading_list_menu.print()

### QUIT ###
def quit():
  quit_header = Header('quit')
  quit_header.print()
  print("Thanks for using Books on 8th!\n")

def main():
  '''
  Set up the main program.
  '''
  main_header = Header('main')
  main_header.print()
  print('\n     Welcome to Books on 8th!')
  print('     ~~~~~~~~~~~~~~~~~~~~~~~~\n')

  main_menu = Menu(['search', 'view', 'quit'])
  main_menu.print()

options_dict = {
  'search': {
    'label': 'Search for books',
    'function': search
  }, 
  'save': {
    'label': 'Save a book to my reading list',
    'function': save_to_reading_list
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


