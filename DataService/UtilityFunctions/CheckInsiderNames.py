import sys
import os

def _processInsiderNames(df):
    Name = []
    Position = []
    for insiders in df['InsiderRelationship']:
        if "Director" in insiders:
            position = insiders[-8:]
            name = insiders.split(position)
            #print(position,'\n',name[0])

        elif "President" in insiders:
            position = insiders[-9:]
            name = insiders.split(position)
            #print(position,'\n',name[0])

        elif "Chairman" in insiders:
            position = insiders[-8:]
            name = insiders.split(position)
            #print(position,'\n',name[0])
        
        elif "Chairman '\n' 10% Owner" in insiders:
            position = insiders[-18:]
            name = insiders.split(position)
            #print(position,'\n',name[0])

        elif "Director '\n' 10% Owner" in insiders:
            position = insiders[-19:]
            name = insiders.split(position)
            #print(position,'\n',name[0])

        elif "10% Owner" in insiders:
            position = insiders[-9:]
            name = insiders.split(position)
            #print(position,'\n',name[0])

        elif "5% Owner" in insiders:
            position = insiders[-8:]
            name = insiders.split(position)
            #print(position,'\n',name[0])

        elif "VP" in insiders:
            position = insiders[-2:]
            name = insiders.split(position)
            #print(position,'\n',name[0])

        elif "CAO" in insiders:
            position = insiders[-3:]
            name = insiders.split(position)
            #print(position,'\n',name[0])

        elif "CEO" in insiders:
            position = insiders[-3:]
            name = insiders.split(position)
            #print(position,'\n',name[0])

        elif "CTO" in insiders:
            position = insiders[-3:]
            name = insiders.split(position)
            #print(position,'\n',name[0])

        elif "CFO" in insiders:
            position = insiders[-3:]
            name = insiders.split(position)
            #print(position,'\n',name[0])

        elif "COO" in insiders:
            position = insiders[-3:]
            name = insiders.split(position)
            #print(position,'\n',name[0])

        elif "Chief Customer Officer" in insiders:
            position = insiders[-14:]
            name = insiders.split(position)
            #print(position,'\n',name[0])

        elif "Chief Medical Officer" in insiders:
            position = insiders[-21:]
            name = insiders.split(position)
            #print(position,'\n',name[0])

        elif "General Counsel" in insiders:
            position = insiders[-15:]
            name = insiders.split(position)
            #print(position,'\n',name[0])

        elif "Principal Accounting Officer" in insiders:
            position = insiders[-28:]
            name = insiders.split(position)
            #print(position,'\n',name[0])
    
        Name.append(name)
        Position.append(position)
    df['Name'] = Name
    df['Position'] = Position
    return df