"""
scrape-demo-2_1_5.py

A modified version of scrape demo 2.1. demo 2.1.5 sorts the list.

Created by Charles Bos on 2014-11-26
"""

from bs4 import BeautifulSoup
import requests

url = "http://www.tesco.com/groceries/product/browse/default.aspx?N=4294792649&Ne=4294793660"

response = requests.get(url)

htmlString = str(BeautifulSoup(response.content))

priceStart = htmlString.find('£') + 1
priceEnd = priceStart + 4
priceTerminus = htmlString.rfind('£')
priceExtract = htmlString[priceStart:priceEnd]
priceList = [priceExtract]


if priceStart == -1 : print("No prices here. Sorry.")
else :
    while priceStart < priceTerminus :
        htmlString = str(htmlString[priceEnd:])
        priceStart = htmlString.find('£') + 1
        priceEnd = priceStart + 4
        priceTerminus = htmlString.rfind('£')
        priceExtract = htmlString[priceStart:priceEnd]
        priceList.extend([priceExtract])

priceListSorted = sorted(priceList)

print(priceListSorted)
