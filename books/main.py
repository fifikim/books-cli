import json
import requests
import math

# CLASSES

# prints menu with options for current view & executes user-selected action
class Menu:
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
        print(style_output('\n\nWhat would you like to do?', 'underline'))
        for (i, element) in enumerate(self.options, start=1):
            label = self.options_dict[element]['label']
            id = style_output(i, 'header')
            print(f'{id} - {label}')
        print('\n')
        self.select()

    def select(self):
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

# prints header for current view
class Header:
    def __init__(self, name):
        self.name = name.upper()

    def print(self):
        margin = math.floor((35 - len(self.name)) / 2) * ' '
        border = '=' * 30
        border2 = '=' * 34
        heading = style_output(self.name, 'header')
        print(f'\n\n   {border}')
        print(f" {style_output(border2, 'border')}")
        print(f'={margin}{heading}{margin}=')
        print(f" {style_output(border2, 'border')}")
        print(f'   {border}\n\n')

# stores book data as object & prints formatted details
class Book:
    def __init__(self, title, author, publisher):
        self.title = title
        self.author = author
        self.publisher = publisher

    def print(self):
        title = style_output(self.title, 'title')
        print(f'    Title: {title}')
        print(f'    Author(s): {self.author}')
        print(f'    Publisher: {self.publisher}')


# SHARED UTILITIES

# validates user selection is available menu option
def validate_selection(val, list):
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

# formats books in a numbered list
def display_books(list):
    for (i, book) in enumerate(list, start=1):
        print(style_output(f'ID {i}', 'header'))
        book.print()

# applies text styling to terminal output
def style_output(string, style):
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

# displays search header & prompts user for query
def search():
    header = Header('search')
    header.print()
    # TO DO: add escape key to cancel query
    q = validate_query()
    fetched = fetch_by(q)
    display_results(fetched)

# validates search query, repeats prompt if query is blank
def validate_query():
    query = input('Search for books containing the query:  ')
    if query:
        return query
    else:
        print(style_output('Please enter a valid query.\n', 'warning'))
        validate_query()

# submits api get request & returns relevant data from response
def fetch_by(query):
    response = requests.get(
        f'https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=5').json()
    if response['totalItems'] == 0:
        return False
    search_results = (format_search_results(response))
    return search_results

# formats response data & saves as Book instance
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

# prints formatted search results & new menu selections
def display_results(results):
    if results == False:
        print(style_output('Sorry, your search returned 0 results.', 'warning'))
        menu = Menu(['new', 'view', 'exit'])
        menu.print()
    else:
        print(style_output('\nResults matching your query:\n', 'underline'))
        display_books(results)
        menu = Menu(['save', 'new', 'view', 'exit'], results)
        menu.print()

# saves selected book to reading list
def save(search_results):
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

# appends book data to reading_list.json file
def write_to_saved(book):
    with open('reading_list.json', 'r+') as file:
        file_data = json.load(file)
        file_data["reading_list"].append(book)
        file.seek(0)
        json.dump(file_data, file, indent=4)


# READING LIST VIEW

# displays reading list header & prints saved books
def view_reading_list():
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

# loads data from reading_list.json file 
def load_saved():
    with open('reading_list.json') as f:
      data = json.load(f)
      return data['reading_list']

# formats JSON strings as list of Book instances
def format_loaded(list):
    books = []
    for record in list:
        book = json.loads(record)
        books.append(Book(book['title'], book['author'], book['publisher']))
    return books


# QUIT VIEW

# displays quit header & goodbye message
def quit():
    quit_header = Header('quit')
    quit_header.print()
    print(style_output('\nThanks for using Books on 8th! Goodbye.\n', 'success'))


# HOMEPAGE VIEW

# displays homepage header & menu
def main():
    header = Header('home')
    header.print()
    print(style_output('      Welcome to Books on 8th!', 'header'))
    menu = Menu(['search', 'view', 'quit'])
    menu.print()


if __name__ == '__main__':
    main()