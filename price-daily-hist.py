from bdshare import *
import pymongo, datetime, certifi
from variables import mongo_string

df = get_hist_data('2023-10-19','2023-10-31')
  
share_data_array = []

for x in range(df.shape[0]): 
  # print(datetime.datetime.strptime(df.index[x] , '%Y-%m-%d')) 
  share_data_array.append({
    'date': datetime.datetime.strptime(df.index[x] , '%Y-%m-%d'),
    'tradingCode': df.iloc[x]['symbol'],
    'ltp': (float(df.iloc[x]['ltp'])),
    'high': (float(df.iloc[x]['high'])),
    'low': (float(df.iloc[x]['low'])),
    'close': (float(df.iloc[x]['close'])),
    'ycp': (float(df.iloc[x]['ycp'])),
    'change': round((float(df.iloc[x]['ltp'])) - (float(df.iloc[x]['ycp'])), 2),
    'percentChange': 0 if float(df.iloc[x]['ycp']) == 0 else round((float(df.iloc[x]['ltp'])-float(df.iloc[x]['ycp']))/float(df.iloc[x]['ycp'])*100, 2),
    'trade': (float(df.iloc[x]['trade'])),
    'value': (float(df.iloc[x]['value'])),
    'volume': (float(df.iloc[x]['volume'])),
  })

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient["stockanalyst"]
mycol = mydb["daily_prices"]
# mycol = mydb["dps"]
mycol.insert_many(share_data_array)

