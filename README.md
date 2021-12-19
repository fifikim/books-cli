# Books on 8th

A command line application utilizing Google Books API. Allows user to search for books and save selections to a reading list.

## Preview

to come

## Features

to come

## Installation

to come 

## Process

I decided to write this program in Python even though it's my weaker language of the two so far that I practice. I've just graduated a bootcamp concentrating solely on JavaScript & JS frameworks, so I thought this project would be a great opportunity to refresh my rusty Python skills and demonstrate my range as a developer.

It also meant that I had a lot of research to do! Since I'm self-taught in Python, this project required quite a few aspects that I'd never encountered in this language. (Testing, etc etc)

Before I got started, I spent half a day researching approaches to Python CLI's. Many examples I found relied heavily on dependencies (which I wanted to avoid), until I found a blog about building a command line weather forecaster. I built <a href='github.com/fifikim/weather-cli'>this weather app</a> to get a sense of my process, and then went to work on the books CLI.

### Day One 
- Goals:
  ✅ Kanban board with user stories to guide feature implementation
  ✅ Pseudocode a skeleton of the app & then write each function

- Wins: 
  ✅ Created a working (buggy) version with decent UI. 
  ✅ Figured out how to save reading list to a local json file so that it persists after app exits.
  ✅ I got to code in Python again, yay!

- Blockers:
  👻 What is Python? lol - feeling amnesia & constant urge to hit that semicolon key
  ❓ Have never written a test in Python - need to research tomorrow
  ❓ Unsure how to handle queries including special characters & spaces

# Day Two 
- Goals:
  - Work on blockers from yesterday - testing, special characters
  - Improve UX: 
    - app should only exit when user decides to quit 
    - let user cancel a search or save
    - add identifier to books (not displayed) to prevent saving duplicate entries
    - write help files?
  - Look into ways to reduce coupling: ORM/encapsulation
  - Modularize components for reusability & SOC 
  - Break apart fns that aren't following SRP
  - Create classes -- whoops!!!! Edit book & menu fns to use classes

- Wins:

- Blockers: