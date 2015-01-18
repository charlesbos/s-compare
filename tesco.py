"""
tesco.py

This modules extracts prices and item titles from a valid Tesco store page
url and then returns that data.
"""
from fetcher import simpleFetch

def tescoData(url, titletag, unit, scroll) :
    '''
    Extract Tesco prices per measure and item titles.
    Three arguments are accepted. The first is a url which can be passed to the htmlFetch function.
    The second is a unit to append to the extracted prices.
    from the fetcher module. The third and fourth are not used in this function
    at all and are specified for compatibility reasons only.
    '''

    htmlString = simpleFetch(url)

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
            priceEnd = htmlString.find('/', priceStart)
            priceExtract = htmlString[priceStart:priceEnd].strip('()') + unit
            measureCheck = htmlString[priceEnd:priceEnd + 5]
            if measureCheck == '/75cl' :
                temp = str('{:.2f}'.format(((float(htmlString[priceStart:priceEnd].strip('()')[1:]) / 30) * 4)))
                priceExtract = '£' + temp + unit
            if (measureCheck == '/l)</') or (measureCheck == '/kg)<') :
                temp = str('{:.2f}'.format((float(htmlString[priceStart:priceEnd].strip('()')[1:]) / 10)))
                priceExtract = '£' + temp + unit
            priceList = [priceExtract]
            
            while priceStart != 27 :
                priceStart = htmlString.find('<span class="linePriceAbbr">', priceEnd) + 28
                priceEnd = htmlString.find('/', priceStart)
                priceExtract = htmlString[priceStart:priceEnd].strip('()') + unit
                measureCheck = htmlString[priceEnd:priceEnd + 5]
                if measureCheck == '/75cl' :
                    temp = str('{:.2f}'.format(((float(htmlString[priceStart:priceEnd].strip('()')[1:]) / 30) * 4)))
                    priceExtract = '£' + temp + unit
                if (measureCheck == '/l)</') or (measureCheck == '/kg)<') :
                    temp = str('{:.2f}'.format((float(htmlString[priceStart:priceEnd].strip('()')[1:]) / 10)))
                    priceExtract = '£' + temp + unit
                priceList.extend([priceExtract])

            priceList = priceList[:-1]

        # Extract titles
        titleStart = htmlString.find('<span data-title="true">') + 24

        if titleStart == -1 :
            print("TescoError: failed to extract item titles.")
            return 'null'
        else :
            titleEnd = htmlString.find('</span>')
            titleExtract = htmlString[titleStart:titleEnd].partition('&gt;')[0]
            itemExistCheck = htmlString.find('Sorry, this product is currently not available.', titleEnd, titleEnd + 200)
            if itemExistCheck == -1 :
                titleList = [titleExtract]

            while titleStart != 23 :
                titleStart = htmlString.find('<span data-title="true">', titleEnd) + 24
                titleEnd = htmlString.find('</span></a></h2>', titleStart)
                titleExtract = htmlString[titleStart:titleEnd].partition('&gt;')[0]
                itemExistCheck = htmlString.find('Sorry, this product is currently not available.', titleEnd, titleEnd + 200)
                if itemExistCheck == -1 :
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

            if tescoList == [] :
                print("TescoError: unspecified extraction error.")
                return 'null'
            else :
                return tescoList


                            


                    


