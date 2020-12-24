# Utilities
import syslog
import sys

# Main API Modules
import Webservices
from Webservices import GetRSS
from Webservices import GetCIK
from Webservices import GetForm4

# Establish Connection to Mongo DB
import MongoConnection
from MongoConnection import connection


# Utility Functions
import UtilityFunctions
from UtilityFunctions import ParseJson
from UtilityFunctions import CheckDate

# Time Utilities
import datetime 
from datetime import datetime

# Global Variable: File Location
RSSFile = '/Users/taishanlin/Desktop/RootDirectory/DataService/OutputSamples/Filings.json'
Form4   = '/Users/taishanlin/Desktop/RootDirectory/DataService/OutputSamples/Form4.json'


def updateMongoDB(collection, updateArray, collection_to_update):
    """
    Depending on SEC Filings or SEC Form 4 collection:
    1. Pass update array into MongoDB upsert function, which performs the following:
        2. Query ticker, find the symbol
        3. Set update items to items within the update array. Each index represents a list of ticker info.
    """
    if collection_to_update == "SEC Filings":
        for items in updateArray:
            try:
                collection.update_one(
                    {'ticker': items['Ticker']},
                    {"$set" :  items}, 
                    upsert = True)
                print("Update SEC Filing Complete for"  + " "  + items['Ticker'])
            except:
                print(sys.exc_info(),syslog.openlog())


        print("Update completed")

    elif collection_to_update == "SEC Form 4":
        for items in updateArray:
            try:
                collection.update_one(
                    {'ticker': items['Symbol']},
                    {"$set" :  items}, 
                    upsert = True)
                print("Update Form 4 Complete for"  + " "  + items['Symbol'])
            except:
                print(sys.exc_info(),syslog.openlog())


        print("Update completed")

    

def updateRSS():
    """ 
    Only run this function if there ever needs to be a CIK - Ticker Mapping update to your database.
    """
    db   = connection()
    collection = db['Utradea_SIT_Main']
    try:
        mapping = GetCIK.cik_map()
        
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
      

# Executable #
def rss_job(RSSFile,db):
    """ 
    # 0: Fetch Filings JSON \n
    # 1: Establish Connection \n
    # 2: Parse the JSON, return list of dictionaries \n
    # 3: Update MongoDB, SEC Filings Collection \n
    """
    #db = connection();
    SECFilings = db['SEC Filings'];
    try: 
        GetRSS.fetchRSS('Filings')
    except:
        print(sys.exc_info(),syslog.openlog(),"error executing GetRSS.fetchRSS")
    finally:
        updateArray = ParseJson.extraction(RSSFile);
        updateMongoDB(SECFilings,updateArray,"SEC Filings")
        print("Full Update Procedure Completed For" + " " + str(datetime.now()))
        db.client.close()


# Executable #
def form4_job(Form4,db):
    """ 
    # 0: Fetch Form4 JSON \n
    # 1: Establish Connection \n
    # 2: Parse the JSON, return list of dictionaries \n
    # 3: Update MongoDB, SEC Form4 Collection \n
    """
    #db = connection();
    SEC_Form4 = db['SEC Form 4'];
    try: 
        GetForm4.fetchFormInsider('General Information','N/A',"by_latest")
    except:
        print(sys.exc_info(),syslog.openlog())
    finally:
        updateArray = ParseJson.extraction_Form4(Form4);
        updateMongoDB(SEC_Form4,updateArray,"SEC Form 4")
        print("Full Update Procedure Completed For" + " " + str(datetime.now()))
        db.client.close()


def main(RSSFile,Form4):
    db = connection()
    try:
        rss_job(RSSFile,db)
        try:
            form4_job(Form4,db)
        except:
            print("error for Form 4 job")
    except:
        print("Error for RSS job")


# Execute # 
main(RSSFile,Form4);

    