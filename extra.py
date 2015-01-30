"""
extra.py

A module which contains functions for extra functionality such as supplying text to dialogues or creating error logs.
"""
import os
from tkinter import messagebox

def viewFile(fileName) :
    try :
        file = open(fileName, 'r')
        fileText = file.read()
        file.close()
        return fileText
    except IOError :
         return 'null'

def errorLog(time, message, listLengths, exceptDetails) :
    file = open('ERROR_LOG.txt', 'a')
    if time != 'null' : print(time, file = file)
    if exceptDetails != 'null' : print(exceptDetails, file = file)
    if listLengths != 'null' : print(listLengths, file = file)
    if message != 'null' : print(message + '\n' + ('-' * 100), file = file)
    file.close()

def clearLogs() :
    choice = messagebox.askyesno(title = "Clear Logs?", message = "Would you like to delete the application's logs?")
    if choice == True :
        try :
            os.remove('ERROR_LOG.txt')
        except :
            pass
        
    

    
    
