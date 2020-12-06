import pandas as pd 
import pandas as pd
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


def getCIK(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response
        with open('{}.txt'.format('CIK'),'w') as outfile:
            outfile.write(data.text)
            
    else:
        print(response.status_code)


def cikHashMap(outfile):
    with open(outfile) as fp:
        #count = 0
        data = []

        for line in fp:
            cik_ = line.strip('\n')
            cik_ = cik_.upper()
            cik_ = cik_.split('\t')
            elements = cik_
            data.append(elements)
    CIK = {element[1]: element[0] for element in data}
    return CIK

    
def produceCIKHash():
    outfile = '/Users/taishanlin/Desktop/RootDirectory/DataService/UtilityFunctions/UtilityFiles/CIK.txt'
    if outfile.count != None:
        return cikHashMap(outfile)
    else:
        url = 'https://www.sec.gov/include/ticker.txt' 
        getCIK(url)
        return cikHashMap(outfile)
  
produceCIKHash();
