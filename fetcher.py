"""
fetcher.py

This module downloads html for a given url, applies soup to the html using
BeautifulSoup and then returns the html as a string.

Created by: Charles Bos
Contributors: Charles Bos
"""

from bs4 import BeautifulSoup
import requests

def htmlFetch(url) :
    '''
    Returns a string of html which the other modules can use
    One argument accepted, the url.
    '''
    response = requests.get(url)
    return str(BeautifulSoup(response.content))
