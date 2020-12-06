import folium
import pandas as pd

filepath_address = '/Users/taishanlin/Desktop/RootDirectory/Tastethe6ix/DataSamples/Addresses.csv'
df = pd.read_csv(filepath_address)

def createGeoMap(df):
    del df['altitude']
    df = df.dropna()
    location = list(zip(df['latitude'],df['longitude']))
    for i in location:
        if i != None:
            m = folium.Map(i)


createGeoMap(df)