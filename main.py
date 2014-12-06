"""
scrape-demo-2.py

A modified version of the original demo - this one
grabs bottled water prices from the Tesco groceries page and print them.

Created by Charles Bos
"""

from bs4 import BeautifulSoup
import requests

url = "http://www.tesco.com/groceries/product/browse/default.aspx?N=4294792649&Ne=4294793660"

response = requests.get(url)

htmlString = str(BeautifulSoup(response.content))

priceStart = htmlString.find('£')
priceEnd = priceStart + 5
priceExtract = htmlString[priceStart:priceEnd]

if priceStart == -1 : print("No prices here. Sorry.")
else :
    while htmlString[priceEnd] != htmlString[-1] :
        print(priceExtract)
        htmlString = str(htmlString[priceEnd:])
        priceStart = htmlString.find('£')
        priceEnd = priceStart + 5
        priceExtract = htmlString[priceStart:priceEnd]
