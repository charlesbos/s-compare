"""
main.py

This file imports the various modules for each shop, calls the functions and
then outputs the data returned by them.

Created by: Charles Bos
Contributors: Charles Bos
"""

from tesco import tescoData
from sainsburys import sainsburysData

tescoPrices = tescoData("http://www.tesco.com/groceries/product/browse/default.aspx?N=4294792641&Ne=4294793660")
sainsburysPrices = sainsburysData("http://www.sainsburys.co.uk/shop/gb/groceries/drinks/still-water#langId=44&storeId=10151&catalogId=10122&categoryId=12351&parent_category_rn=12192&top_category=12192&pageSize=30&orderBy=FAVOURITES_FIRST&searchTerm=&beginIndex=0")

print("The cheapest water from Tesco:", tescoPrices[0])
print("The cheapest water from Sainsbury's:", sainsburysPrices[0])

print("\nThe cheapest water overall:", min([tescoPrices[0], sainsburysPrices[0]]))
