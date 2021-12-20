<h1 align="center">Books on 8th</h1>

<div>
<p align="center"> A command line application utilizing Google Books API. <br> 
Allows user to search for books and save selections to a reading list.
</p>

<p align="center">
  <a href="" rel="noopener">
  <img width=200px height=200px src="https://i.imgur.com/6wj0hh6.jpg" alt="Project logo"></a></br>
  (preview gif)
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
- [Author](#author)
- [Acknowledgments](#acknowledgments)


## Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites 

What things you need to install the software and how to install them.

```
Give examples
```

### Installing 

A step by step series of examples that tell you how to get a development env running.

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo.

## Testing <a name = "testing"></a>

Explain how to run the automated tests for this system.

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Usage <a name="usage"></a>

Add notes about how to use the system.

## Process <a name = "process"></a>

I decided to write this program in my weaker language of the two so far that I practice. I've just graduated a bootcamp concentrating on JavaScript & JS frameworks, so I thought this would be a great opportunity to refresh my rusty Python skills and demonstrate my range as a developer.

That meant that I had a lot of research to do! Since I'm self-taught in Python, this project required quite a few aspects that I'd never encountered in this language.

Before I got started, I spent half a day researching approaches to Python CLI's. Many examples I found relied heavily on dependencies (which I wanted to avoid), until I found a blog about building a command line weather forecaster. I built <a href='github.com/fifikim/weather-cli'>this weather app</a> to get a sense of my process and then went to work on the books CLI.

### Day One <a name = "day-one"></a>
- Goals:
  - ✅ Kanban board with user stories to guide feature implementation
  - ✅ Pseudocode a skeleton of the app & then write each function

- Wins: 
  - ✅ Created a working (buggy) version with decent UI. 
  - ✅ Figured out how to save reading list to a local json file so that it persists after app exits.
  - ✅ I got to code in Python again, yay!

- Blockers:
  - 👻 What is Python? lol - feeling amnesia & constant urge to hit that semicolon key
  - ❓ Have never written a test in Python - need to research tomorrow
  - ❓ Unsure how to handle queries including special characters 

### Day Two <a name = "day-two"></a>
- Goals:
  - Work on blockers from yesterday - testing, special characters
  - Improve UX: 
    - ✅ app should only exit when user decides to quit 
    - let user cancel a search or save
    - add identifier to books (not displayed) to prevent saving duplicate entries
  - Look into ways to reduce coupling: ORM/encapsulation
  - ✅ Modularize components for reusability & SOC 
  - ✅ Break apart fns that aren't following SRP
  - ✅ Create classes -- whoops!!!! Edit book & menu fns to use classes

- Wins:
  - ✅ Code feels much less redundant & cleaner after creating classes & methods.
  - ✅ Better user flow, fewer unexpected terminations/dead ends.
  - ✅ Took some effort but was able to convert reading list & search results back and forth from JSON format to a list of Book class instances.

- Blockers:
  - ⏳ Took a long time to switch from functional to OOP mindset. 
  - ❓ Not sure how to let user cancel out of input prompt without exiting program.
  - 😨 Wasn't able to start testing today -- more research needed.

### Day Three <a name = "day-three"></a>
- Goals:
  - Create tests
  - Implement try/except blocks to catch invalid user input
  - Keep looking for ways to DRY code, separate concerns, & decouple components
  - Create installation instructions for user

- Wins:
  - ✅ Learned how to color output to the terminal without installing additional libraries, using ANSI escape sequences (need to figure out how to test compatibility with other OS's)

- Blockers:

## Author <a name = "author"></a>

Sophia Kim <br/>
mail@fifikim.com <br/>
<a href="linkedin.com/in/fifikim">LinkedIn</a> <br/>
portfolio under construction

## Acknowledgements <a name = "acknowledgements"></a>

List of books and references consulted:
- Clean Python, Sunil Kapil, Apress