"""
extra.py

A module which contains functions for extra functionality such as supplying text to dialogues or creating error logs.
"""
import os
from tkinter import messagebox

def aboutText() :
    file = open('ABOUT.txt', 'r')
    about = file.read()
    file.close()
    return about

def licenseView() :
    file = open('LICENSE.txt', 'r')
    gpl = file.read()
    file.close()
    return gpl

def changelogView() :
    file = open('CHANGELOG.txt', 'r')
    changelog = file.read()
    file.close()
    return changelog

def errorLog(time, message, listLengths, exceptDetails) :
    file = open('ERROR_LOG.txt', 'a')
    if time != 'null' : print(time, file = file)
    if exceptDetails != 'null' : print(exceptDetails, file = file)
    if listLengths != 'null' : print(listLengths, file = file)
    if message != 'null' : print(message + '\n' + ('-' * 100), file = file)
    file.close()

def viewLogs() :
    try :
        file = open('ERROR_LOG.txt', 'r')
        logs = file.read()
        file.close()
        return logs
    except IOError :
         return 'null'

def clearLogs() :
    choice = messagebox.askyesno(title = "Clear Logs?", message = "Would you like to delete the application's logs?")
    if choice == True :
        try :
            os.remove('ERROR_LOG.txt')
        except :
            pass
        
    

    
    
