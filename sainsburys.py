"""
sainsburys.py

This modules extracts prices and item titles from a valid Sainsburys store page
url and then returns that data.
"""
from fetcher import simpleFetch
from time import strftime

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
        errorTime = strftime('%H:%M:%S %Y-%m-%d')
        errorMessage = "SainsburysError: failed to retrieve webpage."
        return errorTime + '\n' + errorMessage + '\n' + url + '\n' + '-' * 80
    else :
        # Extract prices
        priceList = []
        priceStart = htmlString.find('<p class="pricePerMeasure">')
        priceEnd = htmlString.find('<abbr', priceStart)
        prevItem = 0
        
        while 0 <= priceStart <= len(htmlString) :
            mCheckStart = htmlString.find('class="pricePerMeasureMeasure">', priceEnd)
            mCheckEnd = htmlString.find('</span></abbr>', mCheckStart)
            if (htmlString[mCheckStart + 31:mCheckEnd] == 'kg') or (htmlString[mCheckStart + 31:mCheckEnd] == 'ltr') :
                priceExtract = '£' + str('{:.2f}'.format((float(htmlString[priceStart + 28:priceEnd]) / 10))) + unit
            else : priceExtract = htmlString[priceStart + 27:priceEnd] + unit
            mercCheck = (htmlString.find('merchandising_associations', priceStart - 1000, priceStart) == -1) and (htmlString.find('<div class="crossSell">', priceStart - 1000, priceStart) == -1)
            if mercCheck : priceList += [priceExtract]
            priceStart = htmlString.find('<p class="pricePerMeasure">', priceEnd)
            priceEnd = htmlString.find('<abbr', priceStart)

        # Extract standard titles and promotion titles
        titleList = []
        titleStart = htmlString.find(titletag)
        titleEnd = htmlString.find('<img alt=', titleStart)

        while 0 <= titleStart <= len(htmlString) :
            titleExtract = htmlString[titleStart + len(titletag):titleEnd].partition(' ')[-1].partition('\r\n')[0].strip(' ').replace('amp;', '')
            titleList += [titleExtract]
            titleStart = htmlString.find(titletag, titleEnd)
            titleEnd = htmlString.find('<img alt=', titleStart)

        proTitleList = []
        proTitleStart = htmlString.find('''<a href="http://www.sainsburys.co.uk/shop/ProductDisplay?''')
        proTitleEnd = htmlString.find('<img alt=', proTitleStart)

        while 0 <= proTitleStart <= len(htmlString) :
            proTitleExtract = htmlString[proTitleStart + 57:proTitleEnd].partition(' ')[-1].partition('\r\n')[0].strip(' ').replace('amp;', '')
            mercCheck = htmlString.find('merchandising_associations', proTitleStart - 3000, proTitleStart) == -1
            if mercCheck : proTitleList += [proTitleExtract]
            proTitleStart = htmlString.find('''<a href="http://www.sainsburys.co.uk/shop/ProductDisplay?''', proTitleEnd)
            proTitleEnd = htmlString.find('<img alt=', proTitleStart)
            
        if proTitleList != [] : titleList = sorted(titleList + proTitleList)

        titleList = [x for x in titleList if x != '']

        # Merge the two lists into one list of tuples and return it
        if len(priceList) != len(titleList) :
            errorTime = strftime('%H:%M:%S %Y-%m-%d')
            errorMessage = "SainsburysError: lengths of prices and item titles do not match."
            listLengths = 'priceList length = ' + str(len(priceList)) + '\n' + 'titleList length = ' + str(len(titleList))
            return errorTime + '\n' + errorMessage + '\n' + listLengths + '\n' + url + '\n' + '-' * 80
        else : return [list(x) for x in zip(titleList, priceList, ["Sainsburys"] * len(priceList))]
