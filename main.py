import requests

### HOME SCREEN ###
def display_home():
  """
  Print the welcome message upon starting app.
  Display menu with available actions.
  """
  # - search for books
  # - display reading list
  # - quit
  pass


### SEARCH ###
def search():
  """
  Search for books by user inputted query
  """
  # display menu: 
  # - search by title
  # - search by author name
  # - search by subject
  # - search by any
  # - exit to home screen
  # if input != x, save selection to type, else return home
  # prompt user to enter query
  # search for books by query, type
  # display search results
  pass

def get_search_results():
  """
  Connect to the API using the requests library
  and return up to five books matching search query.
  """
  # use regex to remove special chars from query, make lowercase
  # construct endpoint URL
  # use requests lib to fetch data from endpoint
  # if request fails, return false
  # convert response obj to dictionary
  # create new dictionary for relevant data & extract from response
  pass

def display_search_results():
  """
  Print entries for up to five matching books.
  Display menu with available actions.
  """
  # include error handling if no matches found
  # extract info from response dictionary
  # format & print records
  # display menu:
  # - save a book (then prompt # 1 - 5)
  # - new search
  # - exit to home screen
  pass


### READING LIST ###
def add_to_reading_list():
  """
  Adds selected record to reading list.
  """
  pass

def display_reading_list():
  """
  Print records of books saved to reading list.
  """
  # include handling for empty list
  pass


### QUIT ###
def quit():
  # print goodbye & exit app
  pass


### UTILITIES ###
def menu_populate(): 
  """
  Reusable component to populate & print menu
  with available selections.
  """
  pass

def menu_select():
  """
  Validates user inputted selection is permitted.
  """
  # print error message & prompt for new selection
  pass


### RUN PROGRAM ###
def main():
  """
  Set up the main program.
  """
  # display_home
  # if input == 1: search
  # elif input == 2: display_reading_list
  # elif input == 3: quit
  # else: menu fn should display error message
  pass

if __name__ == '__main__': main()