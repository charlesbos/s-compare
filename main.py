"""
main.py

This file imports the various modules for each shop, calls the functions and
then outputs the data returned by them.
"""
from tesco import tescoData
from sainsburys import sainsburysData
from operator import itemgetter
import os

def lowestPrices(prices) :
    '''
    This function extracts the minimum prices from a list of tuples. Then it returns a list of tuples
    which contain just those tuples with the minimum values.

    One argument is argument, the list of tuples from which to extract the minimum values.
    '''
    prices = sorted(prices, key=itemgetter(1,0))

    minPrices = [(prices[0])]

    counter = 1

    while counter < len(prices) :
        if prices[counter][1] == minPrices[0][1] : minPrices.append((prices[counter]))
        counter += 1
       
    return minPrices

def writeTable(prices, tableHeader) :
    '''
    A function to write a price list to a neatly formatted table in the
    output file. Two arguments are taken, the price list and the header for the
    table.
    '''
    file = open('OUTPUT.txt', 'a')

    prices = sorted(prices, key=itemgetter(1,0))

    print(tableHeader, file = file)
    
    if prices != [] :
        counter = 0

        while counter < len(prices) :
            print('{:55s}'.format(prices[counter][0]), '{:15s}'.format(prices[counter][1]), prices[counter][2], file = file)
            counter += 1
    else : print("No results obtained. Cannot create table.", file = file)
            
    file.close()

# Call functions from the shop modules to extract item titles and prices
tescoPrices = tescoData("http://www.tesco.com/groceries/product/browse/default.aspx?N=4294792641&Ne=4294793660", "/100ml")
sainsburysPrices = sainsburysData("http://www.sainsburys.co.uk/shop/gb/groceries/drinks/still-water#langId=44&storeId=10151&catalogId=10122&categoryId=12351&parent_category_rn=12192&top_category=12192&pageSize=30&orderBy=FAVOURITES_FIRST&searchTerm=&beginIndex=0", '''<a href="http://www.sainsburys.co.uk/shop/gb/groceries/still-water/''', "/100ml")

# Create aggregate lists
allPrices = []
cheapest = []

if tescoPrices != 'null' :
    allPrices += tescoPrices
    cheapest += lowestPrices(tescoPrices)
else : print("Operation for Tesco failed. No results for Tesco will be displayed.")
if sainsburysPrices != 'null' :
    allPrices += sainsburysPrices
    cheapest += lowestPrices(sainsburysPrices)
else : print("Operation for Sainsbury's failed. No results for Sainsbury's will be displayed.")

# Delete old ouput file if it exists
try :
    os.remove('OUTPUT.txt')
except IOError :
    pass

# Write tables
writeTable(allPrices, "== Prices from all shops ==")
writeTable(cheapest, "\n== Lowest prices from each shop ==")

# Output message to inform user that program has finished working
print("\nProcessing completed! Please see the file 'OUTPUT.txt'.")
