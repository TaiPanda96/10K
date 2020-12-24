import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Main API Modules
import Webservices
from Webservices import GetForm4

# Unit 1: Testing Block
data = {
    'cik' : "1318605",
    'ticker' : 'TSLA'
}

@app.route('/api/v1/resources/form4/all', methods=['GET'])
def api_all():
    response = GetForm4.fetchFormInsider(ticker=data['ticker'],cik=data['cik'],method="by_latest")
    return jsonify(response)


@app.route('/api/v1/resources/form4/{}'.format(data['ticker']), methods=['GET'])
def api_by_ticker():
    response = GetForm4.fetchFormInsider(ticker=data['ticker'],cik=data['cik'],method="by_ticker")
    return jsonify(response)



app.run()