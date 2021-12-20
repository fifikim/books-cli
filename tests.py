import unittest
import json

{
    "title": "Experiments in Personality: Volume 1 (Psychology Revivals)",
    "author": "H.J. Eysenck",
    "publisher": "H.J. Eysenck"
}

author = 'my dad'
title = 'a BOOK'
publisher = 'mabmo'

book = {
  'author': author,
  'title': title,
  'publisher': publisher
}

print(json.dumps(book, indent=4))