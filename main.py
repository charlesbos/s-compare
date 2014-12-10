"""
main.py

See CHANGELOG - now added to git

Created by Charles Bos on 2014-12-05
"""

from tesco import tescoData
from sainsburys import sainsburysData

tescoPrices = tescoData()
sainsburysPrices = sainsburysData()

print("The cheapest water from Tesco:", tescoPrices[0])
print("The cheapest water from Sainsbury's:", sainsburysPrices[0])

print("\nThe cheapest water overall:", min([tescoPrices[0], sainsburysPrices[0]]))
