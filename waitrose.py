"""
waitrose.py

This modules extracts prices and item titles from a valid Waitrose store page
url and then returns that data.
"""
from fetcher import waitroseFetch
from time import strftime

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

    if (htmlString == '<html><head></head><body></body></html>') or (htmlString == 'null') :
        errorTime = strftime('%H:%M:%S %Y-%m-%d')
        errorMessage = "WaitroseError: failed to retrieve webpage."
        return errorTime + '\n' + errorMessage + '\n' + '-' * 80
    else :
        # Extract prices
        priceList = []
        priceStart = htmlString.find('<span class="fine-print">(')
        priceEnd = htmlString.find('p ', priceStart)
        
        while (0 <= priceStart <= len(htmlString)) is True :
            litreCheck = htmlString.find('per litre', priceStart, priceStart + 100)
            kiloCheck = htmlString.find('per kg', priceStart, priceStart + 100)
            try :
                if (litreCheck == -1) and (kiloCheck == -1) :
                    try :
                        priceExtract = '£' + str('{:.2f}'.format((float(htmlString[priceStart + 26:priceEnd]) / 100), 2)) + unit
                    except ValueError :
                        priceEnd = htmlString.find(' per', priceStart)
                        priceExtract = '£' + str('{:.2f}'.format(float(htmlString[priceStart + 26:priceEnd][1:]), 2)) + unit
                else :
                    try :
                        priceEnd = htmlString.find('p ', priceStart)
                        priceExtract = '£' + str('{:.2f}'.format((float(htmlString[priceStart + 26:priceEnd]) / 1000), 2)) + unit
                    except ValueError :
                        priceEnd = htmlString.find(' per', priceStart)
                        priceExtract = '£' + str('{:.2f}'.format((float(htmlString[priceStart + 26:priceEnd][1:]) / 10), 2)) + unit
            except ValueError :
                errorTime = strftime('%H:%M:%S %Y-%m-%d')
                errorMessage = "WaitroseError: prices could not successfully be converted to a standard unit"
                return errorTime + '\n' + errorMessage + '\n' + '-' * 80
            if unit == '/each' :
                parityCheck = htmlString[priceEnd + 2:htmlString.find(')', priceEnd)]
                if parityCheck == unit[1:] : priceList += [priceExtract]
            else : priceList += [priceExtract]
            priceStart = htmlString.find('<span class="fine-print">(', priceEnd)
            priceEnd = htmlString.find('p ', priceStart)

        # Extract titles
        titleList = []
        titleStart = htmlString.find('<div alt="')
        titleEnd = htmlString.find('" ', titleStart)

        while (0 <= titleStart <= len(htmlString)) is True :
            addMeasureStart = htmlString.find('<div class="m-product-volume">', titleEnd) + 30
            addMeasureEnd = htmlString.find('</div>', addMeasureStart)
            titleExtract = str(htmlString[titleStart + 10:titleEnd] + ' ' + htmlString[addMeasureStart:addMeasureEnd]).replace('amp;', '').replace('&#039;', "'")
            priceExistCheck = htmlString.find('<span class="fine-print"> </span>', titleStart, titleStart + 2000)
            if unit == '/each' :
                parityCheckStart = htmlString.find('<span class="fine-print">(', titleEnd)
                parityCheckEnd = htmlString.find(')', parityCheckStart)               
                parityCheck = htmlString[parityCheckStart + 20:parityCheckEnd].partition(' ')[-1]
                if (priceExistCheck == -1) and (parityCheck == unit[1:]) : titleList += [titleExtract]
            elif priceExistCheck == -1 : titleList += [titleExtract]
            titleStart = htmlString.find('<div alt="', titleEnd)
            titleEnd = htmlString.find('" ', titleStart)

        titleList = [x for x in titleList if x != '']

        # Merge the two lists into one list of tuples and return it
        if len(priceList) != len(titleList) :
            errorTime = strftime('%H:%M:%S %Y-%m-%d')
            errorMessage = "WaitroseError: lengths of prices and item titles do not match."
            listLengths = 'priceList length = ' + str(len(priceList)) + '\n' + 'titleList length = ' + str(len(titleList))
            return errorTime + '\n' + errorMessage + '\n' + listLengths + '\n' + '-' * 80
        else :
            return [list(x) for x in zip(titleList, priceList, ["Waitrose"] * len(priceList))]

                            


                    


