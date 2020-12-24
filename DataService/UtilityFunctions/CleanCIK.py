def _clean_cik(outfile):
    """ 
    Private function to clean cik file \n
    1) Clean the text file by stripping empty spaces and splitting CIK # to Ticker Mapping as seperate elements \n
    2) Using dictionary comprehension return a CIK Hash Map where the key = CIK # and value = ticker. \n
    """
    with open(outfile) as fp:
        #count = 0
        data = []

        for line in fp:
            cik_ = line.strip('\n')
            cik_ = cik_.upper()
            cik_ = cik_.split('\t')
            elements = cik_
            data.append(elements)
    CIK = {element[1]: element[0] for element in data}
    return CIK