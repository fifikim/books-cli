import requests

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

def get_search_results(query):
  """
  Connect to the API using the requests library
  and return up to five books matching search query.
  """
  # TO DO: use regex to remove special chars from query, make lowercase
  
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
    newBook = {
      'title': book['title'],
      'author': book['authors'],
      'publisher': book['publisher']
    }
    result_list.append(newBook)
  
  return(result_list)

def display_search_results(books):
  """
  Print entries for up to five matching books.
  Display menu with available actions.
  """
  # include error handling if no matches found
  # extract info from response dictionary
  # format & print records
  if len(books) == 0:
    print('Sorry, your search returned 0 books.')
  else:
    print('\nMatching Results:\n')
    print('------------------')
    for (i, book) in enumerate(books, start=1):
      title = book['title']
      author = book['author'][0]
      publisher = book['publisher']
      print(f'Result {i}')
      print(f'    Title: {title}')
      print(f'    Author(s): {author}')
      print(f'    Publisher: {publisher}')
      print('\n')

  options = ['Save a book to my reading list', 'Start a new search', 'Exit to home']
  selection = select_from_menu(options)

  if selection == '1':
    id = input('Enter ID for book you would like to save:  ')
    index = int(id) - 1
    print(books[index])
    add_to_reading_list(books[index])
  elif selection == '2':
    search()
  elif selection == '3':
    main()

### READING LIST ###
reading_list = ['onebook', 'twobook', 'threebook', 'fourbook']

def add_to_reading_list(book):
  """
  Adds selected record to reading list.
  """
  reading_list.append(book)
  display_reading_list()

def display_reading_list():
  """
  Print records of books saved to reading list.
  """
  # include handling for empty list
  if len(reading_list) == 0:
    print('There are no books in your reading list.')
  else:
    print('\n ------------------- ')
    print('|  MY READING LIST  |')
    print(' ------------------- ')
    for (i, element) in enumerate(reading_list, start=1):
      print(f'{i} - {element}')
    print('\n')

### QUIT ###
def quit():
  print("Thanks for using Books on 8th! Goodbye.")


### UTILITIES ###
def select_from_menu(options_list): 
  """
  Reusable component to populate & print menu with available selections.
  Validates user inputted selection is permitted.
  """
  print('----------------------------')
  for (i, element) in enumerate(options_list, start=1):
    print(f'{i} - {element}')
  print('\n')

  selection = input('Please enter your selection:  ')
  
  # to-do: display error message if invalid type is entered (not int)
  # display error message if invalid selection is made
  if int(selection) not in range(1, len(options_list) + 1):
    print('Please choose a number from the selections listed.')
  else:
    return selection


### RUN PROGRAM ###
def main():
  """
  Set up the main program.
  """

  print('\n ---------------- ')
  print('|  B00KS ON 8TH  |')
  print(' ---------------- ')
  print('\nWelcome to Books on 8th! What would you like to do today?')

  options = ['Search for books', 'View my reading list', 'Quit']
  selection = select_from_menu(options)
  
  if selection == "1": 
    search()
  elif selection == "2": 
    display_reading_list()
  elif selection == "3": 
    quit()

if __name__ == '__main__': main()


