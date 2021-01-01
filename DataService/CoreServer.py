import os
import flask
import pymongo
import sys
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Main API Modules
import Webservices
from Webservices import GetForm4
from Webservices import GetRSS
from Webservices import GetCIK
from Webservices import GetCompanySummaryPage

from MongoConnection import connection


@app.route('/api/dataservice/form4/', methods=['GET'])
def api_form4_by_ticker():
    tickerMap = GetCIK.cik_map()
    ticker = request.args['ticker']
    for cik_key,ticker_value in tickerMap.items():
        if ticker == ticker_value:
            response = GetForm4.fetchFormInsider(ticker=ticker,cik=cik_key,method="by_ticker",output_to="response")
            return jsonify(response)
        else:
            Exception(sys.exc_info())


@app.route('/api/dataservice/filings/', methods=['GET'])
def api_getall_by_ticker():
    tickerMap = GetCIK.cik_map()
    ticker = request.args['ticker']
    for cik_key,ticker_value in tickerMap.items():
        if ticker == ticker_value:
            response = GetCompanySummaryPage.fetch(ticker=ticker,method="API")
            return jsonify(response)
        else:
            Exception(sys.exc_info())
       
app.run()
