import json
import requests
import math
import os
import time
import re

# These classes fetch and store data.

class Book:
    '''This class handles book items.'''
    def __init__(self, id, title, author, publisher):
        self.id = id
        self.title = title
        self.author = author
        self.publisher = publisher

    def __repr__(self):
        '''Print book details as a string.'''
        return f"\n    Title: {self.title}\n    Author(s): {self.author}\n    Publisher: {self.publisher}"

    def print(self):
        '''Prints book details as a formatted string with added emphasis on title.'''
        title = style_output(self.title, 'title')
        print(f"    Title: {title}\n    Author(s): {self.author}\n    Publisher: {self.publisher}")

class File:  
    '''This class handles JSON files.'''
    def __init__(self, name):
        self.name = f"{name.replace('_', ' ').title()}"
        self.filename = f"lists/{name.lower().replace(' ', '_')}.json"   

    def load(self):
        '''Load reading list & format JSON strings as a list of Book instances.'''
        with open(self.filename) as file:
            file_data = json.load(file)
            list = file_data['books']

            books = []
            for record in list:
                book = json.loads(record)
                books.append(Book(book['id'], book['title'], book['author'], book['publisher']))
            return books

    def load_as_list(self):
        '''Loads reading list from file and then displays associated List.'''
        list = self.load()
        List(self.name, list).display()

    def delete_record(self, to_delete):
        '''Delete selected book from reading list.
        
        :param to_delete: Book record selected for deletion.
        :type to_delete: Book obj
        '''
        books = self.load()
        file_data = {}
        file_data['books'] = []

        for book in books:
            if book.id != to_delete.id:
                json_book = json.dumps(book.__dict__, indent=4)
                file_data['books'].append(json_book)

        with open(self.filename, 'w') as file:
            json.dump(file_data, file, indent=4)

    def save(self, book):
        '''Append book data to reading list JSON file.
        
        :param book: Selected search result.
        :type book: 
        :return: True if save was successful; False if not.
        :rtype: boolean
        '''
        json_book = json.dumps(book.__dict__, indent=4)

        if self.list_contains_dupe(book.id):
            return False
        else:
            with open(self.filename, 'r+') as file:
                file_data = json.load(file)
                file_data['books'].append(json_book)
                file.seek(0)
                json.dump(file_data, file, indent=4)
            return True
    
    def delete_file(self):
        os.remove(self.filename)

    def create(self):
        '''Create a new reading list file'''
        file_data = {}
        file_data['books'] = []

        if self.list_name_taken():
            return 'duplicate'
        if self.list_name_invalid():
            return 'invalid'

        with open(self.filename, 'w') as file:
            json.dump(file_data, file, indent=4)
            return 'success'
    
    def list_contains_dupe(self, id):
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

    def list_name_taken(self):
        lists = list_all_lists()
        if self.name in lists:
            return True
        return False
        
    def list_name_invalid(self):
        return bool(re.search('[^a-zA-Z0-9\s]+$', self.name))

class ApiCall:
    '''This class handles calls to the GoogleBooks API.'''
    def __init__(self, type, query, start_index=0):
        self.type = type
        self.query = query
        self.start_index = start_index
        self.query_dict = {
            'Title': '+intitle:',
            'Author': '+inauthor:',
            'Subject': '+subject:',
            'Keyword': ''
        }

    def fetch(self):
        '''Submit API get request & return response.
                
        If server responds with status code not in 200 range: prints error message 
        with specific status code and type. If requests module raises exception, returns message 
        with type if exception is connection error or timeout. If search returns no results, returns notification.
                 
        :return: Prints search results or error message, and menu with available options. 
        :rtype: str
        '''
        search_query = f'{self.query_dict[self.type]}{self.query}'
        url = f'https://www.googleapis.com/books/v1/volumes?q={search_query}&maxResults=5&startIndex={self.start_index}'

        try:
            response = requests.get(url, timeout=5)

            # Print error message if server responds with status other than 200 .
            if not response.status_code // 100 == 2:
                self.display_error(f'{response.status_code} {response.reason}')
            
            # Print error message if server responds with zero results.
            elif response.json()['totalItems'] == 0:
                self.display_error('Sorry, your search returned 0 results.', 'no_results')
            else:
                self.format_search_results(response.json())

        # Print error message if requests raises exception. Give type if timeout or connection error.
        except requests.exceptions.Timeout or requests.exceptions.ReadTimeout or requests.exceptions.ConnectTimeout:
            self.display_error('Timed Out')
        except requests.exceptions.ConnectionError:
            self.display_error(f'Connection Error')
        except requests.exceptions.RequestException as e:
            self.display_error(f'Exception') 
    
    def display_error(self, err, type=''):    
        '''Display error returned from server & prompts user to start a new search.'''
        if type == 'no_results':
            print(style_output(f'{err}', 'warning'))
        else:
            print(style_output(f'Sorry, your search could not be completed. Please try again later or with a different query. (Error: {err})', 'warning'))
        print('\nWould you like to start a new search?')
        confirm = input('Please enter "y" to search or any other key to exit:    ')
        if confirm == 'y':
            Search().build_query()
        else:
            main()

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
        return SearchResults(results, total, self.type, self.query, self.start_index).display_results()


# These classes render headings and menus. 
#TO-DO: check for uniform spacing around menus
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
        print(f'   {border}\n')

class Menu:
    '''This class generates menus that allow user to select from available actions.'''
    def __init__(self, options, options_dict):
        self.options = options
        self.options_dict = options_dict

    def print(self):
        '''Print available options for current view.'''
        print(style_output('\n\nWhat would you like to do?', 'underline'))
        for (i, element) in enumerate(self.options, start=1):
            label = self.options_dict[element][0]
            id = style_output(i, 'header')
            print(f'{id} - {label}')
        print('\n')
        self.select()

    def select(self):
        '''Prompt user to select option and then execute selected action.'''
        selection = input('Please enter your selection:  ')
        valid = validate_selection(selection, self.options)

        if valid:
            option = self.options[int(selection) - 1]
            self.options_dict[option][1]()
        else:
            print(style_output(
                f'Invalid selection. Please choose from Options #1-{len(self.options)}.\n', 'warning'))
            return self.select()

class SelectTarget:
    '''This class generates menus that allow user to select a target to perform a given action.'''
    def __init__(self, list, item, action, start_num=1):
        self.list = list
        self.item = item
        self.action = action
        self.start_num = start_num

    def select_from_list(self):
        '''Print list of available targets and prompt user to select one option.'''
        self.show_list()
        return self.prompt()

    def show_list(self):
        '''Print menu with available options.'''
        print(style_output(f'\n\nWhich {self.item} would you like to {self.action}?', 'underline'))
        for (i, element) in enumerate(self.list, start=self.start_num):
            id = style_output(i, 'header')
            print(f'{id} - {element}')
        print('\n')    
    
    def prompt(self):
        '''Prompt user to select from list shown.'''
        num = input('Please enter your selection:  ')
        valid = validate_selection(num, self.list, self.start_num)

        if valid:
            selected = self.list[int(num) - 1]
            return selected
        else:
            print(style_output(
                f'Invalid selection. Please choose from Options #1-{len(self.list)}.\n', 'warning'))
            return self.prompt()
    
    def select_without_list(self):
        '''Prompt user for selection when options have already been printed.'''
        num = input(f'Please enter the ID of the {self.item} you would like to {self.action}:  ')
        valid = validate_selection(num, self.list, self.start_num)

        if valid:
            index = int(num) - int(self.start_num)
            selected = self.list[index]
            return selected
        else:
            end_num = int(self.start_num) + len(self.list) - 1
            print(style_output(
                f'Invalid selection. Please choose from IDs #{self.start_num} - {end_num}.\n', 'warning'))
            return self.select_without_list()


# These classes handle user navigation and lookups.

class Search:
    '''This class performs a new search.'''
    def __init__(self):
        self.options = ['Title', 'Author', 'Subject', 'Keyword', 'Cancel search']

    def build_query(self):

        type = self.get_type()
        term = self.get_term(type)
        ApiCall(type, term).fetch()

    def get_type(self):
        '''Prompt user to select a type of search.'''
        search_type = SelectTarget(self.options, 'type of search', 'perform').select_from_list()
        if search_type == 'Cancel search and exit to home':
            main()
        else:
            return search_type

    def get_term(self, type):
        '''Prompt user to enter search term(s).'''
        term = input(f'Please enter the {type.lower()} to search:  ')
        
        if term == '':
            print(style_output('Please enter a valid query.\n', 'warning'))
            self.get_term(type)
        else:
            return term

class SearchResults:
    '''This class displays search results & handles relevant actions.'''
    def __init__(self, results, total, type, query, start_index=0):
        self.results = results
        self.total = total
        self.type = type
        self.query = query
        self.start_index = start_index
        self.first = int(self.start_index) + 1
        self.last = self.first + len(self.results) - 1
        self.options_dict = {
            'prev': ['Show previous 5 results', self.prev],
            'next': ['Show next 5 results', self.next],
            'save': ['Save a book to my reading lists', self.save],
            'new': ['Start a new search', Search().build_query],
            'exit': ['Exit to home', main],
        }

    def menu(self):
        '''Generate menu options depending on search results.'''
        options = ['prev', 'next', 'save', 'new', 'exit']
        if self.first == 1:
            options.remove('prev')
        if self.last == self.total:
            options.remove('next')
        Menu(options, self.options_dict).print()

    def next(self):
        '''Fetch next page of search results.'''
        ApiCall(self.type, self.query, self.last).fetch()
    
    def prev(self):
        '''Fetch previous page of search results.'''
        new_start = int(self.start_index) - 5
        ApiCall(self.type, self.query, new_start).fetch()
    
    def display_results(self):
        '''Print formatted search results & new menu options.
                    
        :param results: List of Book objects representing search results.
        :type results: list
        :return: Prints search results and menu with available options. 
        :rtype: str
        '''
        if len(self.results) == 1:
            print(style_output(f'\nShowing 1 result matching {self.type.lower()}: "{self.query}"\n', 'underline'))
        else:
            print(style_output(f'\nShowing {self.first} - {self.last} of {self.total} results matching {self.type}: "{self.query}"\n', 'underline'))
        display_books(self.results, self.first)
        self.menu()

    def save(self):
        '''Save selected book to reading list.
        
        :param search_results: List of Book objects representing search results.
        :type search_results: list
        '''
        target_book = SelectTarget(self.results, 'book', 'save', self.first).select_without_list()
        target_list = SelectTarget(ListsMain().lists, 'list', 'save to').select_from_list()
        saved_book = File(target_list).save(target_book)
        
        if saved_book:
            print(style_output(f'Saved to "{target_list}": {repr(target_book)}', 'success'))
            time.sleep(1)
        else:
            print(style_output(f'Unable to save to "{target_list}": {target_book.title} is already saved to this list.', 'warning'))
            time.sleep(1)
        self.menu()

class ListsMain:
    '''This class handles navigation from the main Reading Lists page.'''
    def __init__(self):
        self.lists = list_all_lists()
        self.options = ['view', 'new_list', 'exit']
        self.options_dict = {
            'view': ['View a list', self.view_list],
            'new_list': ['Create a new list', self.create_list],
            'exit': ['Exit to home', main],
        }

    def menu(self):
        '''Print Reading Lists menu.'''
        Menu(self.options, self.options_dict).print()

    def view_list(self):
        '''Prompt user to select list and then load associated file.'''
        list = SelectTarget(list_all_lists(), 'list', 'view').select_from_list()
        File(list).load_as_list()

    def create_list(self):
        name = input('Please enter a name for the new list:    ').strip()
        if name:
            status = File(name).create()

            if status == 'success':
                print(style_output(f'New list "{name}" created.', 'success'))
                time.sleep(1)
                self.menu()
            elif status == 'duplicate':
                print(style_output(f'List could not be created: "{name}" already exists.\n', 'warning'))
                self.create_list()
            elif status == 'invalid':
                print(style_output(f'List could not be created: "{name}" contains invalid characters. (Only alphanumeric characters and spaces allowed.)\n', 'warning'))
                self.create_list()
        else: 
            return self.create_list()

class List:
    '''This class displays a selected reading list & handles relevant actions.'''
    def __init__(self, name, booklist):
        self.name = name
        self.booklist = booklist
        self.options_dict = {
            'delete_book': ['Delete a book from this list', self.delete_book],
            'move_book': ['Move a book to another list', self.move_book],
            'delete_list': ['Delete this list', self.delete_list],
            'view_another': ['View another list', ListsMain().view_list],
            'new_list': ['Create a new list', ListsMain().create_list],
            'exit': ['Exit to home', main],
        }

    def menu(self):
        options = ['delete_book', 'move_book', 'delete_list', 'view_another', 'new_list', 'exit']
        if self.name == 'Reading List':
            options.remove('delete_list')
        if not self.booklist:
            options.remove('move_book')
            options.remove('delete_book')
        
        Menu(options, self.options_dict).print()

    def display(self):
        '''Print reading list & menu of relevant actions.'''
        if len(self.booklist) == 0:
            print(style_output(f'\nThere are currently no books in "{self.name}".', 'warning'))
            options = ['delete_list', 'view_another', 'new_list', 'exit']
            Menu(options, self.options_dict).print() 
        else:
            print(style_output(f'\nShowing books in "{self.name}":\n', 'underline'))
            display_books(self.booklist)
            options = ['delete_book', 'move_book', 'delete_list', 'view_another', 'new_list', 'exit']
            Menu(options, self.options_dict).print() 

    def move_book(self):
        '''Move a book to a different reading list.'''
        target_book = SelectTarget(self.booklist, 'book', 'move').select_without_list()
        target_list = SelectTarget(ListsMain().lists, 'list', 'move to').select_from_list()

        saved_book = File(target_list).save(target_book)
        if saved_book:
            File(self.name).delete_record(target_book)
            print(style_output(f'\nMoved to "{target_list}": {repr(target_book)}', 'success'))
            print(f'Refreshing "{self.name}"...')
            time.sleep(1)
            File(self.name).load_as_list()
        else:
            print(style_output(f'Unable to move to "{target_list}": {target_book.title} is already saved to this list.', 'warning'))
            options = ['delete_book', 'move_book', 'delete_list', 'view_another', 'new_list', 'exit']
            Menu(options, self.options_dict).print() 

    def delete_book(self):
        '''Delete a book saved to a reading list.'''
        book = SelectTarget(self.booklist, 'book', 'delete').select_without_list()
        confirmed = self.confirm_delete(book.title)
        if confirmed:
            File(self.name).delete_record(book)
            print(style_output(f'\nDeleted from "{self.name}": {repr(book)}', 'warning'))
            print(f'Refreshing "{self.name}"...')
            time.sleep(1)
            File(self.name).load_as_list()
        else: 
            print('Delete cancelled.\n')
            self.menu()
        
    def delete_list(self):
        '''Delete JSON file of selected list'''
        confirmed = self.confirm_delete(self.name)
        if confirmed:
            File(self.name).delete_file()
            print(style_output(f'List "{self.name}" deleted.', 'warning'))
            time.sleep(1)
            ListsMain().menu()
        else:
            print('Delete cancelled.\n')
            self.menu()

    def confirm_delete(self, item):
        print(style_output(f'\nAre you sure you want to delete "{item}"? This action cannot be undone.', 'warning'))
        confirm = input('Please enter "y" to confirm, or press any other key to cancel:    ')
        if confirm == 'y':
            return True
        return False


# These are shared utility functions.

def validate_selection(val, list, start_num=1):
    '''Validate that a user selection is an available menu option.
    
    :param val: User-selected input.
    :type val: str
    :param list: List of available menu options.
    :type list: list
    :return: True if selection is valid, else False.
    :rtype: boolean
    '''
    max = start_num + len(list)
    if val:
        try:
            num = int(val)
            if num in range(start_num, (max)):
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

def list_all_lists():
    '''Return all reading list files as formatted list of names.'''
    list_names = os.listdir('./lists')
    clean_list = []

    for list in list_names:
        name = list.split('.')[0].replace("_", " ")
        clean_list.append(name)
    return clean_list


# These functions print headers and the main navigation menus.

def search_landing():
    '''Display search header & user_selections user for query.'''
    Header('search').print()
    Search().build_query()

def lists_landing():
    '''Display reading list header & print saved books.'''
    Header('my reading lists').print()
    ListsMain().menu()

def quit_landing():
    '''Displays quit header & goodbye message.'''
    Header('quit').print()
    print(style_output('\nThanks for using Books on 8th! Goodbye.\n', 'success'))

def main():
    '''Displays homepage header & menu.'''
    Header('home').print()
    print(style_output('\n      Welcome to Books on 8th!', 'header'))
    options = ['search', 'list', 'quit']
    options_dict = {
            'search': ['Search for books', search_landing],
            'list': ['Go to my reading lists', lists_landing],
            'quit': ['Quit', quit_landing],
        }
    Menu(options, options_dict).print()


if __name__ == '__main__':
    main()
