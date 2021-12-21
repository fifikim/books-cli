from setuptools import setup

setup(
    name='Books on 8th',
    url='https://github.com/fifikim/books-cli',
    author='Sophia Kim',
    author_email='mail@fifikim.com',
    packages=['books'],
    install_requires=['requests'],
    version='0.1',
    license='MIT',
    description='A command line app utilizing Google Books API to search for & save books',
    long_description=open('README.md').read(),
)