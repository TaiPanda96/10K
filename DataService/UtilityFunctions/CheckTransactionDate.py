import sys
import os

def _processTransactionDate_utility(filing_table,search_keyword):
    """ 
    This function takes an Transaction Date and parses 'Sale' from the date.
    """
    TransactionType = []
    TransactionDate = []
    for date in filing_table['TransactionDate']:
        index_position   = _getIndex(date,search_keyword)
        transaction      = date[index_position:]
        transaction_date = date[:index_position]
        TransactionType.append(transaction)
        TransactionDate.append(transaction_date)
        
    filing_table['Sale/Purchase?']   = TransactionType
    filing_table['TransactionDate'] = TransactionDate
    return filing_table


def _getIndex(date,search_keyword):
    for word in search_keyword:
        if word in date:
            index_position = date.index(word)
            return index_position