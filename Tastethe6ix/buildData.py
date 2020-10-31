import pandas as pd 
import geopandas as gp 
import geopy 
import concurrent.futures

from geopy import Nominatim
from geopy.extra.rate_limiter import RateLimiter

filepath_bar = '/Users/taishanlin/Desktop/RootDirectory/Tastethe6ix/DataSamples/Heated Patios by Tastethesix - Heated Patios TO.csv'
filepath_TO  = '/Users/taishanlin/Desktop/RootDirectory/Tastethe6ix/DataSamples/Toronto.csv'

files = [filepath_bar, filepath_TO]

def filecsv(files):
    bars    = pd.read_csv(files[0])
    toronto = pd.read_csv(files[1])

    # What needs to happen is 
    bars['City']         = 'Toronto'
    bars['Province']     = 'Ontario'
    bars['Country']      = 'Canada'
    bars['Full Address'] = bars['Address'] + ',' + bars['City'] + ',' + bars['Province'] + ',' + bars['Country']

    bars  = bars.drop(['Restaurant','Covered','Reservations'],axis=1)
    print(bars, '\n', toronto)
    return bars, toronto


def paralellencode(bars,toronto):
    locator  = Nominatim(user_agent="http")
    location = RateLimiter(locator.geocode, min_delay_seconds=1)
    with concurrent.futures.ThreadPoolExecutor() as e:
        locations = pd.DataFrame(e.map(location,bars['Full Address'].tolist()),columns=['Coordinates'])
    locations['Point'] = locations['Coordinates'].apply(lambda loc: tuple(loc.point) if loc else None)
    locations[['latitude', 'longitude']] = pd.DataFrame(locations['Point'].tolist(), index=locations.index)
    print(locations)
    return locations


def encode(bars, toronto):
    locator  = Nominatim(user_agent="http")
    location = RateLimiter(locator.geocode, min_delay_seconds=1)
    bars['Coordinates'] = bars['Full Address'].apply(location)
    # 3 - create longitude, latitude and altitude from location column (returns tuple)
    bars['Point']       = bars['Coordinates'].apply(lambda loc: tuple(loc.point) if loc else None)
    # 4 - split point column into latitude, longitude and altitude columns
    bars[['latitude', 'longitude', 'altitude']] = pd.DataFrame(bars['Point'].tolist(), index=bars.index)
    result = bars.to_csv('/Users/taishanlin/Desktop/RootDirectory/Tastethe6ix/DataSamples/Addresses.csv')
    print(bars)
    return bars

bars, toronto = filecsv(files)
encode(bars,toronto);

