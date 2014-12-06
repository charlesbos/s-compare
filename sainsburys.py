"""
sainsburys.py

Sainsburys module from the Team S price comparison software

Created by Charles Bos
"""

from operator import itemgetter
from fetcher import htmlFetch

def sainsburysData() :
    '''
    Extract Sainsburys prices and item titles
    No arguments accepted
    '''

    htmlString = htmlFetch("http://www.sainsburys.co.uk/shop/gb/groceries/drinks/still-water#langId=44&storeId=10151&catalogId=10122&categoryId=12351&parent_category_rn=12192&top_category=12192&pageSize=30&orderBy=FAVOURITES_FIRST&searchTerm=&beginIndex=0")
    
    # Extract prices
    priceStart = htmlString.find('<p class="pricePerUnit">') + 24

    if priceStart == -1 :
        print("No prices here. Sorry.")
    else :
        priceEnd = priceStart + 8
        priceExtract = htmlString[priceStart + 2:priceEnd - 1]
        priceList = [priceExtract]
        
        while priceStart != 23 :
            priceStart = htmlString.find('<p class="pricePerUnit">', priceEnd) + 24
            priceEnd = priceStart + 8
            priceExtract = htmlString[priceStart + 2:priceEnd - 1]
            priceList.extend([priceExtract])

        priceList = priceList[:-1]

    # Extract titles
    titleStart = htmlString.find('''<a href="http://www.sainsburys.co.uk/shop/gb/groceries/still-water/''') + 67

    if titleStart == -1 :
        print("No titles here. Sorry.")
    else :
        titleEnd = htmlString.find('<img alt=')
        titleInitialExtract = htmlString[titleStart:titleEnd]
        titleFinalExtract = titleInitialExtract.partition(" ")[0][:-3]
        titleList = [titleFinalExtract]

        while titleStart != 66 :
            titleStart = htmlString.find('''<a href="http://www.sainsburys.co.uk/shop/gb/groceries/still-water/''', titleEnd) + 67
            titleEnd = htmlString.find('<img alt=', titleStart)
            titleInitialExtract = htmlString[titleStart:titleEnd]
            titleFinalExtract = titleInitialExtract.partition(" ")[0][:-3]
            titleList.extend([titleFinalExtract])

        titleList = titleList[1:]

    # Turn the two lists into a dictionary and print it line by line
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


                            


                    


