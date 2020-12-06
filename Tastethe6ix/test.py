import pandas as pd


A = ['1','2','3','4','5','6','7','8']

B = ['A','B','C','D','E']

C = ['CA','US','EU','JJ','PP']
df = pd.DataFrame(list(zip(A,B,C)),columns=['Address','City','Province'])


df['Full Address'] = df['Address'] + ',' + df['City'] + ',' + df['Province']

print(df)