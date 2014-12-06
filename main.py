"""
scrape-demo-2_1.py

A modified version of scrape-demo-2 - scrape demo 2.1
grabs bottled water prices from the Tesco groceries page, and adds them to a list.

Created by Charles Bos
"""

from bs4 import BeautifulSoup
import requests

url = "http://www.tesco.com/groceries/product/browse/default.aspx?N=4294792649&Ne=4294793660"

response = requests.get(url)

htmlString = str(BeautifulSoup(response.content))

priceStart = htmlString.find('£')
priceEnd = priceStart + 5
priceTerminus = htmlString.rfind('£')
priceExtract = htmlString[priceStart:priceEnd]
priceList = [priceExtract]


if priceStart == -1 : print("No prices here. Sorry.")
else :
    while priceStart < priceTerminus :
        htmlString = str(htmlString[priceEnd:])
        priceStart = htmlString.find('£')
        priceEnd = priceStart + 5
        priceTerminus = htmlString.rfind('£')
        priceExtract = htmlString[priceStart:priceEnd]
        priceList.extend([priceExtract])

print(priceList)
