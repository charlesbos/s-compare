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

    print(str(tableHeader).center(113, ' '), file = file)
    print('-' * 113, file = file)
    
    if prices != [] :
        counter = 0

        while counter < len(prices) :
            print('{:85s}'.format(prices[counter][0]), '{:15s}'.format(prices[counter][1]), prices[counter][2], file = file)
            print('-' * 113, file = file)
            counter += 1
    else : print("No results obtained. Cannot create table.", file = file)

    print('\n', file = file)
            
    file.close()

def dataPull(file, shopFunc, titletag, unit) :
    '''
    A function to dynamically call the shop module functions multiple times (for different urls)
    according to the product chosen by the user.
    Four arguments are taken. The first is the path to the file from which to extract the urls. The
    second is the name of the shop function to call. The third is the html string which the shop function
    uses to search for titles (strictly speaking, this is only needed for the sainsburys module). The fourth
    is the unit to attach to the prices.
    '''
    file = open(file, 'r')

    urls = str(file.read()).split('\n')

    counter = 0
    prices = []

    while counter < len(urls) :
        temp = shopFunc(urls[counter], titletag, unit)
        if temp != 'null' : prices += temp
        counter += 1

    return prices

# Print startup message
print('''This program compares prices for common groceries across a number of different
UK retailers.''')
            
# Choose product for comparison and then call modules for data extraction
unselect = 1

while unselect == 1 :
    try :
        proType = input("\nWould you like to compare prices for food or drink? [f/d]: ")
        if (proType != 'f') and (proType != 'd') : int('null')
        unselect = 0
    except ValueError :
        print("\nInvalid choice.")

if proType == 'd' :
    print("\nEnter 1 to compare prices for still water.")
    print("Enter 2 to compare prices for sparkling water.")

    unselect = 1

    while unselect == 1 :
        try :
            product = int(input("\nChoose a product to compare: "))
            if (1 <= product <= 2) is False : int('null')
            unselect = 0
        except ValueError :
            print("\nInvalid choice.")

    if product == 1 :
        tescoPrices = dataPull('URL_STORE/TESCO/STILL_WATER.txt', tescoData, 'null', "/100ml")
        sainsburysPrices = dataPull('URL_STORE/SAINSBURYS/STILL_WATER.txt', sainsburysData, '<a href="http://www.sainsburys.co.uk/shop/gb/groceries/still-water/', "/100ml")

    if product == 2 :
        tescoPrices = dataPull('URL_STORE/TESCO/SPARKLING_WATER.txt', tescoData, 'null', "/100ml")
        sainsburysPrices = dataPull('URL_STORE/SAINSBURYS/SPARKLING_WATER.txt', sainsburysData, '<a href="http://www.sainsburys.co.uk/shop/gb/groceries/sparkling-water/', "/100ml")

if proType == 'f' :
    print("\nEnter 1 to compare prices for white bread.")
    print("Enter 2 to compare prices for brown bread.")

    unselect = 1

    while unselect == 1 :
        try :
            product = int(input("\nChoose a product to compare: "))
            if (1 <= product <= 2) is False : int('null')
            unselect = 0
        except ValueError :
            print("\nInvalid choice.")

    if product == 1 :
        tescoPrices = dataPull('URL_STORE/TESCO/WHITE_BREAD.txt', tescoData, 'null', "/100g")
        sainsburysPrices = dataPull('URL_STORE/SAINSBURYS/WHITE_BREAD.txt', sainsburysData, '<a href="http://www.sainsburys.co.uk/shop/gb/groceries/white-bread/', "/100g")

    if product == 2 :
        tescoPrices = dataPull('URL_STORE/TESCO/BROWN_BREAD.txt', tescoData, 'null', "/100g")
        sainsburysPrices = dataPull('URL_STORE/SAINSBURYS/BROWN_BREAD.txt', sainsburysData, '<a href="http://www.sainsburys.co.uk/shop/gb/groceries/wholemeal-brown-bread/', "/100g")

# Create aggregate lists
allPrices = []
cheapest = []

if tescoPrices != [] :
    allPrices += tescoPrices
    cheapest += lowestPrices(tescoPrices)
else : print("Operation for Tesco failed. No results for Tesco will be displayed.")
if sainsburysPrices != [] :
    allPrices += sainsburysPrices
    cheapest += lowestPrices(sainsburysPrices)
else : print("Operation for Sainsbury's failed. No results for Sainsbury's will be displayed.")

# Delete old ouput file if it exists
try :
    os.remove('OUTPUT.txt')
except IOError :
    pass

# Write tables
writeTable(cheapest, "== Lowest prices from each shop ==")
writeTable(allPrices, "== Prices from all shops ==")

# Output message to inform user that program has finished working
print("\nProcessing completed! Please see the file 'OUTPUT.txt'.")
