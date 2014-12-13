"""
main.py

This file imports the various modules for each shop, calls the functions and
then outputs the data returned by them.

We built this program! We built this program on Py-thon 3!

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

# Call functions from the shop modules to extract item titles and prices
tescoPrices = tescoData("http://www.tesco.com/groceries/product/browse/default.aspx?N=4294792641&Ne=4294793660")
sainsburysPrices = sainsburysData("http://www.sainsburys.co.uk/shop/gb/groceries/drinks/still-water#langId=44&storeId=10151&catalogId=10122&categoryId=12351&parent_category_rn=12192&top_category=12192&pageSize=30&orderBy=FAVOURITES_FIRST&searchTerm=&beginIndex=0")

# Write sorted table of prices to a file called OUTPUT.txt
file = open('OUTPUT.txt', 'w')

prices = sainsburysPrices + tescoPrices
sortedPrices = sorted(prices, key=itemgetter(1,0))

length = len(sortedPrices)
counter = 0

while counter < length :
    print('{:55s}'.format(sortedPrices[counter][0]), '{:15s}'.format(sortedPrices[counter][1]), sortedPrices[counter][2],  file = file)
    counter += 1

file.close()

# Append cheapest water for each individual shop to the ouput file
file = open('OUTPUT.txt', 'a')

cheapestTesco = lowestPrices(tescoPrices)
cheapestSainsburys = lowestPrices(sainsburysPrices)

print("\n== The cheapest water from Tesco ==", file = file)

counter = 0
length = len(cheapestTesco)

while counter < length :
    print('{:55s}'.format(cheapestTesco[counter][0]), '{:15s}'.format(cheapestTesco[counter][1]), file = file)
    counter += 1

print("\n== The cheapest water from Sainsbury's ==", file = file)

counter = 0
length = len(cheapestSainsburys)

while counter < length :
    print('{:55s}'.format(cheapestSainsburys[counter][0]), '{:15s}'.format(cheapestSainsburys[counter][1]), file = file)
    counter += 1

file.close()

# Output message to inform user that program has finished working
print("\nProcessing completed! Please see the file 'OUTPUT.txt'.")
