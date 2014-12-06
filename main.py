"""
scrape-demo-3_0_0.py

Version 3.0.0 is much improved. See CHANGELOG on Onedrive for a full list of changes.

Created by Charles Bos
"""

from bs4 import BeautifulSoup
import requests
from operator import itemgetter

url = "http://www.tesco.com/groceries/product/browse/default.aspx?N=4294792649&Ne=4294793660"

response = requests.get(url)

htmlString = str(BeautifulSoup(response.content))

priceStart = htmlString.find('<span class="linePrice">£') + 25
priceEnd = priceStart + 4
priceExtract = htmlString[priceStart:priceEnd]
priceList = [priceExtract]

if priceStart == -1 : print("No prices here. Sorry.")
else :
    while priceStart != 24 :
        priceStart = htmlString.find('<span class="linePrice">£', priceEnd) + 25
        priceEnd = priceStart + 4
        priceExtract = htmlString[priceStart:priceEnd]
        priceList.extend([priceExtract])

priceList = priceList[:-1]

titleStart = htmlString.find('<span data-title="true">') + 24
titleEnd = htmlString.find('</span>')
titleExtract = htmlString[titleStart:titleEnd]
titleList = [titleExtract]

if titleStart == -1 : print("No titles here. Sorry.")
else :
    while titleStart != 23 :
        titleStart = htmlString.find('<span data-title="true">', titleEnd) + 24
        titleEnd = htmlString.find('</span></a></h2>', titleStart)
        titleExtract = htmlString[titleStart:titleEnd]
        titleList.extend([titleExtract])

titleList = titleList[1:-1]

pricesComparison = ({titleList[0] : priceList[0]})

priceListLength = len(priceList)
titleListLength = len(titleList)

counter = 1

if priceListLength != titleListLength :
    print("Error. Lengths of prices and item titles do not match.")
else:
    while counter != priceListLength :
        pricesComparison.update({titleList[counter] : priceList[counter]})
        counter = counter + 1

    pricesComparisonSorted = sorted(pricesComparison.items(), key=itemgetter(1))

    counter = 0

    while counter != priceListLength :
        print(pricesComparisonSorted[counter])
        counter = counter + 1


                            


                    


