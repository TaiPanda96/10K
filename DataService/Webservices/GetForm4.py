# CORE IMPORTS
import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer
import urllib3
import lxml
from lxml import html
import requests

# OTHER IMPORT DEPENDENCIES
import os
import time, lxml
import string 
import re
import sys
import datetime
import json

print("root = ", sys.path[0], sys.path[1], sys.path[2])

# Adds higher directory to python modules path.
sys.path.append("..") 


# Module Imports 
from UtilityFunctions import CheckInsiderNames
from UtilityFunctions import CheckTransactionDate
from UtilityFunctions.UtilityFiles import tickers

#Unit Test Modules

class FormInsider:
    def __init__(self,ticker,cik):
        self.ticker = ticker
        self.cik    = cik 
        self.map    = dict()
        self.url    = None

    def createRequestURL(self,method):
        if  method == "by_ticker":
            self.url = "https://www.secform4.com/insider-trading/{}.htm".format(self.cik)
            return self.url

        elif method == "by_latest":
            self.url = "https://www.secform4.com/sec-filings.htm"
            return self.url

        else: 
            raise ValueError("the method argument is inaccurate, please try again")


    def createDataStructure(self,data, url, method):
        if method == "by_ticker":
            self.url = url
            self.map['ticker'] = self.ticker
            self.map['CIK']    = self.cik
            self.map['form4_url'] = url
            self.map['requestedDate'] = str(datetime.datetime.now())
            self.map['data'] = data

            #print(self.map)
            return self.map

        elif method == "by_latest":
            self.url = url
            self.map['ticker'] = "General Data Pull"
            self.map['CIK']    = "N/A"
            self.map['form4_url'] = url
            self.map['requestedDate'] = str(datetime.datetime.now())
            self.map['data'] = data

            #print(self.map)
            return self.map


def request(form4_url,method):
    response = requests.get(form4_url)

    if method == "Soup":
        if response.status_code == 200:
            data = response.text
            soup = BeautifulSoup(data,features='lxml')
            return soup
        else:
            print(response.status_code)

    elif method == "Xpath":
        if response.status_code == 200:
            tree = html.fromstring(response.content)
            # Using XPATH, fetch all table elements on the page
            return tree
        else:
            print(response.status_code)


def extract(page_content):
    table = page_content.xpath('//*[@id="filing_table"]')
    keywords = CheckInsiderNames.search_keyword
    try: 
        tstring = lxml.etree.tostring(table[0], method='html')

        df = pd.read_html(tstring)[0]
        df = df.dropna()
        try:
            table = CheckTransactionDate._processTransactionDate_utility(df,search_keyword=['Sale','Purchase'])
            table = CheckInsiderNames._processInsiderNames_utility(df,search_keyword=keywords)
            data  = table.to_dict(orient='records')
            return data
        except:
            print(sys.exc_info(),'\n',"unable to identify sale or purchase in the table. Please check your date function")

    except:
        print(sys.exc_info())


def createJSON(response,ticker,cik,method):
    if method == "by_ticker":
        with open('/Users/taishanlin/Desktop/RootDirectory/DataService/OutputSamples/{}_{}_form4.json'.format(ticker,cik),'w') as outfile:
            json.dump(response, outfile,indent=4)


    elif method == "by_latest":
        with open('/Users/taishanlin/Desktop/RootDirectory/DataService/OutputSamples/Form4.json','w') as outfile:
            json.dump(response, outfile,indent=4)



def fetchFormInsider(ticker,cik, method, output_to):
    form4_url          = FormInsider(ticker,cik).createRequestURL(method=method)
    page               = request(form4_url,'Xpath')
    content            = extract(page)
    responseMap        = FormInsider(ticker,cik).createDataStructure(data=content,url=form4_url,method=method)
    
    if output_to == "json":
        return createJSON(responseMap,ticker,cik,method=method)
    else: 
        return responseMap

