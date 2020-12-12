import pandas as pd
import json
from bs4 import BeautifulSoup, SoupStrainer
import urllib3

# Scraping Libraries Used
import os
import time, requests, lxml
from collections import OrderedDict
from bs4 import BeautifulSoup

class EdgarSearchHashMap:
    """This class is meant to parse data from SEC website and store a Hashmap of harvested data where PK = Ticker
       create method takes a list of tickers and generates a basic hashmap where key = ticker value = url """

    def __init__(self,ticker):
        self.ticker  = str(ticker) 
        self.HashMap = {}

    def request(self):
        urls = 'https://www.sec.gov/cgi-bin/browse-edgar?company=&match=&CIK={}'.format(self.ticker) + '&filenum=&State=&Country=&SIC=&owner=exclude&Find=Find+Companies&action=getcompany'
        self.HashMap[self.ticker] = urls
        return self.HashMap


    def upsert(self,data,ticker):
        """Search if a key exists"""
        if ticker in self.HashMap:
            # If the ticker exists in the Hash, then call 2 executables below to add nested data + links
            self.HashMap['ticker'] = ticker
            self.HashMap['data']  = data
            return self.HashMap
        else:
            # Else, you need to create the hash map first
            # Then call 2 executables below to add nested data + links
            self.request()
            self.HashMap['ticker'] = ticker
            self.HashMap['data']  = data
            #print(self.HashMap)
            return self.HashMap


def jsonMethod(response,ticker):
    with open('{}.json'.format(ticker),'w') as outfile:
        return json.dump(response, outfile,indent=4)


def request(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.text
        soup = BeautifulSoup(data,features='lxml')
    else:
        print(response.status_code)
    return soup


def extractData(soup,ticker,getRequest):
    edgars   = pd.read_html(getRequest[ticker])
    
    # Grab Links
    baseurl  = 'https://www.sec.gov'
    table    = soup.find_all('a', {'id':'documentsbutton'},href=True)
    docLinks = []
    for tags in table:
        docLinks.append(baseurl + tags.get('href'))

    
    query = list(filter(lambda search: 'Archives/edgar/data' in search, docLinks))
    table = pd.DataFrame(query)

    # Prepare Main Table to Join with Links Table
    df = pd.DataFrame(edgars[2])
    df = df.drop(df.index[0])

    # Left Join & Drop NaNs
    response = pd.concat([df,table],axis=1)
    response = response.dropna()
    response.columns = ['File Name', 'File Interaction', 'File Date', 'File Desc', 'File Number','File Link']
    print(response)
    return response


def fetch(ticker, method):
    """ 
    #1 Using the Edgar Search - enter a ticker '\n'
    #2 Land on the ticker Doc Repository page '\n'
    #3 Parse all the contents in the table summary '\n'
    #4 Create a DataFrame from parsed information '\n'
    #5 Send this information either in JSON format OR DataFrame Query format
    """
    getRequest  = EdgarSearchHashMap(ticker).request()
    data        = extractData(soup=request(getRequest[ticker]),ticker=ticker,getRequest=getRequest)
    
    if method == 'JSON':
        data.to_dict(orient='records')
        response = EdgarSearchHashMap(ticker).upsert(data,ticker)
        return jsonMethod(response,ticker)
    elif method == 'QUERY':
        #print(data)
        return data

