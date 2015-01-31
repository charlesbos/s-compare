"""
extra.py

A module which contains functions for extra functionality such as supplying text to dialogues or creating error logs.
"""
import os
from tkinter import messagebox

def viewFile(fileName) :
    '''
    A function to read content from files and return either that content
    or else a keyword to indicate that the procedure failed.
    One argument taken, the name of the file form which to read the content.
    '''
    try :
        file = open(fileName, 'r')
        fileText = file.read()
        file.close()
        return fileText
    except IOError :
         return 'null'

def errorLog(time, message, listLengths, exceptDetails) :
    '''
    A function to write errors to a text file. Depending on the nature of the
    error, this function will write the following: time and date, lengths of
    price and item lists (if they are unequal), a programmer defined message
    and the details of the Python exception that was raised (if one was raised).
    NOTE: more than one function may call the this function, each supplying it's own
    bit of information.
    Four arguments are taken: the time and date (as formatted in strftime), the programmer
    defined message, the list lengths and the exception details. Arguments of 'null' are
    ignored.
    '''
    file = open('ERROR_LOG.txt', 'a')
    if time != 'null' : print(time, file = file)
    if exceptDetails != 'null' : print(exceptDetails, file = file)
    if listLengths != 'null' : print(listLengths, file = file)
    if message != 'null' : print(message + '\n' + ('-' * 100), file = file)
    file.close()

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
        except :
            pass
        
    

    
    
