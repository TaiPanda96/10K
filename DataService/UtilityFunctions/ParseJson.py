# Utilities
import sys
import os

import syslog
import sys
import json

# Time Utilities
import datetime 
from datetime import datetime


def extraction(RSSFile):
    updateTickers = []
    with open(RSSFile) as rss:
        data = json.load(rss)

    info = json.dumps(data)
    jsondict = json.loads(info)

    for items in data:
        company = data['{}'.format(items)]
        for information in company:
            updateTickers.append(information)

    def getNested(jsondict,updateTickers):
        """     # i = Company \n
                # i + 1 = Links \n
                # i + 2 = Document \n
                # i + 3 = Filing Date \n
                # i + 4 = Company Operating Name \n
                # i + 5 = CIK Number \n
                # i + 6 = Publication Date \n
        """
        i = 0
        updateArray = []
        for i in range(len(jsondict)):
            for ticker in updateTickers:
                data = {
                    'Ticker'                 : ticker,
                    'Company'                : jsondict['data']['{}'.format(ticker)][i],
                    'Links'                  : jsondict['data']['{}'.format(ticker)][i + 1],
                    'Document'               : jsondict['data']['{}'.format(ticker)][i + 2],
                    'Filing Date'            : jsondict['data']['{}'.format(ticker)][i + 3],
                    'Company Operating Name' : jsondict['data']['{}'.format(ticker)][i + 4],
                    'CIK Number'             : jsondict['data']['{}'.format(ticker)][i + 5],
                    'Publication Date'       : jsondict['data']['{}'.format(ticker)][i + 6],
                }

                updateArray.append(data)
        return updateArray

    return getNested(jsondict,updateTickers)



def extraction_Form4(Form4):
    updateArray = []

    with open(Form4) as form4:
        data = json.load(form4)

    
    info     = json.dumps(data)
    jsondict = json.loads(info)

    
    for items in jsondict['data']:
        updateArray.append(items)
    
    return updateArray


# if __name__ == "__main__":
# Unit Testing Only
# Form4   = '/Users/taishanlin/Desktop/RootDirectory/DataService/OutputSamples/Form4.json'
#     RSSFile = '/Users/taishanlin/Desktop/RootDirectory/DataService/OutputSamples/Filings.json'
#     extraction_RSS(RSSFile)