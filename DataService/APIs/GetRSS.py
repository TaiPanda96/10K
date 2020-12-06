import pandas as pd
import sys
import datetime
import json
from bs4 import BeautifulSoup, SoupStrainer
import urllib3

# Scraping Libraries Used
import os
import time, requests, lxml
import string 
import re

import xml.etree.ElementTree as ET
from collections import OrderedDict
from bs4 import BeautifulSoup


# CIK Hashmap
#from GetCIK import produceCIKHash
from .GetCIK import produceCIKHash

class RSSHashMap:
    """This class is meant to parse data from SEC website and store a Hashmap of harvested data where PK = Ticker
       create method takes a list of tickers and generates a basic hashmap where key = ticker value = url """

    def __init__(self,ticker):
        self.ticker  = str(ticker) 
        self.HashMap = {}

    def request(self):
        urls  = 'https://www.sec.gov/cgi-bin/browse-edgar?company=&match=&CIK={}'.format(self.ticker) + '&filenum=&State=&Country=&SIC=&owner=exclude&Find=Find+Companies&action=getcompany'
        return urls

    
    def getRSS(self,key):
        Filings               = 'https://www.sec.gov/Archives/edgar/usgaap.rss.xml'
        MutualFundFilings     = 'https://www.sec.gov/Archives/edgar/xbrl-rr.rss.xml'
        FinancialStatements   = 'https://www.sec.gov/Archives/edgar/xbrl-inline.rss.xml'
        self.HashMap[self.ticker] = self.request()
        self.HashMap['Filings']             = Filings
        self.HashMap['MutualFundFilings']   = MutualFundFilings
        self.HashMap['FinancialStatements'] = Filings
        print(self.HashMap)
        return self.HashMap[key]

    
    def upsertRSS(self,data):
        self.request()
        self.HashMap['data']  = data
        #print(self.HashMap)
        return self.HashMap


def jsonMethod(response,feedname):
    with open('{}.json'.format(feedname),'w') as outfile:
        json.dump(response, outfile,indent=4)

 


def request(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.text
        soup = BeautifulSoup(data,features='lxml')
        #print(soup)
    else:
        print(response.status_code)
    return soup



def getNested(json):
    for keys in json:
        for attribute,value in keys.items():
            print(attribute,value)



# This function grabs the JSON value after it has been generated.
def getDocumentLink(link):
    try:
        page = requests.get(link)
        html = page.text
        soup = BeautifulSoup(html, 'html.parser')

        table  = soup.find('table',{'class':'tableFile'})
        base   = 'https://www.sec.gov'
        DocLink = []

        for rows in table.findAll('a', href=True):
            if rows:
                links = base + rows.get('href')
                DocLink.append(links)
                #print(DocLink[0])
                return DocLink[0]
    except:
        print(sys.exc_info())

def extractRSSData(soup,cikHash):
    table    = soup.find_all('item')
    Items    = []
    RSS      = {}
    

    for items in table:
        
        data     = items.text
        elements = data.split('\n')
        result   = list(filter(lambda x: x != '',elements))
        
        Items.append(result)

      
        Company            = { 'Company'  : data[0] for data in Items }
        # There is a function call in 'Links' which is ANOTHER URL request to fetch the actual document link in human viewable format.
        Links              = { 'Links'    : [ data[1], data[2]] for data in Items }
        Document           = { 'Document' : data[3] for data in Items }
        FilingDate         = { 'FilingDate'  : data[4] for data in Items }
        OperatingName      = { 'Company Operating Name'  : data[5] for data in Items }
        CIK                = { 'CIK'  : data[8].lstrip('0') for data in Items }
        PublicationDate    = { 'Publication Date'  : data[7] for data in Items }
        AssistantDirector  = { 'Assistant Director'  : data[13] for data in Items }
        #SIC                = { 'SIC'  : data[14] for data in Items }

        info = [
            Company,
            Links,
            Document,
            FilingDate,
            OperatingName,
            CIK,
            PublicationDate,
            AssistantDirector,
            #SIC
        ]

        ## If the lookup value matches the CIK hash map key, return the CIK hash map value (which is the ticker)
        
        ## Add the ticker to the JSON.
        element = [item for item in info[0].values()]
        CIK_search = [item for item in info[5].values()]

        if CIK_search[0] in cikHash:
            ticker = cikHash['{}'.format(CIK_search[0])]

            RSS['{}'.format(ticker)] = info
        else:
            RSS['{}'.format(element[0])] = info

    return RSS


def fetchRSS(feedname):
    url         = RSSHashMap(feedname).getRSS('Filings')
    xml_page    = request(url)
    cikHash     = produceCIKHash()
    data        = extractRSSData(xml_page,cikHash)
    response    = RSSHashMap(feedname).upsertRSS(data)
    return jsonMethod(response,feedname)

    

fetchRSS('RSS');


