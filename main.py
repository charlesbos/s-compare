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

# Data processing functions
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

def aggregateLists(tescoPrices, sainsburysPrices, waitrosePrices) :
    '''
    A function for aggregating the lists that have been returned by the shop modules.
    No arguments taken.
    '''
    allPrices = []
    cheapest = []

    if tescoPrices != [] :
        allPrices += tescoPrices
        cheapest += lowestPrices(tescoPrices)
    else : pass
    if sainsburysPrices != [] :
        allPrices += sainsburysPrices
        cheapest += lowestPrices(sainsburysPrices)
    else : pass
    if waitrosePrices != [] :
        allPrices += waitrosePrices
        cheapest += lowestPrices(waitrosePrices)
    else : pass

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
    button1 = Button(bread, text = "Wholemeal Bread", height = 5, width = 12, command = lambda : call(prodWholemealBread, bread)).grid(row = 1, column = 1)                
    button2 = Button(bread, text = "White Bread", height = 5, width = 12, command = lambda : call(prodWhiteBread, bread)).grid(row = 1, column = 2)
    
def dairy() :
    dairy = Toplevel()
    dairy.title("Compare - Dairy")
    button1 = Button(dairy, text = "Milk", height = 5, width = 12, command = lambda : call(prodMilk, dairy)).grid(row = 1, column = 1)
    button2 = Button(dairy, text = "Butter", height = 5, width = 12, command = lambda : call(prodButter, dairy)).grid(row = 1, column = 2)
    button3 = Button(dairy, text = "Eggs", height = 5, width = 12, command = lambda : call(prodEggs, dairy)).grid(row = 1, column = 3)

def crisps_and_snacks() :
    crisps_and_snacks = Toplevel()
    crisps_and_snacks.title("Compare - Crisps & Snacks")
    button1 = Button(crisps_and_snacks, text = "Crisps", height = 5, width = 12, command = lambda : call(prodCrisps, crisps_and_snacks)).grid(row = 1, column = 1)
    button2 = Button(crisps_and_snacks, text = "Cereal Bars", height = 5, width = 12, command = lambda : call(prodCerealBars, crisps_and_snacks)).grid(row = 1, column = 2)

def drinks() :
    drinks = Toplevel()
    drinks.title("Compare - Drinks")
    button1 = Button(drinks, text = "Still Water", height = 5, width = 12, command = lambda : call(prodStillWater, drinks)).grid(row = 1, column = 1)
    button2 = Button(drinks, text = "Sparkling Water", height = 5, width = 12, command = lambda : call(prodSparklingWater, drinks)).grid(row = 1, column = 2)
    button3 = Button(drinks, text = "Everyday Tea", height = 5, width = 12, command = lambda : call(prodEverydayTea, drinks)).grid(row = 1, column = 3)

def deserts() :
    deserts = Toplevel()
    deserts.title("Compare - Deserts")
    button1 = Button(deserts, text = "Ice Cream Tubs", height = 5, width = 12, command = lambda : call(prodIceCreamTubs, deserts)).grid(row = 1, column = 1)

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
    text = Text(frame1, height = 40, width = 160, yscrollcommand = scrollbar.set)
    scrollbar.config(command = text.yview)
    text.insert(END, prices)
    text.pack()
    button1 = Button(frame2, text = "Close", command = results.destroy)
    button1.pack(side = TOP)

def about() :
    about = Toplevel()
    about.title("About")
    frame1 = Frame(about)
    frame2 = Frame(about)
    frame1.pack()
    frame2.pack(side = BOTTOM)
    text = Text(frame1)
    text.insert(END, extra.aboutText())
    text.pack()
    button1 = Button(frame2, text = "License", command = licenseWin)
    button1.pack(side = LEFT)
    button2 = Button(frame2, text = "Changelog", command = changelogWin)
    button2.pack(side = LEFT)
    button3 = Button(frame2, text = "Close", command = about.destroy)
    button3.pack(side = RIGHT)

def licenseWin() :
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
    text.insert(END, extra.licenseView())
    text.pack()
    button1 = Button(frame2, text = "Close", command = licenseWin.destroy)
    button1.pack(side = TOP)

def changelogWin() :
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
    text.insert(END, extra.changelogView())
    text.pack()
    button1 = Button(frame2, text = "Close", command = changelogWin.destroy)
    button1.pack(side = TOP)

def logViewer(logs) :
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
    text.insert(END, logs)
    text.pack()
    button1 = Button(frame2, text = "Close", command = logViewer.destroy)
    button1.pack(side = LEFT)

def logFetch() :
    logs = extra.viewLogs()
    if logs == 'null' : messagebox.showinfo(title = "Logs", message = "No logs to display.")
    else : logViewer(logs)

button1 = Button(frame1, text = "Bread", command = bread, height = 5, width = 12).grid(row = 1, column = 1)
button2 = Button(frame1, text = "Dairy", command = dairy, height = 5, width = 12).grid(row = 1, column = 2)
button3 = Button(frame1, text = "Crips and Snacks", command = crisps_and_snacks, height = 5, width = 12).grid(row = 1, column = 3)
button4 = Button(frame1, text = "Drinks", command = drinks, height = 5, width = 12).grid(row = 2, column = 1)
button5 = Button(frame1, text = "Deserts", command = deserts, height = 5, width = 12).grid(row = 2, column = 2)
button6 = Button(frame1, text = "Fruit & Veg", command = fruit_and_veg, height = 5, width = 12, state = DISABLED).grid(row = 2, column = 3)
button7 = Button(frame2, text = "Quit", command = top.destroy).grid(row = 3, column = 3, pady = 10)
button8 = Button(frame2, text = "Help", state = DISABLED).grid(row = 3, column = 1, pady = 10)
button9 = Button(frame2, text = "About", command = about).grid(row = 3, column = 2, pady = 10)
button10 = Button(frame2, text = "View Logs", command = logFetch).grid(row = 4, column = 1, pady = 5)
button11 = Button(frame2, text = "Clear Logs", command = extra.clearLogs).grid(row = 4, column = 2, pady = 5)

# Intermediate functions
def call(prodName, windowName) :
    prodName()
    Toplevel.destroy(windowName)

def prodStillWater() :
    tescoPrices = dataPull('URL_STORE/TESCO/STILL_WATER.txt', tescoData, 'null', "/100ml", 'null')
    sainsburysPrices = dataPull('URL_STORE/SAINSBURYS/STILL_WATER.txt', sainsburysData, '<a href="http://www.sainsburys.co.uk/shop/gb/groceries/still-water/', "/100ml", 'null')
    waitrosePrices = dataPull('URL_STORE/WAITROSE/STILL_WATER.txt', waitroseData, 'null', "/100ml", 4)
    combinedPrices = aggregateLists(tescoPrices, sainsburysPrices, waitrosePrices)
    if combinedPrices == 'null' : messagebox.showerror(title = "Extraction Failure", message = "All operations failed. No results to display.")
    else : results(combinedPrices)

def prodSparklingWater() :
    tescoPrices = dataPull('URL_STORE/TESCO/SPARKLING_WATER.txt', tescoData, 'null', "/100ml", 'null')
    sainsburysPrices = dataPull('URL_STORE/SAINSBURYS/SPARKLING_WATER.txt', sainsburysData, '<a href="http://www.sainsburys.co.uk/shop/gb/groceries/sparkling-water/', "/100ml", 'null')
    waitrosePrices = dataPull('URL_STORE/WAITROSE/SPARKLING_WATER.txt', waitroseData, 'null', "/100ml", 2)
    combinedPrices = aggregateLists(tescoPrices, sainsburysPrices, waitrosePrices)   
    if combinedPrices == 'null' : messagebox.showerror(title = "Extraction Failure", message = "All operations failed. No results to display.")
    else : results(combinedPrices) 

def prodEverydayTea() :
    tescoPrices = dataPull('URL_STORE/TESCO/EVERYDAY_TEA.txt', tescoData, 'null', "/100g", 'null')
    sainsburysPrices = dataPull('URL_STORE/SAINSBURYS/EVERYDAY_TEA.txt', sainsburysData, '<a href="http://www.sainsburys.co.uk/shop/gb/groceries/tea', "/100g", 'null')
    waitrosePrices = dataPull('URL_STORE/WAITROSE/EVERYDAY_TEA.txt', waitroseData, 'null', "/100g", 3)
    combinedPrices = aggregateLists(tescoPrices, sainsburysPrices, waitrosePrices)    
    if combinedPrices == 'null' : messagebox.showerror(title = "Extraction Failure", message = "All operations failed. No results to display.")
    else : results(combinedPrices)
            
def prodMilk() :
    tescoPrices = dataPull('URL_STORE/TESCO/MILK.txt', tescoData, 'null', "/100ml", 'null')
    sainsburysPrices = dataPull('URL_STORE/SAINSBURYS/MILK.txt', sainsburysData, '<a href="http://www.sainsburys.co.uk/shop/gb/groceries/fresh-milk', "/100ml", 'null')
    waitrosePrices = dataPull('URL_STORE/WAITROSE/MILK.txt', waitroseData, 'null', "/100ml", 5)
    combinedPrices = aggregateLists(tescoPrices, sainsburysPrices, waitrosePrices)    
    if combinedPrices == 'null' : messagebox.showerror(title = "Extraction Failure", message = "All operations failed. No results to display.")
    else : results(combinedPrices)

def prodWhiteBread() :
    tescoPrices = dataPull('URL_STORE/TESCO/WHITE_BREAD.txt', tescoData, 'null', "/100g", 'null')
    sainsburysPrices = dataPull('URL_STORE/SAINSBURYS/WHITE_BREAD.txt', sainsburysData, '<a href="http://www.sainsburys.co.uk/shop/gb/groceries/white-bread/', "/100g", 'null')
    waitrosePrices = dataPull('URL_STORE/WAITROSE/WHITE_BREAD.txt', waitroseData, 'null', "/100g", 2)
    combinedPrices = aggregateLists(tescoPrices, sainsburysPrices, waitrosePrices)   
    if combinedPrices == 'null' : messagebox.showerror(title = "Extraction Failure", message = "All operations failed. No results to display.")
    else : results(combinedPrices)

def prodWholemealBread() :
    tescoPrices = dataPull('URL_STORE/TESCO/BROWN_BREAD.txt', tescoData, 'null', "/100g", 'null')
    sainsburysPrices = dataPull('URL_STORE/SAINSBURYS/BROWN_BREAD.txt', sainsburysData, '<a href="http://www.sainsburys.co.uk/shop/gb/groceries/wholemeal-brown-bread/', "/100g", 'null')
    waitrosePrices = dataPull('URL_STORE/WAITROSE/BROWN_BREAD.txt', waitroseData, 'null', "/100g", 2)
    combinedPrices = aggregateLists(tescoPrices, sainsburysPrices, waitrosePrices)   
    if combinedPrices == 'null' : messagebox.showerror(title = "Extraction Failure", message = "All operations failed. No results to display.")
    else : results(combinedPrices)

def prodCerealBars() :
    tescoPrices = dataPull('URL_STORE/TESCO/CEREAL_BARS.txt', tescoData, 'null', "/100g", 'null')
    sainsburysPrices = dataPull('URL_STORE/SAINSBURYS/CEREAL_BARS.txt', sainsburysData, '<a href="http://www.sainsburys.co.uk/shop/gb/groceries/breakfast-cereal-bars-breakfast-biscuits', "/100g", 'null')
    waitrosePrices = dataPull('URL_STORE/WAITROSE/CEREAL_BARS.txt', waitroseData, 'null', "/100g", 3)
    combinedPrices = aggregateLists(tescoPrices, sainsburysPrices, waitrosePrices)    
    if combinedPrices == 'null' : messagebox.showerror(title = "Extraction Failure", message = "All operations failed. No results to display.")
    else : results(combinedPrices)
            
def prodEggs() :
    tescoPrices = dataPull('URL_STORE/TESCO/EGGS.txt', tescoData, 'null', "/each", 'null')
    sainsburysPrices = dataPull('URL_STORE/SAINSBURYS/EGGS.txt', sainsburysData, '<a href="http://www.sainsburys.co.uk/shop/gb/groceries/eggs', "/each", 'null')
    waitrosePrices = dataPull('URL_STORE/WAITROSE/EGGS.txt', waitroseData, 'null', "/each", 1)
    combinedPrices = aggregateLists(tescoPrices, sainsburysPrices, waitrosePrices)   
    if combinedPrices == 'null' : messagebox.showerror(title = "Extraction Failure", message = "All operations failed. No results to display.")
    else : results(combinedPrices)

def prodCrisps() :
    tescoPrices = dataPull('URL_STORE/TESCO/CRISPS.txt', tescoData, 'null', "/100g", 'null')
    sainsburysPrices = dataPull('URL_STORE/SAINSBURYS/CRISPS.txt', sainsburysData, '<a href="http://www.sainsburys.co.uk/shop/gb/groceries/crisps', "/100g", 'null')
    waitrosePrices = dataPull('URL_STORE/WAITROSE/CRISPS.txt', waitroseData, 'null', "/100g", 4)
    combinedPrices = aggregateLists(tescoPrices, sainsburysPrices, waitrosePrices)    
    if combinedPrices == 'null' : messagebox.showerror(title = "Extraction Failure", message = "All operations failed. No results to display.")
    else : results(combinedPrices)

def prodButter() :
    tescoPrices = dataPull('URL_STORE/TESCO/BUTTER.txt', tescoData, 'null', "/100g", 'null')
    sainsburysPrices = dataPull('URL_STORE/SAINSBURYS/BUTTER.txt', sainsburysData, '<a href="http://www.sainsburys.co.uk/shop/gb/groceries/butter', "/100g", 'null')
    waitrosePrices = dataPull('URL_STORE/WAITROSE/BUTTER.txt', waitroseData, 'null', "/100g", 2)
    combinedPrices = aggregateLists(tescoPrices, sainsburysPrices, waitrosePrices)    
    if combinedPrices == 'null' : messagebox.showerror(title = "Extraction Failure", message = "All operations failed. No results to display.")
    else : results(combinedPrices)
    
def prodIceCreamTubs() :
    tescoPrices = dataPull('URL_STORE/TESCO/ICE_CREAM_TUBS.txt', tescoData, 'null', "/100g", 'null')
    sainsburysPrices = dataPull('URL_STORE/SAINSBURYS/ICE_CREAM_TUBS.txt', sainsburysData, '<a href="http://www.sainsburys.co.uk/shop/gb/groceries/ice-cream-tubs', "/100g", 'null')
    waitrosePrices = dataPull('URL_STORE/WAITROSE/ICE_CREAM_TUBS.txt', waitroseData, 'null', "/100g", 6)
    combinedPrices = aggregateLists(tescoPrices, sainsburysPrices, waitrosePrices)   
    if combinedPrices == 'null' : messagebox.showerror(title = "Extraction Failure", message = "All operations failed. No results to display.")
    else : results(combinedPrices)

top.mainloop()

