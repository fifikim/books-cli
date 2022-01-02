import json
import requests
import math


# CLASSES

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

class Book:
    '''This class handles book items.'''
    def __init__(self, id, title, author, publisher):
        self.id = id
        self.title = title
        self.author = author
        self.publisher = publisher

    def __repr__(self):
        return f"\n    Title: {self.title}\n    Author(s): {self.author}\n    Publisher: {self.publisher}"

    def print(self):
        '''prints formatted details for selected book'''
        title = style_output(self.title, 'title')
        print(f"    Title: {title}\n    Author(s): {self.author}\n    Publisher: {self.publisher}\n")

class File:  
    '''This class handles JSON files.'''
    def __init__(self, name):
        self.name = name
        self.filename = f'{name}.json'    

    def load(self):
        '''Load reading list & format JSON strings as a list of Book instances.'''
        with open(self.filename) as file:
            data = json.load(file)
            list = data['reading_list']

            books = []
            for record in list:
                book = json.loads(record)
                books.append(Book(book['id'], book['title'], book['author'], book['publisher']))
            return books

    def save(self, book):
        '''Append book data to reading list JSON file.
        
        :param book: Selected search result.
        :type book: 
        '''
        json_book = json.dumps(book.__dict__, indent=4)

        with open(self.filename, 'r+') as file:
            file_data = json.load(file)
            file_data['reading_list'].append(json_book)
            file.seek(0)
            json.dump(file_data, file, indent=4)
        print(style_output(f'\nSaved: {repr(book)}', 'success'))

    def create(self):
        '''Create new JSON file to store new reading list'''
        pass

class API_Call:
    '''This class handles calls to the GoogleBooks API.'''
    def __init__(self, query):
        self.query = query

    def fetch(self):
        '''Print "fetching" message and returns JSON search results'''
        print(f"Fetching books matching: '{self.query}'\n")
        self.return_response()

    def return_response(self):
        '''Submit API get request & return response.
                
        If server responds with status code not in 200 range: prints error message 
        with specific error code. If requests module raises exception, returns message 
        with exception. If search returns no results, returns notification.
                 
        :return: Prints search results or error message, and menu with available options. 
        :rtype: str
        '''
        try:
            response = requests.get(
        f'https://www.googleapis.com/books/v1/volumes?q={self.query}&maxResults=5')

            # Print error message if server responds with status other than 2xx 
            if not response.status_code // 100 == 2:
                self.display_error(f'Error: Failed to fetch {response}')

            # Print error message if server responds with zero results
            elif response.json()['totalItems'] == 0:
                self.display_error('Sorry, your search returned 0 results.')
            else:
                books = self.format_search_results(response.json())
                self.display_results(books)

        except requests.exceptions.RequestException as e:
            # Print error message if a serious problem occurred (timeout, connection error)
            self.display_error(f'Error: {e}') 
    
    def format_search_results(self, data):
        '''Extract relevant information from API response data & save items as Book instances.
                
        :param data: Server response body formatted as JSON object.
        :type data: 
        :return: List of Book objects representing search results.
        :rtype: list
        '''
        results = []
        for item in data['items']:
            id = item['id']
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
            result = Book(id, title, author, publisher)
            results.append(result)
        return self.display_results(results)

    def display_results(self, results):
        '''Print formatted search results & new menu options.
                    
        :param results: List of Book objects representing search results.
        :type results: list
        :return: Prints search results and menu with available options. 
        :rtype: str
        '''
        print(style_output('\nResults matching your query:\n', 'underline'))
        display_books(results)
        Menu(['save', 'new', 'view', 'exit'], results).print()

    def display_error(self, err):    
        print(style_output(err, 'warning'))
        Menu(['new', 'view', 'exit']).print()


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
        
    :param list: List of Book objects.
    :type list: list
    :return: Numbered, formatted list.
    :rtype: str
    '''
    for (i, book) in enumerate(list, start=1):
        print(style_output(f'ID {i}', 'header'))
        book.print()

def style_output(string, style):
    '''Apply text styling to terminal output.
        
    :param string: The text to stylize.
    :type string: str 
    :param style: Style corresponding to key in 'styles' dictionary.
    :type style: str 
    :return: Text with colors and/or styles applied.
    :rtype: str
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
    Header('search').print()
    prompt()

def prompt():
    '''Prompt user to input search query. Repeat prompt if user tries to enter a blank query.'''
    query = input('Search for books containing the query:  ')
    # TO DO: add escape key to cancel query
    
    if query == '':
        print(style_output('Please enter a valid query.\n', 'warning'))
        prompt()
    else:
        API_Call(query).fetch()

def save(search_results):
    '''Save selected book to reading list.
    
    :param search_results: List of Book objects representing search results.
    :type search_results: list
    '''
    selection = input('Please enter the ID of the book to save:   ')
    valid = validate_selection(selection, search_results)
    
    if valid:
        book = search_results[int(selection) - 1]
        File('reading_list').save(book)
        Menu(['another', 'new', 'view', 'exit'], search_results).print()
    else:
        print(style_output(
            f'Invalid selection. Please choose from IDs #1-{len(search_results)}.\n', 'warning'))
        save(search_results)


# READING LIST VIEW

def view_reading_list():
    '''Display reading list header & print saved books.'''
    Header('reading list').print()
    list = File('reading_list').load()

    if len(list) == 0:
        print(style_output('There are no books in your reading list.', 'warning'))
    else:
        display_books(list)
    Menu(['search', 'exit']).print()


# QUIT VIEW

def quit():
    '''Displays quit header & goodbye message.'''
    Header('quit').print()
    print(style_output('\nThanks for using Books on 8th! Goodbye.\n', 'success'))


# HOMEPAGE VIEW

def main():
    '''Displays homepage header & menu.'''
    Header('home').print()
    print(style_output('      Welcome to Books on 8th!', 'header'))
    Menu(['search', 'view', 'quit']).print()


if __name__ == '__main__':
    main()
