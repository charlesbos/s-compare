"""
fetcher.py

This module contains various functions for fetching the html for a given page
and returning it.
"""
from time import sleep
from tkinter import messagebox
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import os

def simpleFetch(url) :
    '''
    Fetch html for a webpage, parse it with BeautifulSoup and then return it.
    '''
    try :
        response = requests.get(url)
        return str(BeautifulSoup(response.content))
    except :
        return 'null'

def waitroseFetch(url, scroll) :
    '''
    Visit a webpage with the PhantomJS browser, generate the html by ensuring that
    the relevant javascript is executed and then return that html.
    '''
    try :
        browser = webdriver.PhantomJS()
        browser.get(url)

        for x in range(scroll) :
            htmlString = BeautifulSoup(browser.page_source)
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(0.7)

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

