import requests
import sys
import pymongo
import os
import json

from dotenv import load_dotenv

# Global Variables
load_dotenv()

# Environment Variables
credentials      = os.getenv("credentials")
API_DEV_ENDPOINT = os.getenv("API_DEV_ENDPOINT")


def add_ticker_form4(ticker_to_post):
    url = API_DEV_ENDPOINT + ticker_to_post
    client = pymongo.MongoClient(credentials)
    db = client['Database']
    Watchlist = db['Watch List']
    try:
        data = requests.get(url)
        data_insert = data.text
        try:
            response = json.loads(data_insert)
            try:
                Watchlist.update_one({"ticker": response['ticker']},{"$set":response},upsert=True)
            except:
                raise Exception("Unable to update MongoDB for --> {}".format(ticker_to_post))

        except:
            raise Exception("converting json to dictionary failed.")

    except:
        raise Exception(sys.exc_info())

    finally:
        print("Form 4 Insiders Saved for --> {}".format(ticker_to_post))

add_ticker_form4("UBER");