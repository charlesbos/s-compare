"""
tesco.py

This modules extracts prices and item titles from a valid Tesco store page
url and then returns that data.

Created by: Charles Bos
Contributors: Charles Bos
"""
from fetcher import htmlFetch

def tescoData(url, unit) :
    '''
    Extract Tesco line prices and item titles
    Two arguments are accepted. The first is a url which can be passed to the htmlFetch function.
    The second is a unit to append to the extracted prices.
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
            priceEnd = priceStart + 6
            priceExtract = htmlString[priceStart:priceEnd].strip('()') + unit
            priceList = [priceExtract]
            
            while priceStart != 27 :
                priceStart = htmlString.find('<span class="linePriceAbbr">', priceEnd) + 28
                priceEnd = priceStart + 6
                priceExtract = htmlString[priceStart:priceEnd].strip('()') + unit
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

        # Remove unavailable products
        counter = 0

        while (counter + 1) < 19 :
            start = htmlString.find(titleList[counter])
            end = htmlString.find(titleList[counter + 1])
            if htmlString.find('Sorry, this product is currently not available.', start, end) != -1 :
                del titleList[counter]
            counter += 1

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

            if tescoList == [] :
                print("TescoError: unspecified extraction error.")
                return 'null'
            else :
                print("Operation for Tesco completed successfully.")
                return tescoList


                            


                    


