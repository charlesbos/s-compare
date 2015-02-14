"""
main.py

This file imports the various modules for each shop, calls the functions and
then outputs the data returned by them.
"""
from tesco import tescoData
from sainsburys import sainsburysData
from waitrose import waitroseData
from tkinter import *
from tkinter import messagebox
from threading import Thread
from queue import Queue
import os
import tkinter.ttk as ttk
import time

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
    file = open(filePath, 'r')
    urls = str(file.read()).split('\n')
    urls = [x for x in urls if x != '']
    
    for x in range(len(urls)) :
        temp = shopFunc(urls[x], titletag, unit, scroll)
        if type(temp) == list : queue1.put(temp)
        if type(temp) == str : queue2.put([temp])

def call(fileName, unit, titleTagEnd, scroll) :
    '''
    A function for calling dataPull, displaying an error message if there are no results and destroying
    the current window. See the dataPull documentation.
    '''    
    dataPull('URL_STORE/TESCO/' + fileName, tescoData, 'null', unit, 'null')
    dataPull('URL_STORE/SAINSBURYS/' + fileName, sainsburysData, '<a href="http://www.sainsburys.co.uk/shop/gb/groceries/' + titleTagEnd, unit, 'null')
    dataPull('URL_STORE/WAITROSE/' + fileName, waitroseData, 'null', unit, scroll)

    combinedPrices = []
    while not queue1.empty() : combinedPrices.append(queue1.get())

    errors = []
    while not queue2.empty() : errors += queue2.get()

    if errors != [] : writeErrors(errors)

    if combinedPrices == [] : messagebox.showerror(title = "Extraction Failure", message = "All operations failed. No results to display. Check the logs.")
    elif (combinedPrices != []) and (errors != []) :
        messagebox.showerror(title = "Extraction Failure", message = "Some operations failed. Not all results can be displayed. Check the logs.")
        priceTable = aggregateLists(combinedPrices)
        results(priceTable)
    else :
        priceTable = aggregateLists(combinedPrices)
        results(priceTable)

    Toplevel.destroy(runningWinObj)

def aggregateLists(prices) :
    '''
    A function for aggregating the lists that have been returned by the shop modules.
    One argument accepted: the list that was created from the lists placed in the queue
    by the threads started in the call function.
    '''
    allPrices = []
    cheapest = []

    for x in prices : allPrices += x

    tescoPrices = sainsburysPrices = waitrosePrices = []       
    tescoPrices = [x for x in allPrices if x[-1] == "Tesco"]
    sainsburysPrices = [x for x in allPrices if x[-1] == "Sainsburys"]
    waitrosePrices = [x for x in allPrices if x[-1] == "Waitrose"]

    shopAggLists = [tescoPrices, sainsburysPrices, waitrosePrices]
    for x in shopAggLists : cheapest += lowestPrices(x)

    allPrices = createTable(allPrices, "== Prices from all shops ==")
    cheapest = createTable(cheapest, "== Lowest prices from each shop ==")

    return str(cheapest + '\n' + allPrices)

def sortPrices(prices) :
    '''
    A function to correctly sort the lists of tuples by price. Using the sorted function does not
    always work correctly because our prices are strings, not floats.
    One argument is accepted, the list of prices to be sorted.
    '''
    x = 0
    y = 1

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
    
    for x in range(len(prices)) :
        temp = '{:85s}'.format(prices[x][0]), prices[x][1].rjust(15, ' '), ' ' * 6, prices[x][2]
        priceTable += str(temp)
        priceTable += '\n' + ('-' * 130) + '\n'

    return priceTable.replace('"', ' ').replace("'", ' ').replace(',', ' ').replace('(', ' ').replace(')', ' ')

def manager(fileName, unit, titleTagEnd, scroll, windowName) :
    '''
    A function which starts the progress bar window and then concurrently
    starts the call function which handles the fetching and processing of the required data.
    The last argument is the name of the product category window to destroy. For the other
    four arguments, see the dataPull fuction.
    '''
    runningWin()
    global callThread
    callThread = Thread(target = call, args = (fileName, unit, titleTagEnd, scroll))
    callThread.start()
    timeWarningThread = Thread(target = timeWarning, args = ())
    timeWarningThread.start()
    Toplevel.destroy(windowName)

def timeWarning() :
    '''
    A function that offers to close the program if an operation takes 30 seconds to complete.
    If the user answers no and the operation still hangs, the user will be prompted every 15
    seconds thereafter.
    '''
    counter = 0
    period = 30
    while callThread.isAlive() :
        time.sleep(1)
        counter += 1
        if counter == period :
            choice = messagebox.askyesno(title = "Slow running operation", message = "Operation is taking too long. Would you like to close the program and try again?") 
            if choice == True : os._exit(0)
            else : period += 15

# Utility functions
def contentFetch(funcName, fileName) :
    '''
    A function to pass content from text files to the function defining the appropriate
    program window or else display a message in a pop up window if the content cannot
    be found.
    Two arguments taken: the name of the function defining the relevant program window
    and the filename from which to extract the content.
    '''
    content = viewFile(fileName)
    if funcName == logViewer :
        if content == 'null' : messagebox.showinfo(title = "Logs", message = "No logs to display.")
        else : logViewer(content)
    else :
        if content == 'null' : messagebox.showerror(title = "Content Failure", message = "Content not found. Please ensure the program has all the necessary files.")
        else : funcName(content)

def viewFile(fileName) :
    '''
    A function to read content from files and return either that content
    or else a keyword to indicate that the procedure failed.
    One argument taken, the name of the file form which to read the content.
    '''
    try :
        file = open(fileName, 'r', encoding = 'utf-8')
        fileText = file.read()
        file.close()
        return fileText
    except IOError :
         return 'null'

def clearLogs() :
    '''
    A function which uses the tkinter messagebox to ask the user if they
    would like to clear the logs. If the answer is yes, the program will
    attempt to delete the error log file.
    No arguments taken.
    '''
    choice = messagebox.askyesno(title = "Clear Logs?", message = "Would you like to delete the application's logs?")
    if choice == True :
        try :
            os.remove('ERROR_LOG.txt')
        except IOError :
            pass

def writeErrors(errors) :
    '''
    A funtion to write the errors collected in queue2 and then extracted to the
    error log file.
    '''
    file = open('ERROR_LOG.txt', 'w')
    for x in errors : print(x, file = file)
    file.close()

# Initialise windows
top = Tk()
top.title("Team S Scrape")
frame1 = Frame(top).grid()
frame2 = Frame(top).grid()
frame3 = Frame(top).grid()
queue1 = Queue()
queue2 = Queue()

def bread() :
    '''
    Defines the window for bread products.
    No arguments taken.
    '''
    bread = Toplevel()
    bread.title("Compare - Bread")
    button1 = Button(bread, text = "Wholemeal Bread", height = 5, width = 12, wraplength = 80, command = lambda : manager('BROWN_BREAD.txt', '/100g', 'wholemeal-brown-bread/', 2, bread)).grid(row = 1, column = 1)
    button2 = Button(bread, text = "White Bread", height = 5, width = 12, command = lambda : manager('WHITE_BREAD.txt', "/100g", 'white-bread/', 2, bread)).grid(row = 1, column = 2)
    
def dairy() :
    '''
    Defines the window for dairy products.
    No arguments taken.
    '''
    dairy = Toplevel()
    dairy.title("Compare - Dairy")
    button1 = Button(dairy, text = "Milk", height = 5, width = 12, command = lambda : manager('MILK.txt', '/100ml', 'fresh-milk/', 5, dairy)).grid(row = 1, column = 1)
    button2 = Button(dairy, text = "Butter", height = 5, width = 12, command = lambda : manager('BUTTER.txt', '/100g', 'butter/', 2, dairy)).grid(row = 1, column = 2)
    button3 = Button(dairy, text = "Eggs", height = 5, width = 12, command = lambda : manager('EGGS.txt', '/each', 'eggs/', 1, dairy)).grid(row = 1, column = 3)

def crisps_and_snacks() :
    '''
    Defines the window for crisps and snacks products.
    No arguments taken.
    '''
    crisps_and_snacks = Toplevel()
    crisps_and_snacks.title("Compare - Crisps & Snacks")
    button1 = Button(crisps_and_snacks, text = "Crisps", height = 5, width = 12, command = lambda : manager('CRISPS.txt', '/100g', 'crisps/', 4, crisps_and_snacks)).grid(row = 1, column = 1)
    button2 = Button(crisps_and_snacks, text = "Cereal Bars", height = 5, width = 12, command = lambda : manager('CEREAL_BARS.txt', '/100g', 'breakfast-cereal-bars-breakfast-biscuits/', 3, crisps_and_snacks)).grid(row = 1, column = 2)

def drinks() :
    '''
    Defines the window for drinks products.
    No arguments taken.
    '''
    drinks = Toplevel()
    drinks.title("Compare - Drinks")
    button1 = Button(drinks, text = "Still Water", height = 5, width = 12, command = lambda : manager('STILL_WATER.txt', '/100ml', 'still-water/', 4, drinks)).grid(row = 1, column = 1)
    button2 = Button(drinks, text = "Sparkling Water", height = 5, width = 12, command = lambda : manager('SPARKLING_WATER.txt', '/100ml', 'sparkling-water', 2, drinks)).grid(row = 1, column = 2)
    button3 = Button(drinks, text = "Everyday Tea", height = 5, width = 12, command = lambda : manager('EVERYDAY_TEA.txt', '/100g', 'everyday-tea/', 3, drinks)).grid(row = 1, column = 3)

def deserts() :
    '''
    Defines the window for deserts products.
    No arguments taken.
    '''
    deserts = Toplevel()
    deserts.title("Compare - Deserts")
    button1 = Button(deserts, text = "Ice Cream Tubs", height = 5, width = 12, command = lambda : manager('ICE_CREAM_TUBS.txt', '/100g', 'ice-cream-tubs/', 6, deserts)).grid(row = 1, column = 1)

def fruit_and_veg() :
    '''
    Defines the window for fruit and veg products.
    No arguments taken.
    '''
    fruit_and_veg = Toplevel()
    fruit_and_veg.title("Compare - Fruit & Veg")

def results(prices) :
    '''
    Defines the window in which to display the results.
    One argument taken. A string containing the product titles and prices
    which is formatted to appear like a table. This is displayed in the
    tkinter text module.
    '''
    results = Toplevel()
    results.title("Results")
    frame1 = Frame(results)
    frame2 = Frame(results)
    frame1.pack()
    frame2.pack(side = BOTTOM)
    scrollbar = Scrollbar(frame1)
    scrollbar.pack(side = RIGHT, fill = Y)
    text = Text(frame1, height = 40, width = 132, yscrollcommand = scrollbar.set)
    scrollbar.config(command = text.yview)
    text.insert(END, prices)
    text.configure(state = DISABLED)
    text.pack()
    button1 = Button(frame2, text = "Close", command = results.destroy)
    button1.pack(side = TOP)

def about(content) :
    '''
    Defines the window which displays the about dialogue.
    One argument taken: a string containing the about text.
    This is displayed in the tkinter text module.
    '''
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
    '''
    Defines the window which displays the license (this is accessible from the
    about window).
    One argument taken: the string containing the license which is displayed in
    the tkinter text module.
    '''
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
    '''
    Defines the window which displays the changelog (this is accessible from the
    about window).
    One argument taken: the string containing the changelog which is displayed in
    the tkinter text module.
    '''
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
    '''
    Defines the window which displays the error log.
    One argument taken: the string containing the log which is displayed in
    the tkinter text module.
    '''
    logViewer = Toplevel()
    logViewer.title("Logs")
    frame1 = Frame(logViewer)
    frame2 = Frame(logViewer)
    frame1.pack()
    frame2.pack(side = BOTTOM)
    scrollbar = Scrollbar(frame1)
    scrollbar.pack(side = RIGHT, fill = Y)
    text = Text(frame1, height = 40, width = 80, yscrollcommand = scrollbar.set)
    scrollbar.config(command = text.yview)
    text.insert(END, content)
    text.configure(state = DISABLED)
    text.pack()
    button1 = Button(frame2, text = "Close", command = logViewer.destroy)
    button1.pack(side = LEFT)

def runningWin() :
    '''
    A function which defines a window with an indeterminate progressbar.
    '''    
    global runningWinObj
    runningWinObj = Toplevel()
    runningWinObj.title("Processing")
    frame1 = Frame(runningWinObj)
    frame2 = Frame(runningWinObj)
    frame1.pack()
    frame2.pack(side = BOTTOM)
    label = Label(frame1, text = "Please wait a moment for the results...", pady = 30)
    label.pack()
    progressbar = ttk.Progressbar(frame2, mode = 'indeterminate', length = 350)
    progressbar.pack()
    progressbar.start()

label = Label(frame1, text = 'This program compares prices for a number of common groceries. Please select a product category below.', wraplength = 345, pady = 5, padx = 5, relief = SUNKEN)
label.grid(row = 1, column = 1, columnspan = 3)

button1 = Button(frame2, text = "Bread", command = bread, height = 5, width = 10).grid(row = 2, column = 1)
button2 = Button(frame2, text = "Dairy", command = dairy, height = 5, width = 10).grid(row = 2, column = 2)
button3 = Button(frame2, text = "Crisps and Snacks", command = crisps_and_snacks, height = 5, width = 10, wraplength = 80).grid(row = 2, column = 3)
button4 = Button(frame2, text = "Drinks", command = drinks, height = 5, width = 10).grid(row = 3, column = 1)
button5 = Button(frame2, text = "Deserts", command = deserts, height = 5, width = 10).grid(row = 3, column = 2)
button6 = Button(frame2, text = "Fruit & Veg", command = fruit_and_veg, height = 5, width = 10, state = DISABLED).grid(row = 3, column = 3)
button7 = Button(frame3, text = "Quit", command = top.destroy).grid(row = 4, column = 3, pady = 10)
button8 = Button(frame3, text = "Help", state = DISABLED).grid(row = 4, column = 1, pady = 10)
button9 = Button(frame3, text = "About", command = lambda : contentFetch(about, 'ABOUT.txt')).grid(row = 4, column = 2, pady = 10)
button10 = Button(frame3, text = "View Logs", command = lambda : contentFetch(logViewer, 'ERROR_LOG.txt')).grid(row = 5, column = 1, pady = 5)
button11 = Button(frame3, text = "Clear Logs", command = clearLogs).grid(row = 5, column = 2, pady = 5)

top.mainloop()

