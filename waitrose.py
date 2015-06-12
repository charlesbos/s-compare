"""
This program extracts prices and item titles from a valid Waitrose store page
url and then returns that data.

Copyright (C) 2015 Team S

Team S comprises of :
* Charles Bos
* Daniel Bedingfield
* Joshua Coyle
* Oyinpreye Onita
* Sebastian Jakobsen
* Thomas Harris

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from fetcher import waitroseFetch
from time import strftime

def waitroseData(url, titletag, unit, scroll) :
    '''
    Extracts a list of item prices and a list of item titles. Will try and return a
    tuple containing the aforementioned lists plus a list containing the shop name.
    Titletag arg is not used and is specified for compatibilty reasons only.
    '''
    htmlString = waitroseFetch(url, scroll)

    if htmlString == '<html><head></head><body></body></html>' :
        errorTime = strftime('%H:%M:%S %Y-%m-%d')
        errorMessage = "WaitroseError: failed to retrieve webpage."
        return errorTime + '\n' + errorMessage + '\n' + url + '\n' + '-' * 80
    elif htmlString == 'null' :
        errorTime = strftime('%H:%M:%S %Y-%m-%d')
        errorMessage = "WaitroseError: browser operation failed. Please check your browser config."
        return errorTime + '\n' + errorMessage + '\n' + url + '\n' + '-' * 80
    else :
        # Extract prices
        priceList = []
        priceStart = htmlString.find('<span class="fine-print">(')
        priceEnd = htmlString.find('p ', priceStart)
        
        while 0 <= priceStart <= len(htmlString) :
            if unit != '/each' :
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
                    priceList += [priceExtract]        
                except ValueError :
                    errorTime = strftime('%H:%M:%S %Y-%m-%d')
                    errorMessage = "WaitroseError: prices could not successfully be converted to a standard unit"
                    return errorTime + '\n' + errorMessage + '\n' + url + '\n' + '-' * 80
            else :
                if htmlString[priceStart + 26] == '£' : priceEnd = htmlString.find(' each', priceStart)
                priceExtract = htmlString[priceStart + 26:priceEnd]
                parityCheck = htmlString[priceEnd + 2:htmlString.find(')', priceEnd)]
                try :
                    if priceExtract[0] == '£' : priceExtract = '£' + '{:.2f}'.format((float(priceExtract[1:]) / 100)) + unit
                    else : priceExtract = '£' + '{:.2f}'.format((float(priceExtract) / 100)) + unit  
                    sanityCheck = True
                except ValueError :
                    sanityCheck = False
                if (parityCheck == unit[1:]) and (sanityCheck == True) : priceList += [priceExtract]
            priceStart = htmlString.find('<span class="fine-print">(', priceEnd)
            priceEnd = htmlString.find('p ', priceStart)

        # Extract titles
        titleList = []
        titleStart = htmlString.find('<div alt="')
        titleEnd = htmlString.find('" ', titleStart)

        while 0 <= titleStart <= len(htmlString) :
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
            return errorTime + '\n' + errorMessage + '\n' + listLengths + '\n' + url + '\n' + '-' * 80
        else : return [list(x) for x in zip(titleList, priceList, ["Waitrose"] * len(priceList))]
