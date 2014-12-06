"""
scrape-demo-2_9_9.py

A modified version of scrape demo 2.1.5. Version 2.9.9 extracts
the product titles as well and stores them in a list.
Version 3 will store the prices and titles in a dictionary.

Created by Charles Bos on 2014-11-26
"""

# Note: not yet working.

from bs4 import BeautifulSoup
import requests

url = "http://www.tesco.com/groceries/product/browse/default.aspx?N=4294792649&Ne=4294793660"

response = requests.get(url)

htmlString = str(BeautifulSoup(response.content))
tempA = htmlString[:]
tempB = htmlString[:]

priceStart = tempA.find('£') + 1
priceEnd = priceStart + 4
priceExtract = tempA[priceStart:priceEnd]
priceTerminus = tempA.rfind('£') + 1
priceList = [priceExtract]

if priceStart == -1 : print("No prices here. Sorry.")
else :
    while priceStart < priceTerminus :
        tempA = str(tempA[priceEnd:])
        priceStart = tempA.find('£') + 1
        priceEnd = priceStart + 4
        priceExtract = tempA[priceStart:priceEnd]
        priceTerminus = tempA.rfind('£') + 1
        priceList.extend([priceExtract])

titleStart = tempB.find('<span data-title="true">') + 24
titleEnd = tempB.find('</span></a></h2>')
titleExtract = tempB[titleStart:titleEnd]
titleTerminus = len(priceList)
titleList = [titleExtract]

if titleStart == -1 : print("No titles here. Sorry.")
else :
    while titleTerminus > 1 :
        tempB = str(tempB[titleEnd + 1:])
        titleStart = tempB.find('<span data-title="true">')
        titleEnd = tempB.find('</span></a></h2>')
        titleExtract = tempB[titleStart + 24:titleEnd]
        titleTerminus = titleTerminus - 1
        titleList.extend([titleExtract])
        print('worked')

print(priceList)
print(titleList)
