import json
import requests
import math

# CLASSES

class Menu:
    '''This class generates page menus and executes user selections of menu options.'''
    def __init__(self, options, results=[]):
        self.options = options
        self.results = results
        self.options_dict = {
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
                'function': view_reading_list
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

    def print(self):
        '''Print menu with available options for current view.'''
        print(style_output('\n\nWhat would you like to do?', 'underline'))
        for (i, element) in enumerate(self.options, start=1):
            label = self.options_dict[element]['label']
            id = style_output(i, 'header')
            print(f'{id} - {label}')
        print('\n')
        self.select()

    def select(self):
        '''Prompt user for selection and execute selected action.'''
        selection = input('Please enter your selection:  ')
        valid = validate_selection(selection, self.options)

        if valid:
            option = self.options[int(selection) - 1]
            if option == 'save' or option == 'another':
                save(self.results)
            else:
                self.options_dict[option]['function']()
        else:
            print(style_output(
                f'Invalid selection. Please choose from Options #1-{len(self.options)}.\n', 'warning'))
            self.select()

class Header:
    '''This class generates decorative page headers.'''
    def __init__(self, name):
        self.name = name.upper()

    def print(self):
        '''Print page header for current view.'''
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
    '''This class handles book items.'''
    def __init__(self, title, author, publisher):
        self.title = title
        self.author = author
        self.publisher = publisher

    def print(self):
        '''prints formatted details for selected book'''
        title = style_output(self.title, 'title')
        print(f'    Title: {title}')
        print(f'    Author(s): {self.author}')
        print(f'    Publisher: {self.publisher}')

    def write_to_saved(self):
        '''saves selected book to reading list'''
        pass

class List:
    '''This class handles lists of books.'''
    def __init__(self, name):
        self.name = name

# SHARED UTILITIES

def validate_selection(val, list):
    '''Validate that a user selection is an available menu option.
    
    :param val: User-selected input.
    :type val: str
    :param list: List of available menu options.
    :type list: list
    :return: True if selection is valid, else False.
    :rtype: boolean
    '''
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

def display_books(list):
    '''Print list of books as a numbered, formatted list.
        
    :param val: 
    :type val: 
    :param list: 
    :type list:
    :return: 
    :rtype: 
    '''
    for (i, book) in enumerate(list, start=1):
        print(style_output(f'ID {i}', 'header'))
        book.print()

def style_output(string, style):
    '''Apply text styling to terminal output.
        
    :param val: 
    :type val: 
    :param list: 
    :type list: 
    :return: 
    :rtype: 
    '''
    reset = '\033[0;0m'
    styles = {
        'header': '\033[1;36m',
        'underline': '\033[4;33m',
        'border': '\033[0;35m',
        'title': '\033[3;36m',
        'success': '\033[1;32m',
        'warning': '\033[1;31m',
    }
    return f"{styles[style]}{string}{reset}"


# SEARCH VIEW

def search():
    '''Display search header & prompts user for query.'''
    header = Header('search')
    header.print()
    # TO DO: add escape key to cancel query
    q = prompt_query()
    fetched = fetch_by(q)
    display_results(fetched)

def prompt_query():
    '''Prompt user to input search query.
    
    Repeat prompt if user tries to enter a blank query.
        
    :return: User-inputted query term(s).
    :rtype: str
    '''
    query = input('Search for books containing the query:  ')
    # TO-DO: refactor if/else to try/except so that this function has one return type
    if query:
        return query
    else:
        print(style_output('Please enter a valid query.\n', 'warning'))
        prompt_query()

def fetch_by(query):
    '''Submit API get request & return response.
            
    :param query: User-submitted search query.
    :type query: str
    :return: List of Book class objects representing search results. 
    :rtype: list
    '''
    response = requests.get(
        f'https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=5').json()
    if response['totalItems'] == 0:
        return []
    else:
        return format_search_results(response)

def format_search_results(data):
    '''Extract relevant information from API response data & save items as Book instances.
               
    :param data: User-submitted search query.
    :type data: str
    :return: List of Book objects representing search results. 
    :rtype: list
    '''
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
    '''Print formatted search results & new menu options.
                   
    :param results: List of Book objects representing search results.
    :type results: list
    :return: List of Book class instances representing search results. 
    :rtype: list
    '''
    if results == []:
        print(style_output('Sorry, your search returned 0 results.', 'warning'))
        menu = Menu(['new', 'view', 'exit'])
        menu.print()
    else:
        print(style_output('\nResults matching your query:\n', 'underline'))
        display_books(results)
        menu = Menu(['save', 'new', 'view', 'exit'], results)
        menu.print()

def save(search_results):
    '''Save selected book to reading list.
    
    :param search_results: List of Book objects representing search results.
    :type search_results: list
    '''
    selection = input('Please enter the ID of the book to save:   ')
    valid = validate_selection(selection, search_results)
    if valid:
        selected_book = json.dumps(
            search_results[int(selection) - 1].__dict__, indent=4)
        write_to_saved(selected_book)
        print(style_output(f'Saved: {selected_book}', 'success'))
        menu = Menu(['another', 'new', 'view', 'exit'], search_results)
        menu.print()
    else:
        print(style_output(
            f'Invalid selection. Please choose from IDs #1-{len(search_results)}.\n', 'warning'))
        save(search_results)

def write_to_saved(book):
    '''Append book data to reading_list.json file.
        
    :param book: Selected search result.
    :type book: 
    '''
    with open('reading_list.json', 'r+') as file:
        file_data = json.load(file)
        file_data["reading_list"].append(book)
        file.seek(0)
        json.dump(file_data, file, indent=4)

# READING LIST VIEW

def view_reading_list():
    '''Display reading list header & print saved books.'''
    header = Header('reading list')
    header.print()
    list = load_saved()
    reading_list = format_loaded(list)
    if len(reading_list) == 0:
        print(style_output('There are no books in your reading list.', 'warning'))
    else:
        display_books(reading_list)
    menu = Menu(['search', 'exit'])
    menu.print()

def load_saved():
    '''Load data from reading_list.json file.'''
    with open('reading_list.json') as f:
      data = json.load(f)
      return data['reading_list']

def format_loaded(list):
    '''Format JSON strings as a list of Book instances.'''
    books = []
    for record in list:
        book = json.loads(record)
        books.append(Book(book['title'], book['author'], book['publisher']))
    return books


# QUIT VIEW

def quit():
    '''Displays quit header & goodbye message.'''
    quit_header = Header('quit')
    quit_header.print()
    print(style_output('\nThanks for using Books on 8th! Goodbye.\n', 'success'))


# HOMEPAGE VIEW

def main():
    '''Displays homepage header & menu.'''
    header = Header('home')
    header.print()
    print(style_output('      Welcome to Books on 8th!', 'header'))
    menu = Menu(['search', 'view', 'quit'])
    menu.print()


if __name__ == '__main__':
    main()
