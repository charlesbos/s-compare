"""
This program extracts prices and item titles from a valid Tesco store page
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
from fetcher import simpleFetch
from time import strftime

def tescoData(url, titletag, unit, scroll) :
    '''
    Extracts a list of item prices and a list of item titles. Will try and return a
    tuple containing the aforementioned lists plus a list containing the shop name.
    Titletag and scroll args are not used and are specified for compatibilty reasons only.
    '''
    htmlString = simpleFetch(url)

    if htmlString == 'null' :
        errorTime = strftime('%H:%M:%S %Y-%m-%d')
        errorMessage = "TescoError: failed to retrieve webpage."
        return errorTime + '\n' + errorMessage + '\n' + url + '\n' + '-' * 80
    else :
        # Extract prices
        priceList = []
        priceStart = htmlString.find('<span class="linePriceAbbr">')
        priceEnd = htmlString.find('/', priceStart)
        
        while 0 <= priceStart <= len(htmlString) :
            priceExtract = htmlString[priceStart + 28:priceEnd].strip('()') + unit
            measureCheck = htmlString[priceEnd:priceEnd + 5]
            if measureCheck == '/75cl' :
                priceExtract = '£' + str('{:.2f}'.format(((float(htmlString[priceStart + 28:priceEnd].strip('()')[1:]) / 30) * 4))) + unit
            if (measureCheck == '/l)</') or (measureCheck == '/kg)<') :
                priceExtract = '£' + str('{:.2f}'.format((float(htmlString[priceStart + 28:priceEnd].strip('()')[1:]) / 10))) + unit
            parityCheck = (unit != '/each') and (measureCheck == '/each')
            if not parityCheck : priceList += [priceExtract]
            priceStart = htmlString.find('<span class="linePriceAbbr">', priceEnd)
            priceEnd = htmlString.find('/', priceStart)

        # Extract titles
        titleList = []
        titleStart = htmlString.find('<span data-title="true">') + 24
        titleEnd = htmlString.find('</span>')
        nextItem = htmlString.find('<span data-title="true">', titleEnd)

        while 0 <= titleStart <= len(htmlString) :
            titleExtract = htmlString[titleStart + 24:titleEnd].partition('&gt;')[0].replace('amp;', '')
            itemExistCheck = htmlString.find('Sorry, this product is currently not available.', titleEnd, nextItem)
            parityCheck = (unit != '/each') and (htmlString.find('/each', titleEnd, nextItem) != -1)
            if (itemExistCheck == -1) and (parityCheck == False) and (titleExtract.find('http://') == -1) : titleList += [titleExtract]
            titleStart = htmlString.find('<span data-title="true">', titleEnd)
            titleEnd = htmlString.find('</span></a></h2>', titleStart)
            nextItem = htmlString.find('<span data-title="true">', titleEnd)

        titleList = [x for x in titleList if x != '']

        # Merge the two lists into one list of tuples and return it
        if len(priceList) != len(titleList) :
            errorTime = strftime('%H:%M:%S %Y-%m-%d')
            errorMessage = "TescoError: lengths of prices and item titles do not match."
            listLengths = 'priceList length = ' + str(len(priceList)) + '\n' + 'titleList length = ' + str(len(titleList))
            return errorTime + '\n' + errorMessage + '\n' + listLengths + '\n' + url + '\n' + '-' * 80
        else : return [list(x) for x in zip(titleList, priceList, ["Tesco"] * len(priceList))]
