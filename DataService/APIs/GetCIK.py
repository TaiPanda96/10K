# CORE IMPORTS
import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer
import urllib3
import json


# OTHER IMPORT DEPENDENCIES
import os
import time, requests, lxml
import string 
import re
import sys
import datetime
import json




def getCIK(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response
        with open('{}.txt'.format('CIK'),'w') as outfile:
            outfile.write(data.text)
            
    else:
        print(response.status_code)


def _clean_cik(outfile):
    """ 
    Private function to clean cik file \n
    1) Clean the text file by stripping empty spaces and splitting CIK # to Ticker Mapping as seperate elements \n
    2) Using dictionary comprehension return a CIK Hash Map. \n
    """
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

    
def cik_map():
    outfile = '/Users/taishanlin/Desktop/RootDirectory/DataService/UtilityFunctions/UtilityFiles/CIK.txt'
    if outfile.count != None:
        return _clean_cik(outfile)
    else:
        url = 'https://www.sec.gov/include/ticker.txt' 
        getCIK(url)
        return _clean_cik(outfile)
  
cik_map();
