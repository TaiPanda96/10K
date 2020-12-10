import sys
import pymongo
from pymongo import MongoClient

import CronJob.scheduledRSS as scheduledRSS



def connection():
    try: 
        client = pymongo.MongoClient("mongodb+srv://username:password@cluster0.d1abh.mongodb.net/Database?retryWrites=true&w=majority")
        db = client['Database']
        print('connection established successfully for' + ' ' +  str(db))
           
   
        return db

        
    except:
        print(sys.exc_info())


