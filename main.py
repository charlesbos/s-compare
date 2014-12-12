"""
main.py

This file imports the various modules for each shop, calls the functions and
then outputs the data returned by them.

We built this program! We built this program on Py-thon 3! (I listened to way too much Starship today...)

Created by: Charles Bos
Contributors: Charles Bos
"""
from tesco import tescoData
from sainsburys import sainsburysData
from operator import itemgetter

def lowestPrices(prices) :
    '''
    This function extracts the minimum values from a dictionary and then the keys to
    match. Then it creates a new dictionary from the two lists.
    '''
    minKeys = [keys for keys, values in prices.items() if values == min(prices.values())]   
    minVals =  [min(prices.values())] * len(minKeys)
            
    return dict(zip(minKeys, minVals))

def cheapestFrom() :
    '''
    A way of finding which shop the lowest price came from as this information
    is not preserved when merging our lists.
    No arguments taken.
    '''
    if tescoPrices[cheapestItem] != None : return "Tesco"
    if sainsburysPrices[cheapestItem] != None : return "Sainsbury's"

def fileOutput(tescoPrices, sainsburysPrices) :
    '''
    This function will neatly output the results of the scraping and comparison
    into a text file.
    Multiples arguments are taken: the per shop dictionarys of prices and items to be output.
    '''
    file = open('OUTPUT.txt', 'w')

    prices = []

    for key, value in tescoPrices.items() :
        prices.append((key, value, "Tesco"))

    for key, value in sainsburysPrices.items() :
        prices.append((key, value, "Sainsbury's"))

    sortedPrices = sorted(prices, key=itemgetter(1))

    length = len(sortedPrices)
    counter = 0

    while counter < length :
        print('{:55s}'.format(sortedPrices[counter][0]), '{:15s}'.format(sortedPrices[counter][1]), sortedPrices[counter][2],  file = file)
        counter += 1

    file.close()    

# Call functions from the shop modules to extract item titles and prices
tescoPrices = tescoData("http://www.tesco.com/groceries/product/browse/default.aspx?N=4294792641&Ne=4294793660")
sainsburysPrices = sainsburysData("http://www.sainsburys.co.uk/shop/gb/groceries/drinks/still-water#langId=44&storeId=10151&catalogId=10122&categoryId=12351&parent_category_rn=12192&top_category=12192&pageSize=30&orderBy=FAVOURITES_FIRST&searchTerm=&beginIndex=0")

# Output neatly formatted table of all prices to a file called output.txt
fileOutput(tescoPrices, sainsburysPrices)

# Append some useful information to the 
cheapestTesco = lowestPrices(tescoPrices)
cheapestSainsburys = lowestPrices(sainsburysPrices)

file = open('OUTPUT.txt', 'a')

print("\n\nThe cheapest water from Tesco:", cheapestTesco, file = file)
print("\nThe cheapest water from Sainsbury's:", cheapestSainsburys, file = file)

cheapByShop = dict(list(cheapestTesco.items()) + list(cheapestSainsburys.items()))
cheapestOverall = lowestPrices(cheapByShop)
cheapestItem = list(cheapestOverall.keys())[0]

print("\nThe cheapest water overall:", cheapestOverall, "from", cheapestFrom()+'.', file = file)

file.close()

print("Processing completed! Please see the file 'OUTPUT.txt' which has been created in the directory from which you ran this program.")
