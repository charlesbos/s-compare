S-Compare
=============

Python Web Scraping Project - Team S @ University of Essex

S-Compare is a program that collects grocery prices from a number
of major UK retailers, ensures that they are of a standard unit
(per 100 grams for example) and then displays that information in 
a table.

Dependencies:
* Python3
* Tkinter
* Python3-BeautifulSoup4
* Python3-Requests
* Python3-Selenium
* PhantomJS (other browsers can be used but this requires source
modification. For Windows it may also require downloading the
webdriver for the browser in question.)

Platforms known to work:
* GNU/Linux - tested on Arch Linux
* Microsoft Windows - tested on Windows 7

Browser config:
* For GNU/Linux, ensure that you have the browser you wish to use
installed to a standard location such as /usr/bin and ensure that
your distrbution's Selenium package includes the appropriate webdrivers.
* For Microsoft Windows, ensure that the webdriver for the browser
you are using is located either in the program directory or a directory
which is specified in PATH.
