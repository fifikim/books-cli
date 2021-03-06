<h1 align="center">Books on 8th</h1>

<div>
<p align="center"> A command line application utilizing Google Books API. <br> 
Search for books and save selections to a reading list.
</p>

<p align="center">
  <a href="" rel="noopener">
  <img src="books.png" alt="Project preview" height="400"></a></br>
</p>
</div>

## Table of Contents

- [Getting Started](#getting_started)
- [Testing](#testing)
- [Usage](#usage)
- [Process: Revisions](#revision)
  - [Day One](#revision-day-one)
  - [Day Two](#revision-day-two)
  - [Day Three](#revision-day-three)
  - [Day Four](#revision-day-four)
- [Process: Inital Submission](#initial-sub)
  - [Day One](#day-one)
  - [Day Two](#day-two)
  - [Day Three](#day-three)
  - [Day Four](#day-four)
- [Future Implementation](#future)
- [Author](#author)
- [Acknowledgments](#acknowledgments)
<br><br>

## Getting Started <a name = "getting_started"></a>

### Installing 

Clone this repo from the terminal:
```
git clone https://github.com/fifikim/books-cli.git
```

cd to program directory & install dependencies:
```
pipenv install --dev
```

Launch the program:
```
pipenv run python main.py
```
<br>

## Testing <a name = "testing"></a>

Run tests:
```
pipenv run python tests.py
```
<br>

## Usage <a name="usage"></a>

### Features
- Search for books by Title, Author, Subject, or Keyword.
- View 5 books at a time with paginated search results. 
- Create custom reading lists to store saved books.
- Manage your reading lists by deleting or moving saved books.
<br> 

### Navigation

#### Home page <br>
  1. Search for books 
  2. View your reading list 
  3. Quit: exit application

#### Search page - perform search and view results <br>
  1. Show previous page of results
  1. Show next page of results
  1. Save selected books
  2. Start a new search
  3. View your reading lists
  4. Exit to home

#### Reading Lists page - manage your reading lists <br>
  1. View a reading list
  2. Create a new list
  2. Exit to home

#### List page - view your saved books <br>
  1. Delete a saved book
  2. Move a book to another list
  2. Delete list
  2. View another list
  2. Create a new list
  2. Exit to home
<br><br>


## Process: Revision (Second Round) <a name = "revision"></a>

The following are my responses to the questions posed by my reviewer, as well my initial plan for how I'll proceed with this revision.

### 1. Classes: 

  > Can you think of any other classes you could introduce to cover some of the other functions? How did you decide what to include in the classes you created? A case might be made to include `write_to_saved()` in the `Book` class, or possibly to create a `List` or `File` class to handle saving. How would you approach something like that?

  - My response: After the first day of my initial attempt, I noticed I had a lot of duplicate lines of code and realized that I'd neglected to incorporate classes. Once I set out to refactor my app to take a more OOP-guided approach, I decided what to include in my classes by figuring out where I could DRY my program by reusing code blocks. <br>
  - Plan: I love the suggestions of a `write_to_saved()` method and a `List` class! I'll add these, and look for other functions in the code that can be refactored as class methods.

### 2. Edge cases:

  > You've done a good job of handling edge cases and 'bad' user inputs, but what about some other potential problem states?What happens if the API is down or returns an error? What if the API takes a little while to respond, and doesn't return any response immediately? How would you handle something like that in `fetch_by()`?

  - My response: I've always created API error handling when I've built full-stack apps in JavaScript, but for some reason I completely forgot to do that here. <br>
  - Plan: Wrap my API calls in try/except blocks that return custom error messages to the user according to the type of error response returned by the server. 

### 3. Type signature:

  > Along those same lines, the type signature of `fetch_by()` is a little strange ??? when called, it either returns a list of book objects, or a boolean value. While it's perfectly legal with a dynamic language like Python, it wouldn't compile in a statically typed language like TypeScript or Java. Can you think of why something like that might also be confusing to a different developer on the project?

  - My response: I see now how this function is behaving wonky by returning two different types, and how it would be confusing to another developer on the project trying to understand the role of the function by examining its inputs and output. <br>
  - Plan: Refactor `fetch_by()` so that it returns either a list of book objects or an empty list. Then refactor the functions that invoke `fetch_by()` to check if it returns an empty list, rather than `False`. I think I should also include replace my function comments with proper docstrings, not just to make my code easier to read by other developers, but also to prevent me from making this kind of mistake again.

### 4. Tests:

  > Have you written any tests before that use mocks? Typically, it's a good idea to mock things like API calls or database transactions in unit tests ??? do you have any thoughts around that? Why might it be problematic to hit a live API in your automated tests?

  - My response: I haven't written tests with mocks before, but I can see how they'd be useful at isolating a program's code to prevent any external dependencies from introducing variables that might interfere with accurate test outcomes. In the case of an API, this could be because the server is down, or the API hasn't been fully built yet. I also see the value of mocking API calls if cost of transactions was a factor. For db transactions, mocking seems useful as a way to avoid potential corruption of a database that your program needs to run. <br>
  - Plan: Create mocks to test functions that make API calls. 

### 5. Additional features:

  > Finally, what are some features that you would add for another iteration of the app? As a user, I might next request the ability to remove items from the saved list.

  - My response: The ability to delete entries from the reading list was one I thought would be useful, too! As I was testing my app, I kept coming up with features that I would want to implement and I had to keep reminding myself that I wasn't permitted to add extra features in my initial submission. <br>
  - Plan: I don't know yet how many of these I'll be able to complete given time constraints, but below is a list of features I'd like to add, grouped by page:
    - Home:
      - ~~Log in / log out~~ 
      - ~~Create a new account~~ -> decided multiple user accounts weren't necessary since all data is saved to a local machine. 
    - Search:
      - ??? View more results
      - ??? Specify type of search (author, title, subject, keyword)
      - ??? Choose where to save (existing/new list)
    - Reading List:
      - ??? Create a new list
      - ??? Delete an existing list
      - ??? Delete an item in a list
      - ??? Prevent user from saving duplicate items (Add ID property to book class)
      - Mark item as read (future)
      - Show list of read items (future)
    - Quit:
      - ~~Confirm quit~~ -> implemented this, then decided I preferred UX without

### 6. Commits:

  > I would like to see some more descriptive PR titles and descriptions, and multiple commits with messages like 'update readme' could probably be squashed into one. 

  - My response: ????????????????? I made a ton of really nitpicky little edits to my README file from the github website before I realized that all of these saves were littering my commit history with identical commits.<br>
  - Plan: Don't update my README from the browser! Approach naming pull requests & writing commit messages with the same level of descriptiveness that I try to use when naming variables and functions.
<br><br>

### Revision - Day One <a name = "revision - day-one"></a>
Goals:
  - Create outline of reviewer feedback and proposed next steps
  - Start refactoring suggested edits and pseudocoding new features

Wins: 
  - ??? Defined goals and tasks for revision process
  - ??? Created new classes & methods to further modularize and streamline code
  - ??? Implemented error handling for API calls (non 200-range status codes, timeouts, connection errors)
  - ??? Converted existing comments to docstrings -- noticed that declaring the types of inputs and returns is definitely making it easier to refactor existing code

Blockers:
  - ??? Need to do research tomorrow about best practices for creating classes. I'm uncertain whether or not I'm going too far in my refactoring functions as class methods.
  - ??? Off to a slow start today due to the holiday.
<br><br>

### Revision - Day Two <a name = "revision - day-two"></a>
Goals:
  - Begin implementing additional features

Wins: 
  - ??? Added validation to prevent duplicate books saved to a reading list.
  - ??? Added feature allowing users to delete books from a reading list.
  - ??? Added feature allowing users to choose type of search to perform (title, author, subject, keyword).
  - ??? Added feature that paginates search results, allowing users to view all results by viewing next/previous page.

Blockers:
  - ??? Code is a mess! I know I'm introducing lots of lines of duplicate code right now (like replicating my PageMenu and SearchMenu classes instead of extending a Menu base class), but my logic right now is that it'll be simpler/faster to implement the new features and then see where I can streamline later.
  - ??? Struggled to implement features that involve manipulating existing lists without corrupting files. Decided to take a break from this to work on other features -- will start up again tomorrow with fresh eyes.
  - ??? Wondering how I can store data like most recent search results & current index in the app so I don't have to keep passing multiple params between the Menu class. 
  - ??? Confused about why the GoogleBooks API returns varying # of totalItems when I send identical calls multiple times. For example, when user flips through paginated search results, the heading displayed changes from 'Showing 1-5 of 426 results' to 'Showing 6-10 of 377 results'.
<br><br>

### Revision - Day Three <a name = "revision - day-three"></a>
Goals:
  - Continue implementing additional features.
  - Clean up new code & look for ways to minimize duplication. I think I need to look at how my Menu classes are structured bc this is where a lot of the messiness currently originates. Probably need to break up the PageMenu class into different Menu classes that manage each page's respective actions.

Wins:
  - ???  I completely refactored my and restructured my classes to make sure relevant methods are grouped together and have access to the data that they need. Looks much tidier to me.
  - ???  Starting to wrap up new features.

Blockers:
  - ??? It took me all day to complete this refactor... it felt like every time I made a change to how one of part of my code was structured, every other part of my app broke. This demonstrated to me the fact that the new features I added were not decoupled enough.
<br><br>
### Revision - Day Four <a name = "revision - day-four"></a>

Goals:
- Finish debugging additional features.
- Begin testing new features & creating mocks to test API calls.
- Realized that my API error messages are not very user-friendly. Want to replace these with more detailed, less technical messages.

Wins:
  - ??? Added tests mocking my API calls. 
  - ??? Debugging complete. Fixed a bug that had been bothering me since yesterday (selection menu was using a recursive call to prompt user for new selection if invalid selection was entered -- I needed to return the recursive call in order to pass the input after an unsuccessful input was entered.)
  - ??? Happy with the amount of new features. Decided it wasn't important to add additional accounts since all data is being saved to a local machine. 
  - ??? Added more validation to prevent bad user inputs in new features & to auto-generate menu options depending on contents of lists/search resutls.

Blockers:
  - ??? Took me forever to create tests for my API calls. Spent all night reading tutorials on mocks but couldn't get them working on my code -- eventually decided that the issue might not be my tests but the way my program was written. Wound up refactoring my code again to further separate operations relating to the API. When I parsed out the fetch request into its own class method, I was finally able to get these tests working.
  - I also attempted to mock std.output to test my `print_header` function but was unsuccessful -- not sure why.

<br><br>
## Process: Initial Submission (First Round) <a name = "intial-sub"></a>

I decided to build this app in my weaker language of the two that I practice so far. I've just graduated a bootcamp concentrating on JavaScript & JS frameworks, so I thought this would be a great opportunity to refresh my novice/rusty Python skills and demonstrate my range as a developer.

I had a lot of research to do! Since I'm self-taught in Python, this project required quite a few skills that I'd never attempted in this language (such as sending api calls & writing tests). 

I wanted to avoid relying on libraries, apart from built-in modules and those explicitly permitted in the instructions (which stated we could use libraries to parse JSON & send API requests). 

Before I got started, I spent half a day researching approaches to building Python CLI's. Many examples I found relied heavily on dependencies, until I found a blog about building a simple command line weather forecaster. I built <a href='https://www.github.com/fifikim/weather-cli'>this weather app</a> to get a sense of my process and then went to work on this Books CLI.

### First Draft - Day One <a name = "day-one"></a>
- Goals:
  - Create kanban board with user stories to guide feature implementation
  - Pseudocode a skeleton of the app & then write each function

- Wins: 
  - ??? Built a working (buggy) version of the full program with decent UI. 
  - ??? Figured out how to save reading list to a local json file so that data persists after app exits.

- Blockers:
  - ???? Python feeling very foreign & I'm fighting constant urge to hit the semicolon key.
  - ??? Have never written a test in Python (only Mocha/Chai for JS) - need to research tomorrow.
  - ??? Unsure how to handle invalid menu selections & queries.

### First Draft - Day Two <a name = "day-two"></a>
- Goals:
  - Work on blockers from yesterday - testing, special characters
  - Improve UX: app should only exit when user decides to quit 
  - Look into ways to reduce coupling: ORM/encapsulation
  - Modularize components for reusability & SOC 
  - Break apart fns that aren't following SRP
  - Create classes -- whoops!!!! Edit book & menu fns to use classes & class methods

- Wins:
  - ??? Code feels much less redundant after creating classes & methods.
  - ??? Better user flow, fewer unexpected terminations/dead ends.
  - ??? Took some effort but was able to convert reading list & search results back and forth from JSON format to a list of Book class instances.

- Blockers:
  - ??? Took a long time to switch from functional to OOP mindset. Not sure that I'm there yet.
  - ??? Unsure how to let user cancel out of input prompt without exiting program.
  - ???? Wasn't able to start testing today -- more research needed on this topic.

### First Draft - Day Three <a name = "day-three"></a>
- Goals:
  - Create tests
  - Implement try/except blocks to catch invalid user input
  - Keep looking for ways to DRY code, separate concerns, & decouple components

- Wins:
  - ??? Refactored code to remove all global variables 
  - ??? Validation handles invalid/blank input for menu selection & search queries
  - ??? Learned how to color output to the terminal w/o using additional libraries. Happier with UI.
  - ??? Created tests to check fns that return 

- Blockers:
  - ??? Not sure yet how to write tests that check terminal output - need to read up on unittest.mock
  - ??? Realized that program won't run on Python 2, I think due to use of f-strings. Could convert all formatting to use string concatenation, but want to research building executable stand-alone apps to run on Mac/Unix & Windows. 

### First Draft - Day Four <a name = "day-four"></a>
- Goals:
  - Create tests that mock print() and input()
  - Figure out how to turn script into executable stand-alone app 

- Wins:
  - ??? Finished README file w/ preview gif & instructions
  - ??? Figured out how to use pipenv to package dependencies with my github repo. Hopefully I did it right! ????

- Blockers:
  - ??? Spent a lot of today working on the tic-tac-toe code review, and wasn't able to do more research on testing mocks. Hoping I have the opportunity to submit more thorough tests with my revision of this project.
<br><br>

## Future Implementation <a name = "future"></a>

- Add a Book page view displaying extended details about a selected book
- Allow user to mark a saved book as read, and view a list of all saved books
- Allow user to save personal notes & rating to saved books.
- Create additional tests to ensure output() functions are working correctly
<br><br>

## Author <a name = "author"></a>

Sophia Kim <br/>
mail@fifikim.com <br/>
<a href="https://www.fifikim.com">Portfolio</a> 
<a href="https://www.linkedin.com/in/fifikim">LinkedIn</a> 
<br><br>


## Acknowledgements <a name = "acknowledgements"></a>

Books and online references:
- Clean Python, Sunil Kapil, Apress
- Python Cookbook, David Beazley & Brian K. Jones, O'Reilly
- <a href='https://realpython.com/python-mock-library/'>Understanding the Python Mocking Library</a>
- <a href='https://realpython.com/testing-third-party-apis-with-mocks/'>Mocking External APIs</a>
- <a href='https://docs.python.org/3/library/unittest.html'>Unittest</a>
- <a href='https://www.codecademy.com/courses/learn-intermediate-python-3/lessons/int-python-unit-testing/'>More on Testing</a> (subscription required)
- <a href='https://stackabuse.com/how-to-print-colored-text-in-python/'>Coloring terminal output</a>
- <a href='https://realpython.com/python-json/'>Encoding/decoding JSON to/from custom Python objects</a>
- <a href='https://realpython.com/pipenv-guide/'>Packaging Python projects with pipenv</a>
