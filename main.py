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
        
class PageMenu:
    '''This class generates page menus and executes user selections of menu options.'''
    def __init__(self, options, results=[], type='', query='', search_query='', start_index=0):
        self.options = options
        self.results = results
        self.type = type
        self.query = query
        self.search_query = search_query
        self.start_index = start_index
        self.options_dict = {
            'search': ['Search for books', search],
            'next': ['Show next 5 results'],
            'prev': ['Show previous 5 results'],
            'new': ['Start a new search', search],
            'save': ['Save a book to my reading list', save],
            'another': ['Save another book to my reading list', save],
            'view': ['View my reading list', view_list],
            'delete_book': ['Delete a saved book', delete_book],
            'exit': ['Exit to home', main],
            'quit': ['Quit', quit]
        }

    def print(self):
        '''Print menu with available options for current view.'''
        print(style_output('\n\nWhat would you like to do?', 'underline'))
        for (i, element) in enumerate(self.options, start=1):
            label = self.options_dict[element][0]
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
            if option in ['save', 'another', 'delete_book']:
                save(self.results, self.start_index)
            elif option is 'delete_book':
                delete_book(self.results)
            elif option is 'prev':
                index = int(self.start_index) - 5
                ApiCall(self.type, self.query, self.search_query, index).fetch()
            elif option is 'next':
                index = int(self.start_index) + 5
                ApiCall(self.type, self.query, self.search_query, index).fetch()
            else:
                self.options_dict[option][1]()
        else:
            print(style_output(
                f'Invalid selection. Please choose from Options #1-{len(self.options)}.\n', 'warning'))
            self.select()

class SearchMenu:
    def __init__(self):
        self.options = {
            '1': ['Title', '+intitle:'],
            '2': ['Author', '+inauthor:'],
            '3': ['Subject', '+subject:'],
            '4': ['Keyword', '']
        }

    def print(self):
        '''Print menu with available options for current view.'''
        print(style_output(f'What would you like to search by?', 'underline'))
        for key in self.options:
            id = style_output(key, 'header')
            print(f'{id} - {self.options[key][0]}')
        print('\n')
        self.prompt_type()

    def prompt_type(self):
        '''Prompt user for selection and execute selected action.'''
        type = input('Please enter your selection:  ')
        valid = validate_selection(type, self.options)

        if valid:
            self.prompt_query(type)
        else:
            print(style_output(
                f'Invalid selection. Please choose from Options #1-{len(self.options)}.\n', 'warning'))
            self.prompt_type()
    
    def prompt_query(self, type):
        '''Prompt user to input search query. Repeat prompt if user tries to enter a blank query.'''
        search_by = self.options[type][0]
        query = input(f'Please enter the {search_by} to search:  ')
        # TO DO: add escape key to cancel query
        
        if query == '':
            print(style_output('Please enter a valid query.\n', 'warning'))
            self.prompt_query(type)
        else:
            search_query = f'{self.options[type][1]}{query}'
            ApiCall(search_by, query, search_query).fetch()

class Book:
    '''This class handles book items.'''
    def __init__(self, id, title, author, publisher):
        self.id = id
        self.title = title
        self.author = author
        self.publisher = publisher
        self.read = False

    def __repr__(self):
        return f"\n    Title: {self.title}\n    Author(s): {self.author}\n    Publisher: {self.publisher}"

    def print(self):
        '''prints formatted details for selected book'''
        title = style_output(self.title, 'title')
        print(f"    Title: {title}\n    Author(s): {self.author}\n    Publisher: {self.publisher}")

class File:  
    '''This class handles JSON files.'''
    def __init__(self, name):
        self.name = name
        self.filename = f'lists/{name}.json'   

    def display_list(self):
        '''Print formatted reading list or empty list notification.'''
        list = self.load()

        if len(list) == 0:
            print(style_output('There are no books in your reading list.', 'warning'))
        else:
            display_books(list)
        PageMenu(['search', 'delete_book', 'exit'], list).print()

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

    def check_for_dupe(self, id):
        '''Check for book with duplicate ID in reading list.

        :param id: ID of book user attempting to save.
        :type id: str
        :return True if duplicate ID exists; False if not.
        :rtype: boolean
        '''
        books = self.load()
        for book in books:
            if book.id == id:
                return True
        return False

    def delete_record(self, to_delete):
        '''Delete selected book from reading list.
        
        :param to_delete: Book record selected for deletion.
        :type to_delete: Book obj
        '''
        books = self.load()

        file_data = {}
        file_data['reading_list'] = []
        for book in books:
            if book.id is not to_delete.id:
                json_book = json.dumps(book.__dict__, indent=4)
                file_data['reading_list'].append(json_book)

        with open(self.filename, 'w') as file:
            json.dump(file_data, file, indent=4)
        print(style_output(f'"{to_delete.title}" deleted.', 'success'))

    def save(self, book):
        '''Append book data to reading list JSON file.
        
        :param book: Selected search result.
        :type book: 
        '''
        json_book = json.dumps(book.__dict__, indent=4)

        duplicate = self.check_for_dupe(book.id)
        if duplicate:
            print(style_output(f'"{book.title}" is already saved to this list.', 'warning'))
        else:
            with open(self.filename, 'r+') as file:
                file_data = json.load(file)
                file_data['reading_list'].append(json_book)
                file.seek(0)
                json.dump(file_data, file, indent=4)
            print(style_output(f'\nSaved: {repr(book)}', 'success'))

class ApiCall:
    '''This class handles calls to the GoogleBooks API.'''
    def __init__(self, type, query, search_query, start_index=0):
        self.type = type
        self.query = query
        self.search_query = search_query
        self.start_index = start_index

    def fetch(self):
        '''Print "fetching" message and returns JSON search results'''
        self.return_response()

    def return_response(self):
        '''Submit API get request & return response.
                
        If server responds with status code not in 200 range: prints error message 
        with specific error code. If requests module raises exception, returns message 
        with exception. If search returns no results, returns notification.
                 
        :return: Prints search results or error message, and menu with available options. 
        :rtype: str
        '''
        url = f'https://www.googleapis.com/books/v1/volumes?q={self.search_query}&maxResults=5&startIndex={self.start_index}'
        print(url)

        try:
            response = requests.get(url)

            # Print error message if server responds with status other than 2xx 
            if not response.status_code // 100 == 2:
                self.display_error(f'Error: Failed to fetch {response}')

            # Print error message if server responds with zero results
            elif response.json()['totalItems'] == 0:
                self.display_error('Sorry, your search returned 0 results.')
            else:
                self.format_search_results(response.json())

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
        total = data['totalItems']
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
        return self.display_results(results, total, self.start_index)

    def display_results(self, results, total, start_index):
        '''Print formatted search results & new menu options.
                    
        :param results: List of Book objects representing search results.
        :type results: list
        :return: Prints search results and menu with available options. 
        :rtype: str
        '''
        if len(results) == 1:
            print(style_output(f'\nShowing 1 result matching {self.type}: "{self.query}"\n', 'underline'))
        else:
            start = int(start_index) + 1
            end = start + len(results) - 1
            print(style_output(f'\nShowing {start} - {end} of {total} results matching {self.type}: "{self.query}"\n', 'underline'))
        display_books(results, start)

        options = ['prev', 'next', 'save', 'new', 'exit']
        if start == 1:
            options.remove('prev')
        if end == total:
            options.remove('next')
        PageMenu(options, results, self.type, self.query, self.search_query, self.start_index).print()

    def display_error(self, err):    
        print(style_output(err, 'warning'))
        PageMenu(['new', 'view', 'exit']).print()


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

def display_books(list, start_num=1):
    '''Print list of books as a numbered, formatted list.
        
    :param list: List of Book objects.
    :type list: list
    :return: Numbered, formatted list.
    :rtype: str
    '''
    for (i, book) in enumerate(list, start=start_num):
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
    SearchMenu().print()

def save(search_results, start_index):
    '''Save selected book to reading list.
    
    :param search_results: List of Book objects representing search results.
    :type search_results: list
    '''
    selection = int(input('Please enter the ID of the book to save:   '))
    
    if selection in range(start_index + 1, start_index + 6):
        index = selection - start_index - 1
        book = search_results[index]
        File('reading_list').save(book)
        PageMenu(['another', 'new', 'view', 'exit'], search_results).print()
    else:
        print(style_output(
            f'Invalid selection. Please choose from IDs #{start_index + 1} - {start_index + 5}.\n', 'warning'))
        save(search_results, start_index)


# READING LIST VIEW

def view_list():
    '''Display reading list header & print saved books.'''
    Header('reading list').print()
    File('reading_list').display_list()

def delete_book(list):
    '''Delete a book saved to a reading list.'''
    selection = input('Please enter the ID of the book to delete:   ')
    valid = validate_selection(selection, list)
    
    if valid:
        book = list[int(selection) - 1]
        confirm = input(style_output(f'\nThis will delete the record for "{book.title}". Enter "y" to confirm:  ', 'warning'))
        if confirm == 'y':
            File('reading_list').delete_record(book)
            PageMenu(['view', 'exit'], list).print()
        else:
            print('Delete cancelled.')
            PageMenu(['view', 'exit'], list).print()
    else:
        print(style_output(
            f'Invalid selection. Please choose from IDs #1-{len(list)}.\n', 'warning'))
        delete_book(list)


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
    PageMenu(['search', 'view', 'quit']).print()


if __name__ == '__main__':
    main()
