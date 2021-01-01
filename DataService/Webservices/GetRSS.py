# CORE IMPORTS
import bs4
from bs4 import BeautifulSoup, SoupStrainer
import urllib3


# OTHER IMPORT DEPENDENCIES
import os
import time, requests, lxml
import string 
import re
import sys
import datetime
import json

print(sys.path)

# Adds higher directory to python modules path.
sys.path.append(".") 
# MODULE IMPORT: CIK Hashmap
from Webservices.GetCIK import cik_map
# from GetCIK import cik_map


# MAIN CLASS
class RSS:
    """This class is meant to parse data from SEC website and store a Hashmap of harvested data where PK = Ticker
       create method takes a list of tickers and generates a basic hashmap where key = ticker value = url """

    def __init__(self,feedname):
        self.ticker  = str(feedname) 
        self.HashMap = {}

    
    def getRSS(self,key):
        Filings               = 'https://www.sec.gov/Archives/edgar/usgaap.rss.xml'
        MutualFundFilings     = 'https://www.sec.gov/Archives/edgar/xbrl-rr.rss.xml'
        FinancialStatements   = 'https://www.sec.gov/Archives/edgar/xbrl-inline.rss.xml'

        self.HashMap['Filings']               = Filings
        self.HashMap['Mutual Fund Filings']   = MutualFundFilings
        self.HashMap['Financial Statements']  = FinancialStatements
        return self.HashMap[key]

    
    def insertRSS(self,data):
        self.HashMap['data']  = data
        return self.HashMap



def request(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.text
        soup = BeautifulSoup(data,features='lxml')
    else:
        print(response.status_code)
    return soup


def extractRSSData(soup,cikHash):
    table    = soup.find_all('item')
    Items    = []
    filings  = {}
    

    for items in table:
        
        data     = items.text
        elements = data.split('\n')
        result   = list(filter(lambda x: x != '',elements))
        
        Items.append(result)
        #print(Items)

        # Remember you need to left strip CIK to remove the leading 0s
        Company            = { 'Company'  : data[0] for data in Items }
        Links              = { 'Links'    : [ data[1], data[2]] for data in Items }
        Document           = { 'Document' : data[3] for data in Items }
        FilingDate         = { 'FilingDate'  : data[4] for data in Items }
        OperatingName      = { 'Company Operating Name'  : data[5] for data in Items }
        CIK                = { 'CIK'  : data[8].lstrip('0') for data in Items }
        PublicationDate    = { 'Publication Date'  : data[7] for data in Items }

        info = [
            Company,
            Links,
            Document,
            FilingDate,
            OperatingName,
            CIK,
            PublicationDate
        ]

        # Add the ticker to the JSON.
        Company = [item for item in info[0].values()]
        # Add the CIK # to the JSON.
        CIK  = [item for item in info[5].values()]

        # Perform a lookup against your CIK Mapping
            # IF there is a match by CIK key, THEN update the key with the matching ticker value 
            # This produces the key value pair of ticker, info for your JSON.

        if CIK[0] in cikHash:
            ticker = cikHash['{}'.format(CIK[0])]
            filings['{}'.format(ticker)] = info
        else:
            filings['{}'.format(Company[0])] = info

    return filings



def createJSON(response,feedname):
    with open('/Users/taishanlin/Desktop/RootDirectory/DataService/OutputSamples/{}.json'.format(feedname),'w') as outfile:
        json.dump(response, outfile,indent=4)



## Executable Function ##
def fetchRSS(feedname):
    url         = RSS(feedname).getRSS(feedname)
    xml_page    = request(url)
    cikHash     = cik_map()
    data        = extractRSSData(xml_page,cikHash)
    response    = RSS(feedname).insertRSS(data)
    return      createJSON(response,feedname)


