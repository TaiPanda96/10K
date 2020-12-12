import sys
import os
import pymongo
from pymongo import MongoClient

from dotenv import load_dotenv

# Global Variables
load_dotenv()

# Environment Variables
credentials = os.getenv("credentials")

def connection():
    try: 
        client = pymongo.MongoClient(credentials)
        db = client['Database']
        print('connection established successfully for' + ' ' +  str(db))
           
        return db

        
    except:
        print(sys.exc_info())


