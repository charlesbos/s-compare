"""
morrisons.py

This module extracts prices and item titles from a valid Morrisons store page
url and then returns that data.
"""
from fetcher import simpleFetch
from time import strftime

def morriData(url, titletag, unit, scroll) :
    '''
    Extract Morrisons line prices per measure and item titles
    Three arguments are accepted. The first is a url which can be passed to the htmlFetch function.
    The second is a unit to append to the extracted prices.
    from the fetcher module. The third and fourth are not used in this function
    at all and are specified for compatibility reasons only.
    '''

    htmlString = simpleFetch(url)
    
    if htmlString == "null" :
        errorTime = strftime('%H:%M:%S %Y-%m-%d')
        errorMessage = "MorrisonsError: failed to retrieve webpage."
        return errorTime + '\n' + errorMessage + '\n' + url + '\n' + '-' * 80 
    else :
        # Extract prices
        priceList = []
        priceStart = htmlString.find('<p class="pricePerWeight">') + 32
        priceMiddle = htmlString.find(':', priceStart) + 2
        priceEnd = htmlString.find('<', priceMiddle)

        while (0 <= priceStart <= len(htmlString)) is True :
            priceExtract = htmlString[priceMiddle:priceEnd]
            priceExist = htmlString[priceEnd: priceEnd + 500]
            doesPriceExist = priceExist.find('Out of stock')
            priceMeas = htmlString[priceStart:priceMiddle]
            priceExtract = priceExtract[:-1]
            if priceExtract[0] == "£" : priceExtract = priceExtract[1:]
            if priceExtract[-1] == "p" :
                priceExtract = priceExtract[:-1]
                penceToPerfect = priceExtract.find('.')
                if penceToPerfect != -1 : priceExtract = priceExtract[:penceToPerfect]
                priceExtract = '0.0' + priceExtract
                if len(priceExtract) == 5 : priceExtract = priceExtract[:2] + priceExtract[3:]
                if priceExtract == '0.00' : priceExtract = '0.01'
            if (priceMeas == "per litre: ") or (priceMeas == "per kg: ") :
                priceExtract = float(priceExtract)
                priceExtract = priceExtract / 10
                priceExtract = str('{:.2f}'.format(priceExtract))
            if priceMeas == "per 75cl: " :
                priceExtract = float(priceExtract)
                priceExtract = (priceExtract / 30) * 4
                priceExtract = str('{:.2f}'.format(priceExtract))
            priceExtract = '£' + priceExtract + unit
            if (priceExtract[1] == 'a') : break
            elif(priceExtract[1] == '\n') : del priceExtract
            elif doesPriceExist == -1 : priceList += [priceExtract]
            priceStart = htmlString.find('<p class="pricePerWeight">', priceEnd) + 32
            priceMiddle = htmlString.find(':', priceStart) + 2
            priceEnd = htmlString.find('<', priceMiddle)

        # Extract titles
        titleList = []
        titleStart = htmlString.find('<strong itemprop="name">')
        titleEnd = htmlString.find('</strong>', titleStart)
        measureStart = titleEnd + 9
        measureEnd = measureStart + 10

        while (0<= titleStart <= len(htmlString)) is True :
            titleExtract = htmlString[titleStart + 24:titleEnd]
            titleExist = htmlString[titleEnd: titleEnd + 1500]
            doesTitleExist = titleExist.find('Out of stock')
            ampLoc = titleExtract.find('&amp;')
            if ampLoc != -1 : titleExtract = titleExtract[:ampLoc] + 'and' + titleExtract[ampLoc + 5:]
            abbrLoc = titleExtract.find('<')
            if abbrLoc != -1 : titleExtract = titleExtract[13:]
            abbrLoc2 = titleExtract.find('">')
            if abbrLoc2 != -1 : titleExtract = titleExtract[:abbrLoc2]
            totalWeightStart = htmlString.find('', titleEnd) + 24
            totalWeightEnd = htmlString.find('</a>', totalWeightStart)
            totalWeightExtract = htmlString[totalWeightStart:totalWeightEnd]
            slashRLoc = totalWeightExtract.find('\r')
            totalWeightExtract = totalWeightExtract[:slashRLoc]
            titleExtract = titleExtract + ' ' + totalWeightExtract
            valid = titleExtract.find('class=')
            if valid != -1 : titleExtract = titleExtract[:valid]
            if doesTitleExist == -1 : titleList += [titleExtract]
            titleStart = htmlString.find('<strong itemprop="name">', titleEnd)
            titleEnd = htmlString.find('</strong>', titleStart)

        for i in priceList :
            findError = (i[:7].find('c') != -1)
            if findError != -1 :
                del titleList[findError]
                del priceList[findError]
            if (i[1] == 'a'):
                findProblem = priceList.index(i)
                try :
                    del titleList[findProblem]
                    del priceList[findProblem]
                except : pass

        if len(priceList) != len(titleList) :
                errorTime = strftime('%H:%M:%S %Y-%m-%d')
                errorMessage = "MorrisonsError: lengths of prices and item titles do not match."
                listLengths = 'priceList length = ' + str(len(priceList)) + '\n' + 'titleList length = ' + str(len(titleList))
                return errorTime + '\n' + errorMessage + '\n' + listLengths + '\n' + url + '\n' + '-' * 80
        elif priceList == titleList == [] :
                errorTime = strftime('%H:%M:%S %Y-%m-%d')
                errorMessage = "MorrisonsError: no results found. Check the page URL and HTML."
                return errorTime + '\n' + errorMessage + '\n' + url + '\n' + '-' * 80
        else : return [list(x) for x in zip(titleList, priceList, ["Morrisons"] * len(priceList))]
