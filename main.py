"""
main.py

This file imports the various modules for each shop, calls the functions and
then outputs the data returned by them.
"""
from tesco import tescoData
from sainsburys import sainsburysData
from waitrose import waitroseData
import extra
from tkinter import *
from tkinter import messagebox

# Data fetching and processing functions
def dataPull(filePath, shopFunc, titletag, unit, scroll) :
    '''
    A function to dynamically call the shop module functions multiple times (for different urls)
    according to the product chosen by the user.
    Four arguments are taken. The first is the path to the file from which to extract the urls. The
    second is the name of the shop function to call. The third is the html string which the shop function
    uses to search for titles (Sainsburys only). The fourth is the unit to attach to the prices. The
    fifth is the number of times the page needs to be scrolled (Waitrose only).
    '''
    prices = []
    file = open(filePath, 'r')
    urls = str(file.read()).split('\n')
    urls = [x for x in urls if x != '']

    for x in range(len(urls)) :
        temp = shopFunc(urls[x], titletag, unit, scroll)
        if temp != 'null' : prices += temp

    return prices

def call(fileName, unit, titleTagEnd, scroll, windowName) :
    '''
    A function for calling dataPull, displaying an error message if there are no results and destroying
    the current window. The windowName argument argument is the name of the window to destroy. For the
    other args, see the dataPull documentation.
    '''
    tescoPrices = dataPull('URL_STORE/TESCO/' + fileName, tescoData, 'null', unit, 'null')
    sainsburysPrices = dataPull('URL_STORE/SAINSBURYS/' + fileName, sainsburysData, '<a href="http://www.sainsburys.co.uk/shop/gb/groceries/' + titleTagEnd, unit, 'null')
    waitrosePrices = dataPull('URL_STORE/WAITROSE/' + fileName, waitroseData, 'null', unit, scroll)
    combinedPrices = aggregateLists(tescoPrices, sainsburysPrices, waitrosePrices)
    if combinedPrices == 'null' : messagebox.showerror(title = "Extraction Failure", message = "All operations failed. No results to display.")
    else : results(combinedPrices)
    Toplevel.destroy(windowName)

def aggregateLists(tescoPrices, sainsburysPrices, waitrosePrices) :
    '''
    A function for aggregating the lists that have been returned by the shop modules.
    Three arguments taken, the lists of tuples containing the prices for each shop.
    '''
    allPrices = []
    cheapest = []

    if tescoPrices != [] :
        allPrices += tescoPrices
        cheapest += lowestPrices(tescoPrices)
    if sainsburysPrices != [] :
        allPrices += sainsburysPrices
        cheapest += lowestPrices(sainsburysPrices)
    if waitrosePrices != [] :
        allPrices += waitrosePrices
        cheapest += lowestPrices(waitrosePrices)

    if (allPrices != []) and (cheapest != []) :
        allPrices = createTable(allPrices, "== Prices from all shops ==")
        cheapest = createTable(cheapest, "== Lowest prices from each shop ==")
        return str(cheapest + '\n' + allPrices)
    else : return 'null'

def sortPrices(prices) :
    '''
    A function to correctly sort the lists of tuples by price. Using the sorted function does not
    always work correctly because our prices are strings, not floats.
    One argument is accepted, the list of prices to be sorted.
    '''
    x = 0
    y = 1

    if (prices != 'null') and (prices != []) :
        for x in range(len(prices)) :
            for y in range(len(prices) -1, x, -1) :
                tupA = prices[x]
                tupB = prices[y]
                priceA = tupA[1]
                priceB = tupB[1]
                endA = priceA.find('/')
                endB = priceB.find('/')
                if float(priceA[1:endA]) > float(priceB[1:endB]) :
                    prices[x] = tupB
                    prices[y] = tupA        

    return prices

def lowestPrices(prices) :
    '''
    This function extracts the minimum prices from a list of tuples. Then it returns a list of tuples
    which contain just those tuples with the minimum values.

    One argument is accepted, the list of tuples from which to extract the minimum values.
    '''
    prices = sortPrices(prices)
    return [list(x) for x in prices if x[1] == prices[0][1]]

def createTable(prices, tableHeader) :
    '''
    A function to write a price list to a neatly formatted table which can be displayed in the results
    window.
    Two arguments are taken, the price list and the header for the table.
    '''
    prices = sortPrices(prices)
    
    priceTable = str(tableHeader).center(130, ' ') + '\n' + ('-' * 130) + '\n'
    
    if prices != [] :
        for x in range(len(prices)) :
            temp = '{:85s}'.format(prices[x][0]), prices[x][1].rjust(15, ' '), ' ' * 6, prices[x][2]
            priceTable += str(temp)
            priceTable += '\n' + ('-' * 130) + '\n'
    else : 'No results obtained. Cannot create table.\n'

    return priceTable.replace('"', ' ').replace("'", ' ').replace(',', ' ').replace('(', ' ').replace(')', ' ')

# Initialise windows
top = Tk()
top.title("Team S Scrape")
frame1 = Frame(top).grid()
frame2 = Frame(top).grid()

def bread() :
    bread = Toplevel()
    bread.title("Compare - Bread")
    button1 = Button(bread, text = "Wholemeal Bread", height = 5, width = 12, command = lambda : call('BROWN_BREAD.txt', '/100g', 'wholemeal-brown-bread/', 2, bread)).grid(row = 1, column = 1)                
    button2 = Button(bread, text = "White Bread", height = 5, width = 12, command = lambda : call('WHITE_BREAD.txt', "/100g", 'white-bread/', 2, bread)).grid(row = 1, column = 2)
    
def dairy() :
    dairy = Toplevel()
    dairy.title("Compare - Dairy")
    button1 = Button(dairy, text = "Milk", height = 5, width = 12, command = lambda : call('MILK.txt', '/100ml', 'fresh-milk/', 5, dairy)).grid(row = 1, column = 1)
    button2 = Button(dairy, text = "Butter", height = 5, width = 12, command = lambda : call('BUTTER.txt', '/100g', 'butter/', 2, dairy)).grid(row = 1, column = 2)
    button3 = Button(dairy, text = "Eggs", height = 5, width = 12, command = lambda : call('EGGS.txt', '/each', 'eggs/', 1, dairy)).grid(row = 1, column = 3)

def crisps_and_snacks() :
    crisps_and_snacks = Toplevel()
    crisps_and_snacks.title("Compare - Crisps & Snacks")
    button1 = Button(crisps_and_snacks, text = "Crisps", height = 5, width = 12, command = lambda : call('CRISPS.txt', '/100g', 'crisps/', 4, crisps_and_snacks)).grid(row = 1, column = 1)
    button2 = Button(crisps_and_snacks, text = "Cereal Bars", height = 5, width = 12, command = lambda : call('CEREAL_BARS.txt', '/100g', 'breakfast-cereal-bars-breakfast-biscuits/', 3, crisps_and_snacks)).grid(row = 1, column = 2)

def drinks() :
    drinks = Toplevel()
    drinks.title("Compare - Drinks")
    button1 = Button(drinks, text = "Still Water", height = 5, width = 12, command = lambda : call('STILL_WATER.txt', '/100ml', 'still-water/', 4, drinks)).grid(row = 1, column = 1)
    button2 = Button(drinks, text = "Sparkling Water", height = 5, width = 12, command = lambda : call('SPARKLING_WATER.txt', '/100ml', 'sparkling-water', 2, drinks)).grid(row = 1, column = 2)
    button3 = Button(drinks, text = "Everyday Tea", height = 5, width = 12, command = lambda : call('EVERYDAY_TEA.txt', '/100g', 'tea/', 3, drinks)).grid(row = 1, column = 3)

def deserts() :
    deserts = Toplevel()
    deserts.title("Compare - Deserts")
    button1 = Button(deserts, text = "Ice Cream Tubs", height = 5, width = 12, command = lambda : call('ICE_CREAM_TUBS.txt', '/100g', 'ice-cream-tubs/', 6, deserts)).grid(row = 1, column = 1)

def fruit_and_veg() :
    fruit_and_veg = Toplevel()
    fruit_and_veg.title("Compare - Fruit & Veg")

def results(prices) :
    results = Toplevel()
    results.title("Results")
    frame1 = Frame(results)
    frame2 = Frame(results)
    frame1.pack()
    frame2.pack(side = BOTTOM)
    scrollbar = Scrollbar(frame1)
    scrollbar.pack(side = RIGHT, fill = Y)
    text = Text(frame1, height = 40, width = 135, yscrollcommand = scrollbar.set)
    scrollbar.config(command = text.yview)
    text.insert(END, prices)
    text.configure(state = DISABLED)
    text.pack()
    button1 = Button(frame2, text = "Close", command = results.destroy)
    button1.pack(side = TOP)

def about(content) :
    about = Toplevel()
    about.title("About")
    frame1 = Frame(about)
    frame2 = Frame(about)
    frame1.pack()
    frame2.pack(side = BOTTOM)
    text = Text(frame1)
    text.insert(END, content)
    text.configure(state = DISABLED)
    text.pack()
    button1 = Button(frame2, text = "License", command = lambda : contentFetch(licenseWin, 'LICENSE.txt'))
    button1.pack(side = LEFT)
    button2 = Button(frame2, text = "Changelog", command = lambda : contentFetch(changelogWin, 'CHANGELOG.txt'))
    button2.pack(side = LEFT)
    button3 = Button(frame2, text = "Close", command = about.destroy)
    button3.pack(side = RIGHT)

def licenseWin(content) :
    licenseWin = Toplevel()
    licenseWin.title("License")
    frame1 = Frame(licenseWin)
    frame2 = Frame(licenseWin)
    frame1.pack()
    frame2.pack(side = BOTTOM)
    scrollbar = Scrollbar(frame1)
    scrollbar.pack(side = RIGHT, fill = Y)
    text = Text(frame1, height = 40, width = 160, yscrollcommand = scrollbar.set)
    scrollbar.config(command = text.yview)
    text.insert(END, content)
    text.configure(state = DISABLED)
    text.pack()
    button1 = Button(frame2, text = "Close", command = licenseWin.destroy)
    button1.pack(side = TOP)

def changelogWin(content) :
    changelogWin = Toplevel()
    changelogWin.title("Changelog")
    frame1 = Frame(changelogWin)
    frame2 = Frame(changelogWin)
    frame1.pack()
    frame2.pack(side = BOTTOM)
    scrollbar = Scrollbar(frame1)
    scrollbar.pack(side = RIGHT, fill = Y)
    text = Text(frame1, height = 40, width = 160, yscrollcommand = scrollbar.set)
    scrollbar.config(command = text.yview)
    text.insert(END, content)
    text.configure(state = DISABLED)
    text.pack()
    button1 = Button(frame2, text = "Close", command = changelogWin.destroy)
    button1.pack(side = TOP)

def logViewer(content) :
    logViewer = Toplevel()
    logViewer.title("Logs")
    frame1 = Frame(logViewer)
    frame2 = Frame(logViewer)
    frame1.pack()
    frame2.pack(side = BOTTOM)
    scrollbar = Scrollbar(frame1)
    scrollbar.pack(side = RIGHT, fill = Y)
    text = Text(frame1, height = 40, width = 160, yscrollcommand = scrollbar.set)
    scrollbar.config(command = text.yview)
    text.insert(END, content)
    text.configure(state = DISABLED)
    text.pack()
    button1 = Button(frame2, text = "Close", command = logViewer.destroy)
    button1.pack(side = LEFT)

def contentFetch(funcName, fileName) :
    content = extra.viewFile(fileName)
    if funcName == logViewer :
        if content == 'null' : messagebox.showinfo(title = "Logs", message = "No logs to display.")
        else : logViewer(content)
    else :
        if content == 'null' : messagebox.showerror(title = "Content Failure", message = "Content not found. Please ensure the program has all the necessary files.")
        else : funcName(content)

button1 = Button(frame1, text = "Bread", command = bread, height = 5, width = 12).grid(row = 1, column = 1)
button2 = Button(frame1, text = "Dairy", command = dairy, height = 5, width = 12).grid(row = 1, column = 2)
button3 = Button(frame1, text = "Crips and Snacks", command = crisps_and_snacks, height = 5, width = 12).grid(row = 1, column = 3)
button4 = Button(frame1, text = "Drinks", command = drinks, height = 5, width = 12).grid(row = 2, column = 1)
button5 = Button(frame1, text = "Deserts", command = deserts, height = 5, width = 12).grid(row = 2, column = 2)
button6 = Button(frame1, text = "Fruit & Veg", command = fruit_and_veg, height = 5, width = 12, state = DISABLED).grid(row = 2, column = 3)
button7 = Button(frame2, text = "Quit", command = top.destroy).grid(row = 3, column = 3, pady = 10)
button8 = Button(frame2, text = "Help", state = DISABLED).grid(row = 3, column = 1, pady = 10)
button9 = Button(frame2, text = "About", command = lambda : contentFetch(about, 'ABOUT.txt')).grid(row = 3, column = 2, pady = 10)
button10 = Button(frame2, text = "View Logs", command = lambda : contentFetch(logViewer, 'ERROR_LOG.txt')).grid(row = 4, column = 1, pady = 5)
button11 = Button(frame2, text = "Clear Logs", command = extra.clearLogs).grid(row = 4, column = 2, pady = 5)

top.mainloop()

