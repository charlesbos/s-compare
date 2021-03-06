"""
This program extracts prices and item titles from a valid Morrisons store page
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
            priceExtract = htmlString[priceStart + 26:priceEnd]
            if len(priceExtract) > 0 :
                priceExist = htmlString.find('Out of stock', priceEnd, priceEnd + 500)
                if priceExtract.find('p ') != -1 : priceMeasureStart = priceExtract.find('p ')
                elif priceExtract.find(' p') != -1 : priceMeasureStart = priceExtract.find(' p')
                priceMeasure = priceExtract[priceMeasureStart:priceEnd]
                if priceExtract[0] == '£' : priceExtract = priceExtract[1:]
                if priceMeasure.find('p ') != -1 :
                    priceExtract = '{:.2f}'.format(float(priceExtract[:priceMeasureStart]) / 100)
                if (priceMeasure.find("litre") != -1) or (priceMeasure.find("kg") != -1) :
                    priceExtract = '{:.2f}'.format(float(priceExtract[:priceMeasureStart]) / 10)
                if priceMeasure.find("75cl") != -1 :
                    priceExtract = '{:.2f}'.format((float(priceExtract[:priceMeasureStart]) / 30) * 4)
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
