"""
main.py

This file imports the various modules for each shop, calls the functions and
then outputs the data returned by them.

Created by: Charles Bos
Contributors: Charles Bos
"""
from tesco import tescoData
from sainsburys import sainsburysData
from operator import itemgetter

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

def cheapPerShop(shopPrices, shopTitle) :
    '''
    A function to append the cheapest items per shop to the output file.
    Two arguments are taken. The first is the list of tuples containing the
    item titles and prices. The second is the title of the shop.
    '''
    file = open('OUTPUT.txt', 'a')

    if shopPrices != 'null' :
        cheapest = lowestPrices(shopPrices)

        print("\n== The cheapest product from", shopTitle,"==", file = file)

        counter = 0
        length = len(cheapest)

        while counter < length :
            print('{:55s}'.format(cheapest[counter][0]), '{:15s}'.format(cheapest[counter][1]), file = file)
            counter += 1
            
    file.close()

# Call functions from the shop modules to extract item titles and prices
tescoPrices = tescoData("http://www.tesco.com/groceries/product/browse/default.aspx?N=4294792641&Ne=4294793660", "/100ml")
sainsburysPrices = sainsburysData("http://www.sainsburys.co.uk/shop/gb/groceries/drinks/still-water#langId=44&storeId=10151&catalogId=10122&categoryId=12351&parent_category_rn=12192&top_category=12192&pageSize=30&orderBy=FAVOURITES_FIRST&searchTerm=&beginIndex=0", '''<a href="http://www.sainsburys.co.uk/shop/gb/groceries/still-water/''', "/100ml")

# Write sorted table of prices to a file called OUTPUT.txt
prices = []

if tescoPrices != 'null' : prices += tescoPrices
else : print("Operation for Tesco failed. No results for Tesco will be displayed.")
if sainsburysPrices != 'null' : prices += sainsburysPrices
else : print("Operation for Sainsbury's failed. No results for Sainsbury's will be displayed.")

if prices != [] :
    file = open('OUTPUT.txt', 'w')
    
    sortedPrices = sorted(prices, key=itemgetter(1,0))

    length = len(sortedPrices)
    counter = 0

    while counter < length :
        print('{:55s}'.format(sortedPrices[counter][0]), '{:15s}'.format(sortedPrices[counter][1]), sortedPrices[counter][2],  file = file)
        counter += 1

    file.close()

    # Append cheapest product for each individual shop to the ouput file
    cheapPerShop(tescoPrices, 'Tesco')
    cheapPerShop(sainsburysPrices, "Sainsbury's")

    # Output message to inform user that program has finished working
    print("\nProcessing completed! Please see the file 'OUTPUT.txt'.")
else : print("\nAll operations failed. No data to display.")
