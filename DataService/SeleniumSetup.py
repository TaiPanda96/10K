import selenium as selenium
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.command import Command

from GetProjectPath import get_project_root

import os
import sys
import tickers


# base url: https://www.sec.gov/cgi-bin/browse-edgar?company=&match=&CIK=GOOGL&filenum=&State=&Country=&SIC=&owner=exclude&Find=Find+Companies&action=getcompany

class EdgarSearch:

    def __init__(self):
        self.url     = 'https://www.sec.gov/cgi-bin/browse-edgar?company=&match=&CIK=GOOGL&filenum=&State=&Country=&SIC=&owner=exclude&Find=Find+Companies&action=getcompany'
        self.ticker  = None
        self.HashMap = {}
         
    def getTicker(self,tickers):
        """Takes the list of tickers and converts them into a ticker: url key,value pair. """
        self.ticker = tickers
        #print(self.ticker)
        urls = []

        # Build Query
        for i in self.ticker:
            urls.append('https://www.sec.gov/cgi-bin/browse-edgar?company=&match=&CIK={}'.format(i) + '&filenum=&State=&Country=&SIC=&owner=exclude&Find=Find+Companies&action=getcompany')

        self.HashMap = {self.ticker[i]: urls[i] for i in range(len(tickers))}

        return self.HashMap
        
def rowQuery(driver):
    queries = []
    for i in range(0,5):
        row = driver.find_elements_by_xpath("//table/tbody/tr/td[{}]".format(i))
        queries.append(row)
    #print(queries)
    return queries


def extractRow(driver,rowNum):
    rowNum = rowNum + 1
    terms  = rowQuery(driver)

    rData = []
    rCols = []
    for term in rowQuery(driver):
        row = term
        for files in row:
            rData.append(files.text)
    table = pd.DataFrame(rData)
    print(table)
    return table
    
    
  
def seleniumDriver(url):
    root = os.path.join(os.path.dirname(__file__), 'chromedriver')

    # Send a get request via the webdriver.
    # Then, check if you can find the element 10-K and/or 10-Q for each ticker.
    try: 
        driver = webdriver.Chrome(executable_path=str(root))
        driver.get(url)
        # assert (driver.title == "Edgar Search Results"), "The URL fetch was successful"
        # Execute a function that finds the 10-K and retrieves the clickable href 'Document' and 'Interactive Data' for further parsing.
        extractRow(driver,rowNum=1)

    except:
        print(sys.exc_info()[0],'\n',sys.exc_info()[1])


def main():
    getRequest = EdgarSearch()
    getRequest.getTicker(tickers.tickers)
    seleniumDriver(getRequest.url)

main();