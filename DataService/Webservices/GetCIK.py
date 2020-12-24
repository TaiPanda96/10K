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

# MODULE IMPORTS
sys.path.append('..')
from DataService.UtilityFunctions import CleanCIK

def getCIK(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response
        with open('{}.txt'.format('CIK'),'w') as outfile:
            outfile.write(data.text)
            
    else:
        print(response.status_code)


def cik_map():
    outfile = '/Users/taishanlin/Desktop/RootDirectory/DataService/UtilityFunctions/UtilityFiles/CIK.txt'
    if outfile.count != None:
        return CleanCIK._clean_cik(outfile)
    else:
        url = 'https://www.sec.gov/include/ticker.txt' 
        getCIK(url)
        return CleanCIK._clean_cik(outfile)
  
