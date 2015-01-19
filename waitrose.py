"""
waitrose.py

This modules extracts prices and item titles from a valid Waitrose store page
url and then returns that data.
"""
from fetcher import waitroseFetch

def waitroseData(url, titletag, unit, scroll) :
    '''
    Extract Waitrose prices per measure and item titles.
    Three arguments are accepted. The first is a url which can be passed to the htmlFetch function.
    The second is a unit to append to the extracted prices.
    from the fetcher module. The third is not used in this function
    at all and is specified for compatibility reasons only. The fourth is the number of times that
    the page needs to be scrolled in order for the html to be generated.
    '''

    htmlString = waitroseFetch(url, scroll)

    if htmlString == 'null' :
        print("WaitroseError: failed to retrieve webpage.")
        return 'null'
    else :
        # Extract prices
        priceList = []
        priceStart = htmlString.find('<span class="fine-print">(')
        priceEnd = htmlString.find('p per', priceStart)
        
        while (0 <= priceStart <= len(htmlString)) is True :
            litreCheck = htmlString.find('per litre', priceEnd, priceEnd + 10)
            if litreCheck == -1 :
                try :
                    priceExtract = '£' + str('{:.2f}'.format((float(htmlString[priceStart + 26:priceEnd]) / 100), 2)) + unit
                except ValueError :
                    priceEnd = priceEnd = htmlString.find(' per', priceStart)
                    priceExtract = '£' + str('{:.2f}'.format(float(htmlString[priceStart + 26:priceEnd][1:]), 2)) + unit
            else : priceExtract = '£' + str('{:.2f}'.format((float(htmlString[priceStart:priceEnd][1:]) / 100), 2)) + unit
            priceList += [priceExtract]
            priceStart = htmlString.find('<span class="fine-print">(', priceEnd)
            priceEnd = htmlString.find('p per', priceStart)

        # Extract titles
        titleList = []
        titleStart = htmlString.find('<div alt="')
        titleEnd = htmlString.find('" ', titleStart)

        while (0 <= titleStart <= len(htmlString)) is True :
            addMeasureStart = htmlString.find('<div class="m-product-volume">', titleEnd) + 30
            addMeasureEnd = htmlString.find('</div>', addMeasureStart)
            titleExtract = str(htmlString[titleStart + 10:titleEnd] + ' ' + htmlString[addMeasureStart:addMeasureEnd]).replace('amp;', '').replace('&#039;', "'")
            priceExistCheck = htmlString.find('<span class="fine-print"> </span>', titleStart, titleStart + 1550)
            if priceExistCheck == -1 :
                titleList += [titleExtract]
            titleStart = htmlString.find('<div alt="', titleEnd)
            titleEnd = htmlString.find('" ', titleStart)

        titleList = [x for x in titleList if x != '']

        # Merge the two lists into one list of tuples and return it
        if len(priceList) != len(titleList) :
            print("WaitroseError: lengths of prices and item titles do not match.")
            return 'null'
        else :
            return [list(x) for x in zip(titleList, priceList, ["Waitrose"] * len(priceList))]

                            


                    


