"""
main.py

See CHANGELOG - now added to git

Created by Charles Bos on 2014-12-05
"""

from tesco import tescoData
from sainsburys import sainsburysData

print("Please choose a shop.")
print("The choices are: Tesco (t) and Sainsburys (s)")

chooseShop = input("[t/s]: ")

if chooseShop == 't' :
    print(tescoData())
if chooseShop == 's' :
    print(sainsburysData())
