"""
tesco.py

This modules extracts prices and item titles from a valid Tesco store page
url and then returns that data.
"""
from fetcher import simpleFetch
from time import strftime

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
        errorTime = strftime('%H:%M:%S %Y-%m-%d')
        errorMessage = "TescoError: failed to retrieve webpage."
        return errorTime + '\n' + errorMessage + '\n' + '-' * 80
    else :
        # Extract prices
        priceList = []
        priceStart = htmlString.find('<span class="linePriceAbbr">')
        priceEnd = htmlString.find('/', priceStart)
        
        while (0 <= priceStart <= len(htmlString)) is True :
            priceExtract = htmlString[priceStart + 28:priceEnd].strip('()') + unit
            measureCheck = htmlString[priceEnd:priceEnd + 5]
            if measureCheck == '/75cl' :
                priceExtract = '£' + str('{:.2f}'.format(((float(htmlString[priceStart + 28:priceEnd].strip('()')[1:]) / 30) * 4))) + unit
            if (measureCheck == '/l)</') or (measureCheck == '/kg)<') :
                priceExtract = '£' + str('{:.2f}'.format((float(htmlString[priceStart + 28:priceEnd].strip('()')[1:]) / 10))) + unit
            priceList += [priceExtract]
            priceStart = htmlString.find('<span class="linePriceAbbr">', priceEnd)
            priceEnd = htmlString.find('/', priceStart)

        # Extract titles
        titleList = []
        titleStart = htmlString.find('<span data-title="true">') + 24
        titleEnd = htmlString.find('</span>')

        while (0 <= titleStart <= len(htmlString)) is True :
            titleExtract = htmlString[titleStart + 24:titleEnd].partition('&gt;')[0]
            itemExistCheck = htmlString.find('Sorry, this product is currently not available.', titleEnd, titleEnd + 500)
            if itemExistCheck == -1 :
                titleList += [titleExtract]
            titleStart = htmlString.find('<span data-title="true">', titleEnd)
            titleEnd = htmlString.find('</span></a></h2>', titleStart)

        titleList = [x for x in titleList if x != '']

        # Merge the two lists into one list of tuples and return it
        if len(priceList) != len(titleList) :
            errorTime = strftime('%H:%M:%S %Y-%m-%d')
            errorMessage = "TescoError: lengths of prices and item titles do not match."
            listLengths = 'priceList length = ' + str(len(priceList)) + '\n' + 'titleList length = ' + str(len(titleList))
            return errorTime + '\n' + errorMessage + '\n' + listLengths + '\n' + '-' * 80
        else :
            return [list(x) for x in zip(titleList, priceList, ["Tesco"] * len(priceList))]


                            


                    


