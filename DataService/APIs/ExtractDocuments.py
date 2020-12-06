import GetCompanyDocuments as GetCompanyDocuments
from GetCompanyDocuments import fetch
from GetCompanyDocuments import EdgarSearchHashMap
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup, SoupStrainer


import selenium
from selenium.webdriver.common.by import By

import urllib3
import time, requests, lxml
from collections import OrderedDict
from bs4 import BeautifulSoup
import os
import sys
import re

def extraction(soup,searchterm):

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
    print('Old Link = ',DocLink,'\n','New Link=', NewLink)
    try:
        page    = requests.get(NewLink)
        DocSoup = BeautifulSoup(page.text, 'html.parser')
        text    = DocSoup.find_all(text=True)

        for elements in text:
            if elements.parent.name not in blacklist:
                output += '{}'.format(elements)
                f = open("/Users/taishanlin/Desktop/RootDirectory/DataSamples/{}.txt".format(ticker), "w")
                f.write(output)
                f.close()

    except:
        print(page.status_code,'\n', sys.exc_info())   
    

# Search for 10-K and/or 10-Q & Extract HTML Elements
def getDocument(ticker,searchterm):
    """1.Search method identifies the search criteria from previously extracted URLs table for a given ticker, and then opens the appropriate URL that matches the search criteria.
    Then, search method calls the extraction method to pull the Document's HTML. """
    data  = fetch(ticker,'QUERY')
    #print(data['FileName'],data['File Link'])

    # If you are looking for 10-K but the name '10-K' does not exist in the list of file names extracted, then:
    if searchterm == '10-K' and data['File Link'].loc[data['FileName']==searchterm] is None:
        # Try to look for a 10-K/A instead.
        searchterm == '10-K/A'
        query = data['File Link'].loc[data['FileName'] == searchterm]
    # In all other cases, search term is set to whatever the function argument specifies
    else:
        query = data['File Link'].loc[data['FileName'] == searchterm]

    # Add logic to factor in 10-K or 10-K/A
    #print(query)
    
    for mainlink in query:
        print(mainlink)
        try:
            # root = os.path.join(os.path.dirname(__file__), 'chromedriver')
            # driver = selenium.webdriver.Chrome(executable_path=root)
            # Get to the company 10-K Page
            page = requests.get(mainlink)
            html = page.text
            soup = BeautifulSoup(html, 'html.parser')
            print('This step')
            # Find the 10-K filing in .htm format
            # Call Parse which evokes extraction of the URL first, and then downloads the data.
            parse(ticker,DocLink=extraction(soup,searchterm))

        except:
            print(page.status_code,sys.exc_info())


# Main Executable
getDocument('AMZN','10-K');
