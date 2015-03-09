"""
This program contains various functions for fetching the html for a given page
and returning it.

Copyright (C) 2015 Team S

Team S comprises of :
* Charles Bos
* Daniel Bedingfield
* Joshua Coyle
* Oyinpreye Onita
* Sebastian Jakobsen
* Thomas Harris

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
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

