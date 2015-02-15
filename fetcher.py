"""
fetcher.py

This module contains various functions for fetching the html for a given page
and returning it.
"""
import time
import os
from tkinter import messagebox
try :
    from bs4 import BeautifulSoup
    from selenium import webdriver
    import requests
except ImportError :
    messagebox.showerror(title = 'Software not installed', message = 'Some of the software required to run this program is not installed. Please ensure you have installed the following: Python-Requests, Python-BeautifulSoup4, Python-Selenium, PhantomJS')
    os._exit(0)

def simpleFetch(url) :
    '''
    This function fetches the html for a given webpage using the requests module,
    parses it using BeautifulSoup and then returns it.
    One argument accepted, the url.
    '''
    try :
        response = requests.get(url)
        return str(BeautifulSoup(response.content))
    except :
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

        for x in range(scroll) :
            htmlString = BeautifulSoup(browser.page_source)
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.7)

        browser.quit()

        # Uncomment for debugging purposes
        # file = open('Waitrose_Html.txt', 'w')
        # print(htmlString, file = file)
        # file.close()

        return str(htmlString)
    except :
        return 'null'
    finally :
        try :
            os.remove('ghostdriver.log')
        except IOError :
            pass

