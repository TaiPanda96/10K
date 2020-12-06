# Main API Modules
import APIs
from APIs import GetRSS
from APIs import GetCIK

# import Models
# from Models import RSS
# from Models import CIKMapping

# Establish Connection to Mongo DB
import MongoConnection
from MongoConnection import connection

# Utility Functions
import UtilityFunctions
from UtilityFunctions import ParseJson
from UtilityFunctions import CheckDate

# Utilities
import syslog
import sys
import json

# Time Utilities
import datetime 
from datetime import datetime

# File Location
RSSFile = '/Users/taishanlin/Desktop/RootDirectory/DataService/RSS.json'

def updateSECFilings(SECFilings, updateArray):
    for items in updateArray:
        try:
            SECFilings.update_one(
                {'ticker': items['Ticker']},
                {"$set" :  items}, 
                upsert = True)
            print("Update completed for"  + " "  + items['Ticker'])
        except:
            print(sys.exc_info(),syslog.openlog())


    print("Update completed")
    

def updateRSS():
    db   = connection()
    collection = db['Utradea_SIT_Main']
    try:
        mapping = GetCIK.produceCIKHash()
        
        for key,value in mapping.items():
            data = {
                    'cik' : key,
                    'ticker' : value,
                    'dateloaded' : datetime.now()
                    }
            collection.update_one({'cik': key },{"$set":data},upsert=True)

    except:
        print(sys.exc_info(), syslog.openlog())

    finally:
        print("data initiation completed")
      

def updateSEC_test(SECFilings):
    try:
        test = {
            'ticker' : 'GOOGL',
            'value'  : 1225,
            'date'   : datetime.now() 
        }
        
        SECFilings.update_one(
             {'ticker':'GOOGL'},
             {"$set" : test}, 
              upsert= True)
    except:
        print(sys.exc_info(), syslog.openlog())

    finally:
        print("data initiation completed")


def createCollection(db):
    if db['SEC Filings'].estimated_document_count() > 0:
        updateSEC_test(db['SEC Filings'])

        print('collection' + ' ' + str(db['SEC Filings']) + ' ' + 'has been updated')
    else:
        print(db['SEC Filings'].estimated_document_count())
        SECFilings   = db['SEC Filings']
        updateSEC_test(SECFilings)
        

def BaseTables(method):
    db = connection()
    if method == 'Mapping & SEC Tables':
        createCollection(db=db)
        # Run this only when you've deleted the collection
        updateRSS()
    else:
        createCollection(db=db)


def UpdateTables(db,updateArray):
    SECFilings = db['SEC Filings']
    for items in updateArray:
        return updateSECFilings(SECFilings,items)

#################################################### Executable ###################################################################
def main():
    """ 
    # 0: Fetch RSS JSON \n
    # 1: Establish Connection \n
    # 2: Parse the JSON, return list of dictionaries \n
    # 3: Update MongoDB, SEC Filings Collection \n
    """
    db = connection();
    SECFilings = db['SEC Filings'];
    try: 
        GetRSS.fetchRSS('RSS')
    except:
        print(sys.exc_info(),syslog.openlog())
    finally:
        updateArray = ParseJson.extraction(RSSFile);
        updateSECFilings(SECFilings,updateArray)
        print("Full Update Procedure Completed")


main();