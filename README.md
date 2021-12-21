<h1 align="center">Books on 8th</h1>

<div>
<p align="center"> A command line application utilizing Google Books API. <br> 
Search for books and save selections to a reading list.
</p>

<p align="center">
  <a href="" rel="noopener">
  <img src="books3.gif" alt="Project preview"></a></br>
</p>
</div>

## Table of Contents

- [Getting Started](#getting_started)
- [Testing](#testing)
- [Usage](#usage)
- [Process](#process)
  - [Day One](#day-one)
  - [Day Two](#day-two)
  - [Day Three](#day-three)
  - [Day Four](#day-four)
- [Future Implementation](#future)
- [Author](#author)
- [Acknowledgments](#acknowledgments)


## Getting Started <a name = "getting_started"></a>

### Prerequisites 

This app requires Python3.

### Installing 

Clone this repo from the terminal:
```
git clone https://github.com/fifikim/books-cli.git
```

cd to program directory & install setup file & dependencies:
```
python3 setup.py install
```

Launch the program:
```
python3 books/main.py
```

## Testing <a name = "testing"></a>

Run tests:

```
python3 tests.py
```

## Usage <a name="usage"></a>

- Search for books and receive up to 5 matching results at a time. 
- Save search results to your reading list to view later.

### Navigation
from Home page:
  1. Search for books 
  2. View your reading list 
  3. Quit - exit application

Search page:
  View search results and:
  1. Save selected books
  2. Start a new search
  3. View your reading list
  4. Exit to home

Reading List page:
  View your saved books and:
  1. Search
  2. Exit to home

## Process <a name = "process"></a>

I decided to build this app in my weaker language of the two that I practice so far. I've just graduated a bootcamp concentrating on JavaScript & JS frameworks, so I thought this would be a great opportunity to refresh my novice/rusty Python skills and demonstrate my range as a developer.

I had a lot of research to do! Since I'm self-taught in Python, this project required quite a few skills that I'd never attempted in this language (such as sending api calls & writing tests). 

I wanted to avoid relying on libraries, apart from built-in modules and those explicitly permitted in the instructions (which stated we could use libraries to parse JSON & send API requests). 

Before I got started, I spent half a day researching approaches to building Python CLI's. Many examples I found relied heavily on dependencies, until I found a blog about building a simple command line weather forecaster. I built <a href='github.com/fifikim/weather-cli'>this weather app</a> to get a sense of my process and then went to work on this Books CLI.

### Day One <a name = "day-one"></a>
- Goals:
  - Create kanban board with user stories to guide feature implementation
  - Pseudocode a skeleton of the app & then write each function

- Wins: 
  - ✅ Built a working (buggy) version of the full program with decent UI. 
  - ✅ Figured out how to save reading list to a local json file so that data persists after app exits.

- Blockers:
  - 👻 Python feeling very foreign & I'm fighting constant urge to hit the semicolon key.
  - ❓ Have never written a test in Python (only Mocha/Chai for JS) - need to research tomorrow.
  - ❓ Unsure how to handle invalid menu selections & queries.

### Day Two <a name = "day-two"></a>
- Goals:
  - Work on blockers from yesterday - testing, special characters
  - Improve UX: app should only exit when user decides to quit 
  - Look into ways to reduce coupling: ORM/encapsulation
  - Modularize components for reusability & SOC 
  - Break apart fns that aren't following SRP
  - Create classes -- whoops!!!! Edit book & menu fns to use classes & class methods

- Wins:
  - ✅ Code feels much less redundant after creating classes & methods.
  - ✅ Better user flow, fewer unexpected terminations/dead ends.
  - ✅ Took some effort but was able to convert reading list & search results back and forth from JSON format to a list of Book class instances.

- Blockers:
  - ⏳ Took a long time to switch from functional to OOP mindset. Not sure that I'm there yet.
  - ❓ Unsure how to let user cancel out of input prompt without exiting program.
  - 😨 Wasn't able to start testing today -- more research needed on this topic.

### Day Three <a name = "day-three"></a>
- Goals:
  - Create tests
  - Implement try/except blocks to catch invalid user input
  - Keep looking for ways to DRY code, separate concerns, & decouple components

- Wins:
  - ✅ Refactored code to remove all global variables 
  - ✅ Validation handles invalid/blank input for menu selection & search queries
  - ✅ Learned how to color output to the terminal w/o using additional libraries. Happier with UI.
  - ✅ Created tests to check fns that return 

- Blockers:
  - ❓ Not sure yet how to write tests that check terminal output - need to read up on unittest.mock
  - ❓ Realized that program won't run on Python 2, I think due to use of f-strings. Could convert all formatting to use string concatenation, but want to research building executable stand-alone apps to run on Mac/Unix & Windows. 

### Day Four <a name = "day-four"></a>
- Goals:
  - Create tests that mock print() and input()
  - Figure out how to turn script into executable stand-alone app

- Wins:
  - Finished README file w/ preview gif & instructions

- Blockers:
  - Spent a lot of today working on the tic-tac-toe code review, and wasn't able to do more research on testing mocks. Going to keep working on this after I submit, and hopefully will have the opportunity to submit more thorough tests with my revision.
  - 🤞 Researched packaging and distributing Python projects but not sure if I'm doing it right so that other users are able to use the requests module.

## Future Implementation <a name = "future"></a>

- Add hidden id key to book entries, enabling program to prevent user from creating duplicate entries in reading list
- Create additional tests to ensure print() and output() functions are working correctly

## Author <a name = "author"></a>

Sophia Kim <br/>
mail@fifikim.com <br/>
<a href="linkedin.com/in/fifikim">LinkedIn</a> <br/>

## Acknowledgements <a name = "acknowledgements"></a>

Books and online references:
- Clean Python, Sunil Kapil, Apress
- Python Cookbook, David Beazley & Brian K. Jones, O'Reilly
- <a href='https://docs.python.org/3/library/unittest.html'>Unittest</a>
- <a href='https://www.codecademy.com/courses/learn-intermediate-python-3/lessons/int-python-unit-testing/'>More on Testing</a> (subscription required)
- <a href='https://stackabuse.com/how-to-print-colored-text-in-python/'>Coloring terminal output</a>
- <a href='https://realpython.com/python-json/'>Encoding/Decoding JSON <==> Custom Python Objects</a>
- <a href='https://packaging.python.org/en/latest/tutorials/packaging-projects/'>Packaging Python projects</a>