"""
This program extracts prices and item titles from a valid Sainsburys store page
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

def sainsburysData(url, titletag, unit, scroll) :
    '''
    Extracts a list of item prices and a list of item titles. Will try and return a
    tuple containing the aforementioned lists plus a list containing the shop name.
    Scroll arg is not used and specified for compatibility reasons only.
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
