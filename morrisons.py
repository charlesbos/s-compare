"""
morrisons.py

This module extracts prices and item titles from a valid Morrisons store page
url and then returns that data.
"""
from fetcher import simpleFetch
from time import strftime

def morriData(url, titletag, unit, scroll) :
    '''
    Extracts a list of item prices and a list of item titles. Will try and return a
    tuple containing the aforementioned lists plus a list containing the shop name.
    Titletag and scroll args are not used and are specified for compatibilty reasons only.
    '''
    htmlString = simpleFetch(url)
    
    if htmlString == "null" :
        errorTime = strftime('%H:%M:%S %Y-%m-%d')
        errorMessage = "MorrisonsError: failed to retrieve webpage."
        return errorTime + '\n' + errorMessage + '\n' + url + '\n' + '-' * 80 
    else :
        # Extract prices
        priceList = []
        priceStart = htmlString.find('<p class="pricePerWeight">')
        priceEnd = htmlString.find('</p>', priceStart)

        while 0 <= priceStart <= len(htmlString) :
            priceExtract = htmlString[priceStart + 26:priceEnd].partition('\n')[0].partition(': ')[-1]
            if len(priceExtract) > 0 :
                priceExist = htmlString.find('Out of stock', priceEnd, priceEnd + 500)
                priceMeasureEnd = htmlString.find(':', priceStart)
                priceMeasure = htmlString[priceStart + 26:priceMeasureEnd]
                if priceExtract[0] == '£' : priceExtract = priceExtract[1:]
                if priceExtract[-1] == 'p' :
                    priceExtract = priceExtract[:-1]
                    priceExtract = '{:.2f}'.format(float(priceExtract) / 100)
                if (priceMeasure == "Price per litre") or (priceMeasure == "Price per kg") :
                    priceExtract = '{:.2f}'.format(float(priceExtract) / 10)
                if priceMeasure == "Price per 75cl" :
                    priceExtract = '{:.2f}'.format((float(priceExtract) / 30) * 4)
                priceExtract = '£' + priceExtract + unit
                if priceExist == -1 : priceList += [priceExtract]
            priceStart = htmlString.find('<p class="pricePerWeight">', priceEnd)
            priceEnd = htmlString.find('</p>', priceStart)

        # Extract titles
        titleList = []
        titleStart = htmlString.find('<strong itemprop="name">')
        titleEnd = htmlString.find('</strong>', titleStart)

        while 0 <= titleStart <= len(htmlString) :
            if htmlString.find('<p class="pricePerWeight"> </p>', titleEnd, titleEnd + 3000) == -1 :
                measureEnd = htmlString.find('</a>', titleEnd)
                measure = htmlString[titleEnd:measureEnd].partition('\n')[-1].partition('             ')[-1].partition('\r\n')[0]
                titleExtract = htmlString[titleStart + 24:titleEnd].replace('amp;', '').lstrip('<abbr title= ').partition('>')[0].strip('''"''')
                titleExtract = titleExtract + ' ' + measure
                titleExist = htmlString.find('Out of stock', titleEnd, titleEnd + 1500)
                if titleExist == -1 : titleList += [titleExtract]
            titleStart = htmlString.find('<strong itemprop="name">', titleEnd)
            titleEnd = htmlString.find('</strong>', titleStart)

        if len(priceList) != len(titleList) :
                errorTime = strftime('%H:%M:%S %Y-%m-%d')
                errorMessage = "MorrisonsError: lengths of prices and item titles do not match."
                listLengths = 'priceList length = ' + str(len(priceList)) + '\n' + 'titleList length = ' + str(len(titleList))
                return errorTime + '\n' + errorMessage + '\n' + listLengths + '\n' + url + '\n' + '-' * 80
        else : return [list(x) for x in zip(titleList, priceList, ["Morrisons"] * len(priceList))]
