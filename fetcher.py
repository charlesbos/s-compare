"""
fetcher.py

Fetch required html

Created by Charles Bos
"""

from bs4 import BeautifulSoup
import requests

def htmlFetch(url) :
    '''
    Returns a string of html which the other modules can use
    One argument accepted, the url.
    '''
    response = requests.get(url)
    htmlString = str(BeautifulSoup(response.content))
    return htmlString
