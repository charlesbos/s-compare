"""
waitrose.py

This modules extracts prices and item titles from a valid Waitrose store page
url and then returns that data.
"""
from fetcher import htmlFetch

def waitroseData(url, titletag, unit) :
    '''
    Extract Waitrose prices per measure and item titles.
    Three arguments are accepted. The first is a url which can be passed to the htmlFetch function.
    The second is a unit to append to the extracted prices.
    from the fetcher module. The third is the fragment of html that marks the beginning
    of an item title. Note that the titletag argument is not used in this function
    at all and is specified for compatibility reasons only.
    '''

    htmlString = htmlFetch(url)

    if htmlString == 'null' :
        print("WaitroseError: failed to retrieve webpage.")
        return 'null'
    else :
        # Extract prices
        priceStart = htmlString.find('<span class="fine-print">(') + 26

        if priceStart == -1 :
            print("WaitroseError: failed to extract prices.")
            return 'null'
        else :
            priceEnd = htmlString.find('p', priceStart)
            measureCheck = htmlString.find('per litre', priceEnd, priceEnd + 10)
            if measureCheck == -1 :
                try :
                    priceExtract = '£' + str('{:.2f}'.format((float(htmlString[priceStart:priceEnd]) / 100), 2)) + unit
                except ValueError :
                    pass
            else : priceExtract = '£' + str('{:.2f}'.format((float(htmlString[priceStart:priceEnd][1:]) / 100), 2)) + unit
            priceList = [priceExtract]
            
            while priceStart != 25 :
                priceStart = htmlString.find('<span class="fine-print">(', priceEnd) + 26
                priceEnd = htmlString.find('p', priceStart)
                measureCheck = htmlString.find('per litre', priceEnd, priceEnd + 10)
                if measureCheck == -1 :
                    try :
                        priceExtract = '£' + str('{:.2f}'.format((float(htmlString[priceStart:priceEnd]) / 100), 2)) + unit
                    except ValueError :
                        pass
                else : priceExtract = '£' + str('{:.2f}'.format((float(htmlString[priceStart:priceEnd][1:]) / 100), 2)) + unit
                priceList.extend([priceExtract])

            priceList = priceList[:-1]

        # Extract titles
        titleStart = htmlString.find('''productX.push('{"name":"''') + 24

        if titleStart == -1 :
            print("WaitroseError: failed to extract item titles.")
            return 'null'
        else :
            titleEnd = htmlString.find('","id":')
            addMeasureStart = htmlString.find('"weight":"', titleEnd) + 10
            addMeasureEnd = htmlString.find('",', addMeasureStart)
            titleExtract = str(htmlString[titleStart:titleEnd] + ' ' + htmlString[addMeasureStart:addMeasureEnd]).replace('&amp;', '&').replace('&#039;', "'")
            priceExistCheck = htmlString.find('"price_per_unit":"",', titleEnd, titleEnd + 400)
            if priceExistCheck == -1 :
                titleList = [titleExtract]

            while titleStart != 23 :
                titleStart = htmlString.find('''productX.push('{"name":"''', titleEnd) + 24
                titleEnd = htmlString.find('","id":', titleStart)
                addMeasureStart = htmlString.find('"weight":"', titleEnd) + 10
                addMeasureEnd = htmlString.find('",', addMeasureStart)
                titleExtract = str(htmlString[titleStart:titleEnd] + ' ' + htmlString[addMeasureStart:addMeasureEnd]).replace('&amp;', '&').replace('&#039;', "'")
                priceExistCheck = htmlString.find('"price_per_unit":"",', titleEnd, titleEnd + 400)
                if priceExistCheck == -1 :
                    titleList.extend([titleExtract])

            titleList = titleList[:-1]

        # Merge the two lists into one list of tuples and return it
        if len(priceList) != len(titleList) :
            print("WaitroseError: lengths of prices and item titles do not match.")
            return 'null'
        else :
            waitroseList = []
            counter = 0

            while counter < len(priceList) :
                waitroseList.append((titleList[counter], priceList[counter], "Waitrose"))
                counter += 1

            if waitroseList == [] :
                print("WaitroseError: unspecified extraction error.")
                return 'null'
            else :
                print("Operation for Waitrose completed successfully.")
                return waitroseList


                            


                    


