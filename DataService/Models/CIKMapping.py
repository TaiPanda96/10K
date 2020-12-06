import pymodm
import pymongo
from pymongo.read_preferences import ReadPreference
from pymodm import MongoModel, fields
import datetime
from datetime import datetime




class CIK(MongoModel):
    CIK                  = fields.CharField(primary_key=True, required=True)
    ticker               = fields.CharField(max_length=350,required=True)

    def isCIK(self):
        if self.CIK is None:
            raise fields.ValidationError("CIK cannot be null or else the API call will not be able to fetch a ticker")

    def isTicker(self):
        if self.ticker is None:
            raise fields.ValidationError("PublicationDate cannot be empty. Please check RSS feed.")

