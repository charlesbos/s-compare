"""
tesco.py

Tesco module from the Team S price comparison software

Created by Charles Bos
"""

from operator import itemgetter
from fetcher import htmlFetch

def tescoData() :
    '''
    Extract Tesco line prices and item titles
    No arguments accepted
    '''

    htmlString = htmlFetch("http://www.tesco.com/groceries/product/browse/default.aspx?N=4294792641&Ne=4294793660")
    
    # Extract prices
    priceStart = htmlString.find('<span class="linePrice">£') + 24

    if priceStart == -1 :
        print("No prices here. Sorry.")
    else :
        priceEnd = priceStart + 5
        priceExtract = htmlString[priceStart:priceEnd]
        priceList = [priceExtract]
        
        while priceStart != 23 :
            priceStart = htmlString.find('<span class="linePrice">£', priceEnd) + 24
            priceEnd = priceStart + 5
            priceExtract = htmlString[priceStart:priceEnd]
            priceList.extend([priceExtract])

        priceList = priceList[:-1]

    # Extract titles
    titleStart = htmlString.find('<span data-title="true">') + 24

    if titleStart == -1 :
        print("No titles here. Sorry.")
        quit()
    else :
        titleEnd = htmlString.find('</span>')
        titleExtract = htmlString[titleStart:titleEnd]
        titleList = [titleExtract]

        while titleStart != 23 :
            titleStart = htmlString.find('<span data-title="true">', titleEnd) + 24
            titleEnd = htmlString.find('</span></a></h2>', titleStart)
            titleExtract = htmlString[titleStart:titleEnd]
            titleList.extend([titleExtract])

        titleList = titleList[1:-1]

    # Turn the two lists into a dictionary and return it
    if len(priceList) != len(titleList) :
        print("Error. Lengths of prices and item titles do not match.")
    else :
        pricesComparison = dict(zip(titleList, priceList))
        return sorted(pricesComparison.items(), key=itemgetter(1))


                            


                    


