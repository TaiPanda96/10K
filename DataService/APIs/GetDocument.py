from .GetCompanySummaryPage import fetch
from .GetCompanySummaryPage import EdgarSearchHashMap


from bs4 import BeautifulSoup
from bs4 import BeautifulSoup, SoupStrainer


import selenium
from selenium.webdriver.common.by import By

import urllib3
import time, requests, lxml
from bs4 import BeautifulSoup
import os
import sys
import re

def extraction(soup,searchterm):
    """ 
    Document Link [0] = the url for the 'File Name' (10-K for example) in .htm format
    
    """

    table  = soup.find('table',{'class':'tableFile'})
    base   = 'https://www.sec.gov'
    DocLink = []

    for rows in table.findAll('a', href=True):
       if rows:
           links = base + rows.get('href')
           DocLink.append(links)
           print(DocLink[0])
           return DocLink[0]



def parse(ticker,DocLink):
    blacklist = [
                    '[document]',
                    'noscript',
                    'header',
                    'html',
                    'meta',
                    'head', 
                    'input',
                    'script', 
                ]
    output = ''
    NewLink = str(DocLink).replace('https://www.sec.gov/ix?doc=/','https://www.sec.gov/')

    def createFile(text, blacklist):
        for elements in text:
            if elements.parent.name not in blacklist:
                output += '{}'.format(elements)
                f = open("/Users/taishanlin/Desktop/RootDirectory/DataSamples/{}.txt".format(ticker), "w")
                f.write(output)
                f.close()

    print("{}".format(ticker), " " + " is created")

    try:
        page    = requests.get(NewLink)
        DocSoup = BeautifulSoup(page.text, 'html.parser')
        text    = DocSoup.find_all(text=True)
        return createFile(text,blacklist)


    except:
        print(page.status_code,'\n', sys.exc_info())   
    

# Search for 10-K and/or 10-Q & Extract HTML Elements
def getDocument(ticker,searchterm):
    """
    Functions Purpose: \n
    getDocument searches for the file name from the extracted URLs table, then finds the matching URL based on the document search criteria. \n
    If a match is found, getDocument calls the extraction method to pull the Document's HTML. 


    Steps: \n
    1) Perform Initial Fetch of the ticker's URls table for a ticker \n
    2) Search 'File Name' in URls table \n
       a) If the 'File Name' is 10-K, then first search by 10-K. If no result is found, then search for 10-K/A. \n
       b) For any other document that isn't 10-K/10-K/A, search by 'File Name' in the URLs table \n
    3) If 'File Name' match is found, then open the URL containing this file name in the URLs table. \n
    4) Call Beautiful Soup to extract the html content of this 'File Name'.
    
    """
    
    data  = fetch(ticker,'QUERY')

    
    # If you are looking for 10-K but the name '10-K' does not exist in the list of file names extracted, then:
    if searchterm == '10-K' and data['File Link'].loc[data['File Name'] == searchterm] is None:
        # Try to look for a 10-K/A instead.
        searchterm == '10-K/A'
        query = data['File Link'].loc[data['File Name'] == searchterm]
    # In all other cases, search term is set to whatever the function argument specifies
    else:
        query = data['File Link'].loc[data['File Name'] == searchterm]

    
    for mainlink in query:
        print(mainlink)
        try:
            # Get to the company 10-K Page
            page = requests.get(mainlink)
            html = page.text
            soup = BeautifulSoup(html, 'html.parser')

            # Find the 10-K filing in .htm format
              # Call Parse which evokes extraction of the URL first, and then downloads the data.
              # The first document link is usually the .htm format.
            parse(ticker,DocLink=extraction(soup,searchterm))

        except:
            print(page.status_code,sys.exc_info())


# Main Executable #
getDocument('AMZN','10-K');
