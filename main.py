import requests
import json

### SEARCH ###
def search():
  """
  Search for books by user inputted query
  """
  print('\n ---------------- ')
  print('|  SEARCH BOOKS  |')
  print(' ---------------- \n')

  query = input('Search for books containing the query:  ')
  results = get_search_results(query)
  
  display_search_results(results)

  # TO DO: 

def get_search_results(query):
  """
  Connect to the API using the requests library
  and return up to five books matching search query.
  """
  # format query
  f_query = format_query(query)

  # construct endpoint URL
  api_prefix = 'https://www.googleapis.com/books/v1/volumes'
  api_key = 'AIzaSyBRv9nNOtXCLqu36oPqB8OsWwy5MfaCcBs'
  api_endpoint = f'{api_prefix}?q={f_query}&key={api_key}&maxResults=5'

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

  options = ['Save a book to my reading list', 'Start a new search', 'Exit to home']
  selection = select_from_menu(options)

  if selection == '1':
    id = input('Enter ID for book you would like to save:  ')
    index = int(id) - 1
    add_to_reading_list(books[index])
    print(f'Saving: {books[index]}')

    # TO DO: would you like to save another? 
    # - yes: prompt user for book id
    # - no: select new search or go home

  elif selection == '2':
    search()
  elif selection == '3':
    main()

### READING LIST ###
def add_to_reading_list(book):
  """
  Adds selected record to reading list.
  """
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

def display_reading_list():
  """
  Print records of books saved to reading list.
  """
  # open JSON reading list file
  f = open('reading_list.json')

  # return JSON object as a dictionary
  data = json.load(f)

  reading_list = data['reading_list']

  # include handling for empty list
  if len(reading_list) == 0:
    print('There are no books in your reading list.')
  else:
    print('\n ---------------- ')
    print('|  READING LIST  |')
    print(' ---------------- \n')
    display_books_in_list(reading_list)

### QUIT ###
def quit():
  """
  Search for books by user inputted query
  """
  print('\n ----------------- ')
  print('|    GOOD-BYE!    |')
  print(' ----------------- \n')
  print("Thanks for using Books on 8th!\n")

### UTILITIES ###
def select_from_menu(options_list): 
  """
  Reusable component to populate & print menu with available selections.
  Validates user inputted selection is permitted.
  """
  print('----------------------------')
  for (i, element) in enumerate(options_list, start=1):
    print(f'{i} - {element}')

  selection = input('\nPlease enter your selection:  ')
  
  # to-do: display error message if invalid type is entered (not int)
  # display error message if invalid selection is made
  if int(selection) not in range(1, len(options_list) + 1):
    input('Please choose a number from the selections listed:  ')
  else:
    return selection

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

def format_query(query):
  # TO DO: use regex to remove special chars from query, make lowercase
  # TO DO: convert spaces to '+'s
  return query

def display_books_in_list(books):
  for (i, book) in enumerate(books, start=1):
    title = book['title']
    author = book['author']
    publisher = book['publisher']
    print(f'ID {i}')
    print(f'    Title: {title}')
    print(f'    Author(s): {author}')
    print(f'    Publisher: {publisher}\n')

### RUN PROGRAM ###
def main():
  """
  Set up the main program.
  """

  print('\n ---------------- ')
  print('|  B00KS ON 8TH  |')
  print(' ---------------- ')
  print('\nWelcome to Books on 8th!\n\nWhat would you like to do?')

  options = ['Search for books', 'View my reading list', 'Quit']
  selection = select_from_menu(options)
  
  if selection == "1": 
    search()
  elif selection == "2": 
    display_reading_list()
  elif selection == "3": 
    quit()

if __name__ == '__main__': main()


