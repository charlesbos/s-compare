"""
This program fetches prices for common groceries from a number of UK retailers, ensures the prices are of
a standard unit such as per 100 grams, sorts the prices from low to high and then outputs a table of results.

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
from tesco import tescoData
from sainsburys import sainsburysData
from waitrose import waitroseData
from morrisons import morriData
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from threading import Thread
from queue import Queue
import os
import tkinter.ttk as ttk
import webbrowser

class data() :
    def manager(fileName, unit, titleTagEnd, scroll, windowName) :
        '''
        This is the function called by the UI. It coordinates the fetching and displaying
        of results as well as the progressbar. The first 4 args are passed to the call function.
        '''
        # Ensure that only one progressbar window is started for parallel operations.
        # Try except is needed because the object won't be defined on first run.
        try :
            if not UI.runningWinObj.winfo_exists() : UI.runningWin()
        except :
            UI.runningWin()
        
        callThread = Thread(target = data.call, args = (fileName, unit, titleTagEnd, scroll))
        callThread.start() 
        Toplevel.destroy(windowName)

        # This is an ugly hack. Suggestions for better solutions are welcome.
        while True :
            if not callThread.isAlive() :
                data.outputHandler()
                break
            top.update()

    def call(fileName, unit, titleTagEnd, scroll) :
        '''
        This function is run in a separate thread and is called from manager. It calls dataPull to fetch results
        and then processes them. All args are passed to dataPull.
        '''
        tescoResults = data.dataPull('URL_STORE/TESCO/' + fileName, tescoData, 'null', unit, 'null')
        sainsburysResults = data.dataPull('URL_STORE/SAINSBURYS/' + fileName, sainsburysData, '<a href="http://www.sainsburys.co.uk/shop/gb/groceries/' + titleTagEnd, unit, 'null')
        waitroseResults = data.dataPull('URL_STORE/WAITROSE/' + fileName, waitroseData, 'null', unit, scroll)
        morrisonsResults = data.dataPull('URL_STORE/MORRISONS/' + fileName, morriData, 'null', unit, 'null')

        results = [tescoResults, sainsburysResults, waitroseResults, morrisonsResults]
        errors = []
        cheapest = []
        allPrices = []

        for x in results :
            if x[0] != [] : errors += x[0]
            if x[1] != [] :
                cheapest += data.lowestPrices(x[1])
                allPrices += x[1]

        allPricesFormatted = data.createTable(allPrices, "Prices from all shops")
        cheapestFormatted = data.createTable(cheapest, "Lowest prices from each shop")
        priceTable = cheapestFormatted + '\n' + allPricesFormatted

        if errors != [] : utility.writeErrors(errors)
        if allPrices == [] : outputQueue.put(("FullOperationsFailure",))
        elif (allPrices != []) and (errors != []) : outputQueue.put(("PartialOperationsFailure", priceTable))
        else : outputQueue.put((priceTable,))
    
    def dataPull(filePath, shopFunc, titletag, unit, scroll) :
        '''
        This fuction will call the shop module function for each url in a file and then
        return a tuple containing the results.
        '''
        urls = utility.viewFile(filePath)
        urls = urls.split('\n')
        urls = [x for x in urls if x != '']

        errors = []
        prices = []
        
        for x in range(len(urls)) :
            temp = shopFunc(urls[x], titletag, unit, scroll)
            if type(temp) == list : prices += temp
            if type(temp) == str : errors += [temp]

        return (errors, prices)

    def sortPrices(prices) :
        '''
        A bubble sort function for sorting our prices - needed because our price data
        is of type string.
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
        prices = data.sortPrices(prices)
        return [list(x) for x in prices if x[1] == prices[0][1]]

    def createTable(prices, tableHeader) :
        prices = data.sortPrices(prices)
        colHeaders = '{:96s}'.format("  Item title") + "Price per unit".ljust(15, ' ') + (' ' * 9) + "Retailer"
        priceTable = str(tableHeader).center(130, ' ') + '\n' + ('=' * len(tableHeader)).center(130, ' ') + '\n' + colHeaders + '\n' + ('-' * 130) + '\n'
        
        for x in range(len(prices)) :
            temp = '{:85s}'.format(prices[x][0]), prices[x][1].rjust(15, ' '), ' ' * 6, prices[x][2]
            priceTable += str(temp)
            priceTable += '\n' + ('-' * 130) + '\n'

        return priceTable.replace('"', ' ').replace("'", ' ').replace(',', ' ').replace('(', ' ').replace(')', ' ')

    def outputHandler() :
        '''
        This function destroys the progressbar window, fetches the processed results from the output
        queue and displays them along with any errors.
        '''
        Toplevel.destroy(UI.runningWinObj)
        output = outputQueue.get() 
        if output[0] == "FullOperationsFailure" : messagebox.showerror(title = "Operation failure", message = "All operations failed. No results to display. Check the logs for errors.")
        elif output[0] == "PartialOperationsFailure" :
            messagebox.showerror(title = "Some errors encountered", message = "Some operations failed. Not all results can be displayed. Check the logs for errors.")
            UI.results(output[1])
        else : UI.results(output[0])

class utility() :
    def contentFetch(funcName, fileName) :
        '''
        An intermediary function for passing data from files to the appropriate part
        of the UI.
        '''
        content = utility.viewFile(fileName)
        if funcName == UI.logViewer :
            if content == 'null' : messagebox.showinfo(title = "Logs", message = "No logs to display.")
            else : UI.logViewer(content)
        else :
            if content == 'null' : messagebox.showerror(title = "Content Failure", message = "Content not found. Please ensure the program has all the necessary files.")
            else : funcName(content)

    def viewFile(fileName) :
        '''
        A general purpose function for reading information from files. Normally it passes its
        contents to the contentFetch function.
        '''
        try :
            file = open(fileName, 'r', encoding = 'utf-8')
            fileText = file.read()
            file.close()
            return fileText
        except IOError :
             return 'null'

    def clearLogs() :
        choice = messagebox.askyesno(title = "Clear Logs?", message = "Would you like to delete the application's logs?")
        if choice == True :
            try :
                os.remove('ERROR_LOG.txt')
            except IOError :
                pass

    def writeErrors(errors) :
        file = open('ERROR_LOG.txt', 'a')
        for x in errors : print(x, file = file)
        file.close()

    def saveFile(content) :
        '''
        Use a Tkinter file dialog to allow the user to save content to a file.
        This is used for the results window in the UI.
        '''
        file = filedialog.asksaveasfile(mode = 'w', defaultextension = '.txt', initialfile = "results")
        if file != None : print(content, file = file)

class UI() :
    # Main window
    def __init__(self, parent) :
        label = Label(parent, text = 'This program compares prices for a number of common groceries. Please select a product category.', wraplength = 345, pady = 5, padx = 5, relief = SUNKEN)
        label.grid(row = 1, column = 1, columnspan = 3)
        button1 = Button(parent, text = "Bread", command = self.bread, height = 5, width = 10).grid(row = 2, column = 1)
        button2 = Button(parent, text = "Dairy", command = self.dairy, height = 5, width = 10).grid(row = 2, column = 2)
        button3 = Button(parent, text = "Crisps and Snacks", command = self.crisps_and_snacks, height = 5, width = 10, wraplength = 80).grid(row = 2, column = 3)
        button4 = Button(parent, text = "Drinks", command = self.drinks, height = 5, width = 10).grid(row = 3, column = 1)
        button5 = Button(parent, text = "Desserts", command = self.desserts, height = 5, width = 10).grid(row = 3, column = 2)
        button6 = Button(parent, text = "Fruit & Veg", command = self.fruit_and_veg, height = 5, width = 10).grid(row = 3, column = 3)
        button7 = Button(parent, text = "Quit", command = parent.destroy).grid(row = 4, column = 3, pady = 10)
        button8 = Button(parent, text = "Homepage", command = lambda : webbrowser.open("https://github.com/charlesbos/s-compare")).grid(row = 4, column = 1, pady = 10)
        button9 = Button(parent, text = "About", command = lambda : utility.contentFetch(self.about, 'ABOUT.txt')).grid(row = 4, column = 2, pady = 10)
        button10 = Button(parent, text = "View Logs", command = lambda : utility.contentFetch(UI.logViewer, 'ERROR_LOG.txt')).grid(row = 5, column = 1, pady = 5)
        button11 = Button(parent, text = "Clear Logs", command = utility.clearLogs).grid(row = 5, column = 2, pady = 5)

    # Product category windows
    def bread(self) :
        bread = Toplevel()
        bread.title("Compare - Bread")
        button1 = Button(bread, text = "Wholemeal Bread", height = 5, width = 12, wraplength = 80, command = lambda : data.manager('BROWN_BREAD.txt', '/100g', 'wholemeal-brown-bread/', 2, bread)).grid(row = 1, column = 1)
        button2 = Button(bread, text = "White Bread", height = 5, width = 12, command = lambda : data.manager('WHITE_BREAD.txt', "/100g", 'white-bread/', 2, bread)).grid(row = 1, column = 2)
        button3 = Button(bread, text = "Baguette", height = 5, width = 12, command = lambda : data.manager('BAGUETTES.txt', '/100g', 'baguettes-part-baked-bread/', 2, bread)).grid(row = 1, column = 3)
        button4 = Button(bread, text = "Rolls", height = 5, width = 12, command = lambda : data.manager('ROLLS.txt', '/each', 'rolls/', 1, bread)).grid(row = 2, column = 1)
        
    def dairy(self) :
        dairy = Toplevel()
        dairy.title("Compare - Dairy")
        button1 = Button(dairy, text = "Milk", height = 5, width = 12, command = lambda : data.manager('MILK.txt', '/100ml', 'fresh-milk/', 5, dairy)).grid(row = 1, column = 1)
        button2 = Button(dairy, text = "Butter", height = 5, width = 12, command = lambda : data.manager('BUTTER.txt', '/100g', 'butter/', 2, dairy)).grid(row = 1, column = 2)
        button3 = Button(dairy, text = "Eggs", height = 5, width = 12, command = lambda : data.manager('EGGS.txt', '/each', 'eggs/', 1, dairy)).grid(row = 1, column = 3)

    def crisps_and_snacks(self) :
        crisps_and_snacks = Toplevel()
        crisps_and_snacks.title("Compare - Crisps & Snacks")
        button1 = Button(crisps_and_snacks, text = "Crisps", height = 5, width = 12, command = lambda : data.manager('CRISPS.txt', '/100g', 'crisps/', 4, crisps_and_snacks)).grid(row = 1, column = 1)
        button2 = Button(crisps_and_snacks, text = "Cereal Bars", height = 5, width = 12, command = lambda : data.manager('CEREAL_BARS.txt', '/100g', 'breakfast-cereal-bars-breakfast-biscuits/', 3, crisps_and_snacks)).grid(row = 1, column = 2)
        button3 = Button(crisps_and_snacks, text = "Popcorn", height = 5, width = 12, command = lambda : data.manager('POPCORN.txt', '/100g', 'popcorn/', 5, crisps_and_snacks)).grid(row = 1, column = 3)

    def drinks(self) :
        drinks = Toplevel()
        drinks.title("Compare - Drinks")
        button1 = Button(drinks, text = "Still Water", height = 5, width = 12, command = lambda : data.manager('STILL_WATER.txt', '/100ml', 'still-water/', 4, drinks)).grid(row = 1, column = 1)
        button2 = Button(drinks, text = "Sparkling Water", height = 5, width = 12, command = lambda : data.manager('SPARKLING_WATER.txt', '/100ml', 'sparkling-water', 2, drinks)).grid(row = 1, column = 2)
        button3 = Button(drinks, text = "Everyday Tea", height = 5, width = 12, command = lambda : data.manager('EVERYDAY_TEA.txt', '/100g', 'everyday-tea/', 3, drinks)).grid(row = 1, column = 3)
        button4 = Button(drinks, text = "Cola", height = 5, width = 12, command = lambda : data.manager('COLA.txt', '/100ml', 'cola/', 4, drinks)).grid(row = 2, column = 1)
        button5 = Button(drinks, text = "Lager", height = 5, width = 12, command = lambda : data.manager('LAGER.txt', '/100ml', 'lager/', 6, drinks)).grid(row = 2, column = 2)
        button6 = Button(drinks, text = "Energy Drink", height = 5, width = 12, command = lambda : data.manager('ENERGY_DRINK.txt', '/100ml', 'energy-drinks/', 3, drinks)).grid(row = 2, column = 3)
        button7 = Button(drinks, text = "Instant Coffee", height = 5, width = 12, command = lambda : data.manager('INSTANT_COFFEE.txt', '/100g', 'instant-coffee/', 5, drinks)).grid(row = 3, column = 1)

    def desserts(self) :
        desserts = Toplevel()
        desserts.title("Compare - Desserts")
        button1 = Button(desserts, text = "Ice Cream Tubs", height = 5, width = 12, command = lambda : data.manager('ICE_CREAM_TUBS.txt', '/100ml', 'ice-cream-tubs/', 6, desserts)).grid(row = 1, column = 1)
        button2 = Button(desserts, text = "Ice Cream Cones", height = 5, width = 12, command = lambda : data.manager('ICE_CREAM_CONES_AND_STICKS.txt', '/100ml', 'lollies-bars-cones/', 4, desserts)).grid(row = 1, column = 2)
        button3 = Button(desserts, text = "Cakes and Tarts", height = 5, width = 12, command = lambda : data.manager('CAKES_AND_TARTS.txt', '/100g', 'frozen-cold-desserts/', 3, desserts)).grid(row = 1, column = 3)

    def fruit_and_veg(self) :
        fruit_and_veg = Toplevel()
        fruit_and_veg.title("Compare - Fruit & Veg")
        button1 = Button(fruit_and_veg, text = "Grapes", height = 5, width = 12, command = lambda : data.manager('GRAPES.txt', '/100g', 'bananas-grapes/', 4, fruit_and_veg)).grid(row = 1, column = 1)
        button2 = Button(fruit_and_veg, text = "Apples", height = 5, width = 12, command = lambda : data.manager('APPLES.txt', '/each', 'apples-pears-rhubarb/', 4, fruit_and_veg)).grid(row = 1, column = 2)
        button3 = Button(fruit_and_veg, text = "Salads", height = 5, width = 12, command = lambda : data.manager('SALADS.txt', '/100g', 'prepared-salad-herbs/', 4, fruit_and_veg)).grid(row = 1, column = 3)
        
    # Other windows
    def results(prices) :
        results = Toplevel()
        results.title("Results")
        frame1 = Frame(results)
        frame2 = Frame(results)
        frame1.pack(fill = BOTH, expand = YES)
        frame2.pack(side = BOTTOM)
        scrollbar = Scrollbar(frame1)
        scrollbar.pack(side = RIGHT, fill = Y)
        text = Text(frame1, height = 40, width = 135, wrap = WORD, yscrollcommand = scrollbar.set)
        scrollbar.config(command = text.yview)
        text.insert(END, prices)
        text.configure(state = DISABLED)
        text.pack(fill = BOTH, expand = YES)
        button1 = Button(frame2, text = "Close", command = results.destroy)
        button1.pack(side = RIGHT)
        button2 = Button(frame2, text = "Save to file", command = lambda : utility.saveFile(prices))
        button2.pack(side = LEFT)

    def about(self, content) :
        about = Toplevel()
        about.title("About")
        frame1 = Frame(about)
        frame2 = Frame(about)
        frame1.pack(fill = BOTH, expand = YES)
        frame2.pack(side = BOTTOM)
        label = Label(frame1, text = content, padx = 5, pady = 5)
        label.pack(fill = BOTH, expand = YES)
        button1 = Button(frame2, text = "License", command = lambda : utility.contentFetch(self.licenseWin, 'LICENSE.txt'))
        button1.pack(side = LEFT)
        button2 = Button(frame2, text = "Changelog", command = lambda : utility.contentFetch(self.changelogWin, 'CHANGELOG.txt'))
        button2.pack(side = LEFT)
        button3 = Button(frame2, text = "Close", command = about.destroy)
        button3.pack(side = RIGHT)

    def licenseWin(self, content) :
        licenseWin = Toplevel()
        licenseWin.title("License")
        frame1 = Frame(licenseWin)
        frame2 = Frame(licenseWin)
        frame1.pack(fill = BOTH, expand = YES)
        frame2.pack(side = BOTTOM)
        scrollbar = Scrollbar(frame1)
        scrollbar.pack(side = RIGHT, fill = Y)
        text = Text(frame1, height = 40, width = 160, wrap = WORD, yscrollcommand = scrollbar.set)
        scrollbar.config(command = text.yview)
        text.insert(END, content)
        text.configure(state = DISABLED)
        text.pack(fill = BOTH, expand = YES)
        button1 = Button(frame2, text = "Close", command = licenseWin.destroy)
        button1.pack(side = TOP)

    def changelogWin(self, content) :
        changelogWin = Toplevel()
        changelogWin.title("Changelog")
        frame1 = Frame(changelogWin)
        frame2 = Frame(changelogWin)
        frame1.pack(fill = BOTH, expand = YES)
        frame2.pack(side = BOTTOM)
        scrollbar = Scrollbar(frame1)
        scrollbar.pack(side = RIGHT, fill = Y)
        text = Text(frame1, height = 40, width = 160, wrap = WORD, yscrollcommand = scrollbar.set)
        scrollbar.config(command = text.yview)
        text.insert(END, content)
        text.configure(state = DISABLED)
        text.pack(fill = BOTH, expand = YES)
        button1 = Button(frame2, text = "Close", command = changelogWin.destroy)
        button1.pack(side = TOP)

    def logViewer(content) :
        logViewer = Toplevel()
        logViewer.title("Logs")
        frame1 = Frame(logViewer)
        frame2 = Frame(logViewer)
        frame1.pack(fill = BOTH, expand = YES)
        frame2.pack(side = BOTTOM)
        scrollbar = Scrollbar(frame1)
        scrollbar.pack(side = RIGHT, fill = Y)
        text = Text(frame1, height = 40, width = 80, wrap = WORD, yscrollcommand = scrollbar.set)
        scrollbar.config(command = text.yview)
        text.insert(END, content)
        text.configure(state = DISABLED)
        text.pack(fill = BOTH, expand = YES)
        button1 = Button(frame2, text = "Close", command = logViewer.destroy)
        button1.pack(side = LEFT)

    def runningWin() :
        UI.runningWinObj = Toplevel()
        UI.runningWinObj.title("Processing")
        UI.runningWinObj.wm_attributes("-topmost", 1)
        frame1 = Frame(UI.runningWinObj)
        frame2 = Frame(UI.runningWinObj)
        frame1.pack()
        frame2.pack(side = BOTTOM)
        label = Label(frame1, text = "Please wait a moment for the results...", pady = 30)
        label.pack()
        progressbar = ttk.Progressbar(frame2, mode = 'indeterminate', length = 350)
        progressbar.pack()
        progressbar.start()

# Initialise queue for data output
outputQueue = Queue()

# Start the interface
top = Tk()
top.title("S-Compare")
ui = UI(top)
top.mainloop()
