"""
fetcher.py

This module contains various functions for fetching the html for a given page
and returning it.
"""
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time

def simpleFetch(url) :
    '''
    This function fetches the html for a given webpage using the requests module,
    parses it using BeautifulSoup and then returns it.
    One argument accepted, the url.
    '''
    try :
        response = requests.get(url)
        return str(BeautifulSoup(response.content))
    except Exception as e :
        return 'null'

def waitroseFetch(url, scroll) :
    '''
    A function for fetching the html for Waitrose store pages. The pages are
    fetched and processed using the PhantomJS browser controlled by the
    selenium module. The html is then parsed by BeautifulSoup and returned.
    Two arguments accepted: the url and the number of times the page needs to
    be scrolled.
    '''
    try :
        browser = webdriver.PhantomJS()
        browser.get(url)
        htmlString = BeautifulSoup(browser.page_source)

        counter = 0

        while counter < scroll :
            htmlString = BeautifulSoup(browser.page_source)
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.6)
            counter += 1

        browser.quit()

        return str(htmlString)
    except Exception as e :
        return 'null'

