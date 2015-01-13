"""
sainsburys.py

This modules extracts prices and item titles from a valid Sainsburys store page
url and then returns that data.
"""
from fetcher import htmlFetch

def sainsburysData(url, titletag, unit) :
    '''
    Extract Sainsburys prices per measure and item titles.
    Three arguments are accepted. The first is a url which can be passed to the htmlFetch function.
    The second is a unit to append to the extracted prices.
    from the fetcher module. The third is the fragment of html that marks the beginning
    of an item title.
    '''

    htmlString = htmlFetch(url)

    if htmlString == 'null' :
        print("SainsburysError: failed to retrieve webpage.")
        return 'null'
    else :
        # Extract prices
        priceStart = htmlString.find('<p class="pricePerMeasure">') + 27

        if priceStart == -1 :
            print("SainsburysError: failed to extract prices.")
            return 'null'
        else :
            priceEnd = priceStart + 5
            priceExtract = htmlString[priceStart:priceEnd] + unit
            mercCheck = htmlString.find('/wcsstore7.06.4.33/SainsburysStorefrontAssetStore/wcassets/merchandising_associations/', priceStart - 1000, priceStart)
            if mercCheck == -1 :
                priceList = [priceExtract]
            
            while priceStart != 26 :
                priceStart = htmlString.find('<p class="pricePerMeasure">', priceEnd) + 27
                priceEnd = priceStart + 5
                priceExtract = htmlString[priceStart:priceEnd] + unit
                mercCheck = htmlString.find('/wcsstore7.06.4.33/SainsburysStorefrontAssetStore/wcassets/merchandising_associations/', priceStart - 1000, priceStart)
                if mercCheck == -1 :
                    priceList.extend([priceExtract])

            priceList = priceList[:-1]

        # Extract titles
        titleStart = htmlString.find(titletag) + 67

        if titleStart == -1 :
            print("SainsburysError: failed to extract item titles.")
            return 'null'
        else :
            titleEnd = htmlString.find('<img alt=', titleStart) + 9
            titleExtract = htmlString[titleStart:titleEnd].partition(' ')[-1].partition('\r\n')[0].strip(' ').replace('&amp;', '&')
            titleList = [titleExtract]

            while titleStart != 75 :
                titleStart = htmlString.find(titletag, titleEnd) + 76
                titleEnd = htmlString.find('<img alt=', titleStart) + 9
                titleExtract = htmlString[titleStart:titleEnd].partition(' ')[-1].partition('\r\n')[0].strip(' ').replace('&amp;', '&')
                titleList.extend([titleExtract])

            titleList = titleList[:-1] 

        # Extract promotion titles
        proTitleStart = htmlString.find('''<a href="http://www.sainsburys.co.uk/shop/ProductDisplay?''') + 57

        if proTitleStart == -1 : pass
        else:
            proTitleEnd = htmlString.find('<img alt=', proTitleStart) + 9
            proTitleExtract = htmlString[proTitleStart:proTitleEnd].partition(' ')[-1].partition('\r\n')[0].strip(' ').replace('&amp;', '&')
            proTitleList = [proTitleExtract]

            while proTitleStart != 65 :
                proTitleStart = htmlString.find('''<a href="http://www.sainsburys.co.uk/shop/ProductDisplay?''', proTitleEnd) + 66
                proTitleEnd = htmlString.find('<img alt=', proTitleStart) + 9
                proTitleExtract = htmlString[proTitleStart:proTitleEnd].partition(' ')[-1].partition('\r\n')[0].strip(' ').replace('&amp;', '&')
                proTitleList.extend([proTitleExtract])

            proTitleList = proTitleList[1:-1]

        # Merge the lists
        try :
            titleList = titleList + proTitleList
            titleList = sorted(titleList)
        except NameError :
            pass

        # Merge the two lists into one list of tuples and return it
        if len(priceList) != len(titleList) :
            print("SainsburysError: lengths of prices and item titles do not match.")
            return 'null'
        else :
            sainsList = []
            counter = 0

            while counter < len(priceList) :
                sainsList.append((titleList[counter], priceList[counter], "Sainsbury's"))
                counter += 1
                
            if sainsList == [] :
                print("SainsburysError: unspecified extraction error.")
                return 'null'
            else :
                print("Operation for Sainsbury's completed successfully.")
                return sainsList


                            


                    


