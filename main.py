"""
A very small demo program to kick off the coding process for this project.
It downloads the html for a given url and the parses that into a string we
can work with. Then it extracts links that behin with www. and prints them.
As some links can be very, very long, I've truncated them to a manageable
length. It's a bit crude but at least it's a start.

Created by Charles Bos on 2014/11/13
"""

from bs4 import BeautifulSoup
import requests

print("Note: An entered URL must begin with http:// or https://")
print("Note: If a URL cannot be found, the program will hang and then crash")
url = input("\nPlease enter a URL: ")

response = requests.get(url)

htmlString = str(BeautifulSoup(response.content))

findLinks = htmlString.find('www.')
findLinkEnds = htmlString.find('"',findLinks)
linkExtract = htmlString[findLinks:findLinkEnds]
linkFormat = linkExtract.partition(' ')

if findLinks == -1 : print("No links here. Sorry.")
else :
    while htmlString[findLinkEnds] != htmlString[-1] :
        print(str(linkFormat[:1]).replace(',', ' ').replace('"', '').replace("'", '').strip('()')[:150],'\n')
        htmlString = str(htmlString[findLinkEnds:])
        findLinks = htmlString.find('www.')
        findLinkEnds = htmlString.find('"',findLinks)
        linkExtract = htmlString[findLinks:findLinkEnds]
        linkFormat = linkExtract.partition(' ')
