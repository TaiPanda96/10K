import pymodm
import pymongo
from pymongo.read_preferences import ReadPreference
from pymodm import MongoModel, fields
import datetime
from datetime import datetime


    #     'Ticker': ticker,
    #     'Company' : i,
    #     'Links' : i+1,
    #     'Document' : i+2,
    #     'Filing Date' : i+3,
    #     'Company Operating Name' : i+4,
    #     'CIK Number' : i+5,
    #     'Publication Date' : i+6,

class SEC(MongoModel):
    Ticker               = fields.CharField(primary_key=True, required=True)
    Company              = fields.CharField(max_length=350, required=True)
    Links                = fields.CharField(required=True)
    DocumentDesc         = fields.CharField(max_length=350,required=True)
    FilingDate           = fields.DateTimeField(required=True)
    CompanyOperatingName = fields.CharField(max_length=350, required=True)
    CIK                  = fields.IntegerField(required=True,blank=False)
    PublicationDate      = fields.DateTimeField(required=True)
    
    def isCIK(self):
        if self.CIK is None:
            raise fields.ValidationError("CIK cannot be null or else the API call will not be able to fetch a ticker")

    def isPublicationDate(self):
        if self.PublicationDate is None:
            raise fields.ValidationError("PublicationDate cannot be empty. Please check RSS feed.")

