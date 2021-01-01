import sys
import pandas as pd
import os


search_keyword = [
        'Director',
        'President',
        'Chairman',
        'Chairman 10% Owner',
        'Director 10% Owner',
        '10% Owner',
        '5% Owner',
        'VP',
        'CAO',
        'CIO',
        'CEO',
        'CEOChairman'
        'CEO10% Owner',
        'COO',
        'CTO',
        'CFO',
        'Chief Customer Officer',
        'Chief Product Officer',
        'Chief Marketing Officer',
        'Chief Scientific Officer',
        'Chief Revenue Officer',
        'Chief People Officer',
        'Chief Medical Officer',
        'Chief Business Officer',
        'Chief Business Development Off'
        'Chief Product/Marketing',
        'General Counsel',
        'Principal Accounting Officer'
            ]


def _getIndex(values,search_keyword):
    for word in search_keyword:
        if word in values:
            index_position = values.index(word)
            return index_position

def _processInsiderNames_utility(df,search_keyword):
    Name = []
    Position = []
    for values in df['InsiderRelationship']:
       index_position = _getIndex(values,search_keyword)
       position = values[index_position:]
       name = values[:index_position]
       Position.append(position)
       Name.append(name)
    df['Position'] = Position
    df['Name'] = Name
    #print(df)
    return df


