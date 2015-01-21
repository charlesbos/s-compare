"""
main.py

This file imports the various modules for each shop, calls the functions and
then outputs the data returned by them.
"""
from tesco import tescoData
from sainsburys import sainsburysData
from waitrose import waitroseData
import os

def lowestPrices(prices) :
    '''
    This function extracts the minimum prices from a list of tuples. Then it returns a list of tuples
    which contain just those tuples with the minimum values.

    One argument is accepted, the list of tuples from which to extract the minimum values.
    '''
    prices = sortPrices(prices)
    return [list(x) for x in prices if x[1] == prices[0][1]]

def writeTable(prices, tableHeader) :
    '''
    A function to write a price list to a neatly formatted table in the
    output file. Two arguments are taken, the price list and the header for the
    table.
    '''
    prices = sortPrices(prices)
    
    file = open('OUTPUT.txt', 'a')
    print(str(tableHeader).center(120, ' '), file = file)
    print('-' * 120, file = file)
    
    if prices != [] :
        for x in range(len(prices)) :
            print('{:85s}'.format(prices[x][0]), prices[x][1].rjust(15, ' '), ' ' * 6, prices[x][2], file = file)
            print('-' * 120, file = file)
    else : print("No results obtained. Cannot create table.", file = file)
    
    print('\n', file = file)
            
    file.close()

def dataPull(filePath, shopFunc, titletag, unit, scroll) :
    '''
    A function to dynamically call the shop module functions multiple times (for different urls)
    according to the product chosen by the user.
    Four arguments are taken. The first is the path to the file from which to extract the urls. The
    second is the name of the shop function to call. The third is the html string which the shop function
    uses to search for titles (Sainsburys only). The fourth is the unit to attach to the prices. The
    fifth is the number of times the page needs to be scrolled (Waitrose only).
    '''
    prices = []
    file = open(filePath, 'r')
    urls = str(file.read()).split('\n')
    urls = [x for x in urls if x != '']

    for x in range(len(urls)) :
        temp = shopFunc(urls[x], titletag, unit, scroll)
        if temp != 'null' : prices += temp

    return prices

def sortPrices(prices) :
    '''
    A function to correctly sort the lists of tuples by price. Using the sorted function does not
    always work correctly because our prices are strings, not floats.
    One argument is accepted, the list of prices to be sorted.
    '''
    x = 0
    y = 1

    if (prices != 'null') and (prices != []) :
        for x in range(len(prices)) :
            for y in range(len(prices) -1, x, -1) :
                tupA = prices[x]
                tupB = prices[y]
                priceA = tupA[1]
                priceB = tupB[1]
                endA = priceA.find('/')
                endB = priceB.find('/')
                if float(priceA[1:endA]) > float(priceB[1:endB]) :
                    prices[x] = tupB
                    prices[y] = tupA        

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
    print("Enter 3 to compare prices for everyday tea.")
    print("Enter 4 to compare prices for milk.")

    unselect = 1

    while unselect == 1 :
        try :
            product = int(input("\nChoose a product to compare: "))
            if (1 <= product <= 4) is False : int('null')
            unselect = 0
        except ValueError :
            print("\nInvalid choice.")

    if product == 1 :
        print("\nProcessing...")
        tescoPrices = dataPull('URL_STORE/TESCO/STILL_WATER.txt', tescoData, 'null', "/100ml", 'null')
        sainsburysPrices = dataPull('URL_STORE/SAINSBURYS/STILL_WATER.txt', sainsburysData, '<a href="http://www.sainsburys.co.uk/shop/gb/groceries/still-water/', "/100ml", 'null')
        waitrosePrices = dataPull('URL_STORE/WAITROSE/STILL_WATER.txt', waitroseData, 'null', "/100ml", 4)

    if product == 2 :
        print("\nProcessing...")
        tescoPrices = dataPull('URL_STORE/TESCO/SPARKLING_WATER.txt', tescoData, 'null', "/100ml", 'null')
        sainsburysPrices = dataPull('URL_STORE/SAINSBURYS/SPARKLING_WATER.txt', sainsburysData, '<a href="http://www.sainsburys.co.uk/shop/gb/groceries/sparkling-water/', "/100ml", 'null')
        waitrosePrices = dataPull('URL_STORE/WAITROSE/SPARKLING_WATER.txt', waitroseData, 'null', "/100ml", 2)

    if product == 3 :
        print("\nProcessing...")
        tescoPrices = dataPull('URL_STORE/TESCO/EVERYDAY_TEA.txt', tescoData, 'null', "/100g", 'null')
        sainsburysPrices = dataPull('URL_STORE/SAINSBURYS/EVERYDAY_TEA.txt', sainsburysData, '<a href="http://www.sainsburys.co.uk/shop/gb/groceries/tea', "/100g", 'null')
        waitrosePrices = dataPull('URL_STORE/WAITROSE/EVERYDAY_TEA.txt', waitroseData, 'null', "/100g", 3)
		
    if product == 4 :
        print("\nProcessing...")
        tescoPrices = dataPull('URL_STORE/TESCO/MILK.txt', tescoData, 'null', "/100ml", 'null')
        sainsburysPrices = dataPull('URL_STORE/SAINSBURYS/MILK.txt', sainsburysData, '<a href="http://www.sainsburys.co.uk/shop/gb/groceries/fresh-milk', "/100ml", 'null')
        waitrosePrices = dataPull('URL_STORE/WAITROSE/MILK.txt', waitroseData, 'null', "/100ml", 5)

if proType == 'f' :
    print("\nEnter 1 to compare prices for white bread.")
    print("Enter 2 to compare prices for brown bread.")
    print("Enter 3 to compare prices for cereal bars.")
    print("Enter 4 to compare prices for eggs.")
    print("Enter 5 to compare prices for crisps.")
    print("Enter 6 to compare prices for butter.")
	
    unselect = 1

    while unselect == 1 :
        try :
            product = int(input("\nChoose a product to compare: "))
            if (1 <= product <= 6) is False : int('null')
            unselect = 0
        except ValueError :
            print("\nInvalid choice.")

    if product == 1 :
        print("\nProcessing...")
        tescoPrices = dataPull('URL_STORE/TESCO/WHITE_BREAD.txt', tescoData, 'null', "/100g", 'null')
        sainsburysPrices = dataPull('URL_STORE/SAINSBURYS/WHITE_BREAD.txt', sainsburysData, '<a href="http://www.sainsburys.co.uk/shop/gb/groceries/white-bread/', "/100g", 'null')
        waitrosePrices = dataPull('URL_STORE/WAITROSE/WHITE_BREAD.txt', waitroseData, 'null', "/100g", 2)

    if product == 2 :
        print("\nProcessing...")
        tescoPrices = dataPull('URL_STORE/TESCO/BROWN_BREAD.txt', tescoData, 'null', "/100g", 'null')
        sainsburysPrices = dataPull('URL_STORE/SAINSBURYS/BROWN_BREAD.txt', sainsburysData, '<a href="http://www.sainsburys.co.uk/shop/gb/groceries/wholemeal-brown-bread/', "/100g", 'null')
        waitrosePrices = dataPull('URL_STORE/WAITROSE/BROWN_BREAD.txt', waitroseData, 'null', "/100g", 2)

    if product == 3 :
        print("\nProcessing...")
        tescoPrices = dataPull('URL_STORE/TESCO/CEREAL_BARS.txt', tescoData, 'null', "/100g", 'null')
        sainsburysPrices = dataPull('URL_STORE/SAINSBURYS/CEREAL_BARS.txt', sainsburysData, '<a href="http://www.sainsburys.co.uk/shop/gb/groceries/breakfast-cereal-bars-breakfast-biscuits', "/100g", 'null')
        waitrosePrices = dataPull('URL_STORE/WAITROSE/CEREAL_BARS.txt', waitroseData, 'null', "/100g", 3)
		
    if product == 4 :
        print("\nProcessing...")
        tescoPrices = dataPull('URL_STORE/TESCO/EGGS.txt', tescoData, 'null', "/100g", 'null')
        sainsburysPrices = dataPull('URL_STORE/SAINSBURYS/EGGS.txt', sainsburysData, '<a href="http://www.sainsburys.co.uk/shop/gb/groceries/dairy-eggs-chilled/fresh-milk-eggs', "/100g", 'null')
        waitrosePrices = dataPull('URL_STORE/WAITROSE/EGGS.txt', waitroseData, 'null', "/100g", 1)

    if product == 5 :
        print("\nProcessing...")
        tescoPrices = dataPull('URL_STORE/TESCO/CRISPS.txt', tescoData, 'null', "/100g", 'null')
        sainsburysPrices = dataPull('URL_STORE/SAINSBURYS/CRISPS.txt', sainsburysData, '<a href="http://www.sainsburys.co.uk/shop/gb/groceries/food-cupboard/crisps-nuts-snacking-fruit', "/100g", 'null')
        waitrosePrices = dataPull('URL_STORE/WAITROSE/CRISPS.txt', waitroseData, 'null', "/100g", 4)

    if product == 6 :
        print("\nProcessing...")
        tescoPrices = dataPull('URL_STORE/TESCO/BUTTER.txt', tescoData, 'null', "/100g", 'null')
        sainsburysPrices = dataPull('URL_STORE/SAINSBURYS/BUTTER.txt', sainsburysData, '<a href="http://www.sainsburys.co.uk/shop/gb/groceries/dairy-eggs-chilled/butter-spreads-baking', "/100g", 'null')
        waitrosePrices = dataPull('URL_STORE/WAITROSE/BUTTER.txt', waitroseData, 'null', "/100g", 2)


# Create aggregate lists
allPrices = []
cheapest = []

if tescoPrices != [] :
    allPrices += tescoPrices
    cheapest += lowestPrices(tescoPrices)
else : print("All operations for Tesco failed. No results for Tesco will be displayed.")
if sainsburysPrices != [] :
    allPrices += sainsburysPrices
    cheapest += lowestPrices(sainsburysPrices)
else : print("All operations for Sainsbury's failed. No results for Sainsbury's will be displayed.")
if waitrosePrices != [] :
    allPrices += waitrosePrices
    cheapest += lowestPrices(waitrosePrices)
else : print("All operations for Waitrose failed. No results for Waitrose will be displayed.")

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
