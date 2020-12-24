date = "MyExample2020 Sales"
search_keyword = ["Sales","Purchase"]

def _processTransactionDate_utility(df,search_keyword):
    """ 
    This function takes an InsiderRelationship string and parses the part of a larger string that has sale
    """
    TransactionType = []
    

    for date in df['TransactionDate']:
        if search_keyword in date:
            index_position = _getIndex(date,search_keyword)
            transaction = date[index_position:]

        TransactionType.append(transaction)
        
    df['Sale/Purchase?'] = TransactionType
    return df


def _getIndex(date,search_keyword):
    for word in search_keyword:
        if word in date:
            index_position = date.index(word)
            #print(index_position)
            return index_position

