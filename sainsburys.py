"""
sainsburys.py

This modules extracts prices and item titles from a valid Sainsburys store page
url and then returns that data.
"""
from fetcher import simpleFetch

def sainsburysData(url, titletag, unit, scroll) :
    '''
    Extract Sainsburys prices per measure and item titles.
    Three arguments are accepted. The first is a url which can be passed to the htmlFetch function.
    The second is a unit to append to the extracted prices.
    from the fetcher module. The third is the fragment of html that marks the beginning
    of an item title. The fourth is not needed by this function and is specified
    for compatibility reasons only.
    '''

    htmlString = simpleFetch(url)

    if htmlString == 'null' :
        print("SainsburysError: failed to retrieve webpage.")
        return 'null'
    else :
        # Extract prices
        priceList = []
        priceStart = htmlString.find('<p class="pricePerMeasure">')
        priceEnd = htmlString.find('<abbr', priceStart)
        
        while (0 <= priceStart <= len(htmlString)) is True :
            priceExtract = htmlString[priceStart + 27:priceEnd] + unit
            mercCheckA = htmlString.find('merchandising_associations', priceStart - 1000, priceStart)
            mercCheckB = htmlString.find('<div class="crossSell">', priceStart - 1000, priceStart)  
            if (mercCheckA == -1) and (mercCheckB == -1) :
                priceList += [priceExtract]
            priceStart = htmlString.find('<p class="pricePerMeasure">', priceEnd)
            priceEnd = htmlString.find('<abbr', priceStart)

        # Extract titles
        titleList = []
        titleStart = htmlString.find(titletag)
        titleEnd = htmlString.find('<img alt=', titleStart)

        while (0 <= titleStart <= len(htmlString)) is True :
            titleExtract = htmlString[titleStart + len(titletag):titleEnd].partition(' ')[-1].partition('\r\n')[0].strip(' ').replace('&amp;', '&')
            titleList += [titleExtract]
            titleStart = htmlString.find(titletag, titleEnd)
            titleEnd = htmlString.find('<img alt=', titleStart)

        titleList = [x for x in titleList if x != '']

        # Extract promotion titles
        proTitleList = []
        proTitleStart = htmlString.find('''<a href="http://www.sainsburys.co.uk/shop/ProductDisplay?''')
        proTitleEnd = htmlString.find('<img alt=', proTitleStart)

        while (0 <= proTitleStart <= len(htmlString)) is True :
            proTitleExtract = htmlString[proTitleStart + 57:proTitleEnd].partition(' ')[-1].partition('\r\n')[0].strip(' ').replace('&amp;', '&')
            proTitleList += [proTitleExtract]
            proTitleStart = htmlString.find('''<a href="http://www.sainsburys.co.uk/shop/ProductDisplay?''', proTitleEnd)
            proTitleEnd = htmlString.find('<img alt=', proTitleStart)

        proTitleList = [x for x in proTitleList if x != '']

        # Uncomment for debugging purposes
        # print(len(priceList))
        # print(len(titleList))

        # Merge titles and promotion titles
        titleList = sorted(titleList + proTitleList)

        # Merge the two lists into one list of tuples and return it
        if len(priceList) != len(titleList) :
            print("SainsburysError: lengths of prices and item titles do not match.")
            return 'null'
        else :
            return [list(x) for x in zip(titleList, priceList, ["Sainsburys"] * len(priceList))]


                            


                    


