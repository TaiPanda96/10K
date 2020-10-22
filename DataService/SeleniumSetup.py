import selenium as selenium
import json
import multiprocessing
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.command import Command

from GetProjectPath import get_project_root

import os
import sys
import tickers


# base url: https://www.sec.gov/cgi-bin/browse-edgar?company=&match=&CIK=GOOGL&filenum=&State=&Country=&SIC=&owner=exclude&Find=Find+Companies&action=getcompany

class EdgarSearchHashMap:
    """This class is meant to parse data from SEC website and store a Hashmap of harvested data where PK = Ticker
       create method takes a list of tickers and generates a basic hashmap where key = ticker value = url """

    def __init__(self,ticker):
        self.ticker  = str(ticker) 
        self.HashMap = {}

    def request(self):
        urls = 'https://www.sec.gov/cgi-bin/browse-edgar?company=&match=&CIK={}'.format(self.ticker) + '&filenum=&State=&Country=&SIC=&owner=exclude&Find=Find+Companies&action=getcompany'
        self.HashMap[self.ticker] = urls
        #print(self.HashMap)
        return self.HashMap


    def upsert(self,data,link,ticker):
        """Search if a key exists"""
        if ticker in self.HashMap:
            # If the ticker exists in the Hash, then call 2 executables below to add nested data + links
            self.HashMap['data']  = data
            self.HashMap['data']['links'] = link
            return self.HashMap
        else:
            # Else, you need to create the Hash first
            # Then call 2 executables below to add nested data + links
            self.request()
            self.HashMap['data']  = data
            self.HashMap['links'] = link
            #print(self.HashMap)
            return self.HashMap

def jsonMethod(response,ticker):
    with open('{}.json'.format(ticker),'w') as outfile:
        return json.dump(response, outfile,indent=4)


def rowQuery(driver,input):
    row = driver.find_elements_by_xpath("//table/tbody/tr/td[{}]".format(input))
    return row

def rowLinkQuery(driver,input):
    row = driver.find_elements_by_xpath("//a[@href]")
    return row

def extractRow(driver,passTo):
    fileName = []
    fileLink = []
    fileDesc = []
    fileDate = []

    for data in rowQuery(driver,1):
        fileName.append(data.text)

    for data in rowLinkQuery(driver,2):
        fileLink.append(data.get_attribute("href"))

    for data in rowQuery(driver,3):
        fileDesc.append(data.text)

    for data in rowQuery(driver,4):
        fileDate.append(data.text)
    
    cols  =  ["fileName", "fileLink", "fileDesc", "fileDate"]
    table = pd.DataFrame(list(zip(fileName,fileLink,fileDesc,fileDate)), columns=cols)
    
    if passTo == "Hashmap":
        nestedData = table.to_dict('index')
        #print(nestedData)
        return nestedData 

    elif passTo == "Query":
        #print(table)
        return table 


def extractDocumentLink(driver):
    element     = driver.find_elements_by_xpath("//a[@href]")
    #links       = pd.DataFrame(data=[elem.get_attribute("href") for elem in element])
    links       = [elem.get_attribute("href") for elem in element]
    linksmap    = {i : links[i] for i in range(len(links))}
    #print(links)
    return linksmap
  

# Main Executable Function
def seleniumDriver(ticker):
    root = os.path.join(os.path.dirname(__file__), 'chromedriver')

    # Send a get request via the webdriver.
    # Then, check if you can find the element 10-K and/or 10-Q for each ticker.
    try: 
        driver      = webdriver.Chrome(executable_path=str(root))

        # Example: 'GOOGL'
        getRequest  = EdgarSearchHashMap(ticker).request()

        driver.get(getRequest[ticker])
        # Execute a function that finds the 10-K and retrieves the clickable href 'Document' and 'Interactive Data' for further parsing.
        data     = extractRow(driver,"Hashmap")
        link     = extractDocumentLink(driver)

        # Save File in JSON format
        response = EdgarSearchHashMap(ticker).upsert(data,link,ticker)
        jsonfile = jsonMethod(response,ticker)
        
        
    except:
        print(sys.exc_info()[0],'\n',sys.exc_info()[1])


def main():
    seleniumDriver('AAPL')


main();