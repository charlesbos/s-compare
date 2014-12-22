"""
tesco.py

This modules extracts prices and item titles from a valid Tesco store page
url and then returns that data.

Created by: Charles Bos
Contributors: Charles Bos
"""
from fetcher import htmlFetch

def tescoData(url) :
    '''
    Extract Tesco line prices and item titles
    One argument accepted, a url which can be passed to the htmlFetch function
    from the fetcher module.
    '''

    htmlString = htmlFetch(url)

    if htmlString == 'null' :
        print("TescoError: failed to retrieve webpage.")
        return 'null'
    else :
        # Extract prices
        priceStart = htmlString.find('<span class="linePriceAbbr">') + 28

        if priceStart == -1 :
            print("TescoError: failed to extract prices.")
            return 'null'
        else :
            priceEnd = priceStart + 13
            priceExtract = htmlString[priceStart:priceEnd].strip('()')
            priceList = [priceExtract]
            
            while priceStart != 27 :
                priceStart = htmlString.find('<span class="linePriceAbbr">', priceEnd) + 28
                priceEnd = priceStart + 13
                priceExtract = htmlString[priceStart:priceEnd].strip('()')
                priceList.extend([priceExtract])

            priceList = priceList[:-1]

        # Extract titles
        titleStart = htmlString.find('<span data-title="true">') + 24

        if titleStart == -1 :
            print("TescoError: failed to extract item titles.")
            return 'null'
        else :
            titleEnd = htmlString.find('</span>')
            titleExtract = htmlString[titleStart:titleEnd]
            titleList = [titleExtract]

            while titleStart != 23 :
                titleStart = htmlString.find('<span data-title="true">', titleEnd) + 24
                titleEnd = htmlString.find('</span></a></h2>', titleStart)
                titleExtract = htmlString[titleStart:titleEnd]
                titleList.extend([titleExtract])

            titleList = titleList[1:-1]

        # Merge the two lists into one list of tuples and return it
        if len(priceList) != len(titleList) :
            print("TescoError: lengths of prices and item titles do not match.")
            return 'null'
        else :
            tescoList = []
            counter = 0

            while counter < len(priceList) :
                tescoList.append((titleList[counter], priceList[counter], "Tesco"))
                counter += 1

            return tescoList


                            


                    


