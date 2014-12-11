"""
main.py

This file imports the various modules for each shop, calls the functions and
then outputs the data returned by them.

Created by: Charles Bos
Contributors: Charles Bos
"""
from tesco import tescoData
from sainsburys import sainsburysData

def lowestPrices(priceList) :
    '''
    This function extracts the minimum values from a dictionary and then the keys to
    match. Then it creates a new dictionary from the two lists.
    '''
    minKeys = [keys for keys, values in priceList.items() if values == min(priceList.values())]   
    minVals =  [min(priceList.values())] * len(minKeys)
            
    return dict(zip(minKeys, minVals))

def cheapestFrom() :
    '''
    A way of finding which shop the lowest price came from as this information
    is not preserved when merging our lists.
    No arguments taken.
    '''
    if tescoPrices[cheapestItem] != None : return "Tesco"
    if lowestPriceDic[cheapestItem] != None : return "Sainsbury's"

# Call functions from the shop modules to extract item titles and prices
tescoPrices = tescoData("http://www.tesco.com/groceries/product/browse/default.aspx?N=4294792641&Ne=4294793660")
sainsburysPrices = sainsburysData("http://www.sainsburys.co.uk/shop/gb/groceries/drinks/still-water#langId=44&storeId=10151&catalogId=10122&categoryId=12351&parent_category_rn=12192&top_category=12192&pageSize=30&orderBy=FAVOURITES_FIRST&searchTerm=&beginIndex=0")

# Display data
cheapestTesco = lowestPrices(tescoPrices)
cheapestSainsburys = lowestPrices(sainsburysPrices)

print("The cheapest water from Tesco:", cheapestTesco)
print("The cheapest water from Sainsbury's:", cheapestSainsburys)

cheapByShop = dict(list(cheapestTesco.items()) + list(cheapestSainsburys.items()))
cheapestOverall = lowestPrices(cheapByShop)
cheapestItem = list(cheapestOverall.keys())[0]

print("\nThe cheapest water overall:", cheapestOverall, "from", cheapestFrom())
