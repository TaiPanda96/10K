# Utilities
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
                #print(data)
                updateArray.append(data)
                #print(updateTickers)
        return updateArray

                #print(jsondict['data']['{}'.format(ticker)][i])

    return getNested(jsondict,updateTickers)