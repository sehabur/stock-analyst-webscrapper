from pytz import timezone
import pandas as pd
import requests, datetime, pymongo, certifi
from bs4 import BeautifulSoup
from variables import mongo_string

def get_current_trade_data(symbol=None, retry_count=1, pause=0.001):
    """
        get last stock price.
        :param symbol: str, Instrument symbol e.g.: 'ACI' or 'aci'
        :return: dataframecd 
    """
    for _ in range(retry_count):
        try:
            r = requests.get("https://www.dsebd.org/latest_share_price_scroll_l.php")
            # if r.status_code != 200:
            #     r = requests.get("https://dsebd.com.bd/latest_share_price_scroll_l.php")
        except Exception as e:
            print(e)
        else:
            soup = BeautifulSoup(r.content, 'html.parser')
            quotes = []  # a list to store quotes
            table = soup.find('table', attrs={
                                'class': 'table table-bordered background-white shares-table fixedHeader'})

            # print(table)
            for row in table.find_all('tr')[1:]:
                cols = row.find_all('td')
                quotes.append({'symbol': cols[1].text.strip().replace(",", ""),
                       'ltp': cols[2].text.strip().replace(",", ""),
                       'high': cols[3].text.strip().replace(",", ""),
                       'low': cols[4].text.strip().replace(",", ""),
                       'close': cols[5].text.strip().replace(",", ""),
                       'ycp': cols[6].text.strip().replace(",", ""),
                       'change': cols[7].text.strip().replace("--", "0"),
                       'trade': cols[8].text.strip().replace(",", ""),
                       'value': cols[9].text.strip().replace(",", ""),
                       'volume': cols[10].text.strip().replace(",", "")
                       })
            df = pd.DataFrame(quotes)
            if symbol:
                df = df.loc[df.symbol == symbol.upper()]
                return df
            else:
                return df

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient["stockanalyst"]

data_setting = mydb.settings.find_one()

if data_setting['dataInsertionEnable'] == 0:
    print('exiting script')
    exit()

df = get_current_trade_data()

share_data_array = []

for x in range(df.shape[0]):

  if (float(df.iloc[x]['ycp']) == 0 or float(df.iloc[x]['ltp']) == 0):
    percent_change = 0
  else:
    percent_change = round((float(df.loc[x]['ltp'])-float(df.loc[x]['ycp']))/ float(df.loc[x]['ycp']) *100 , 2)
      
  share_data_array.append({
    'date': datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0), 
    'time': datetime.datetime.now(timezone('Asia/Dhaka')).replace(second=0, microsecond=0), 
    'tradingCode': df.loc[x]['symbol'],
    'ltp': (float(df.loc[x]['ltp'])),
    'high': (float(df.loc[x]['high'])),
    'low': (float(df.loc[x]['low'])),
    'close': (float(df.loc[x]['close'])),
    'ycp': (float(df.loc[x]['ycp'])),
    'change': (float(df.loc[x]['change'])),
    'percentChange': percent_change,
    'trade': (float(df.loc[x]['trade'])),
    'value': (float(df.loc[x]['value'])),
    'volume': (float(df.loc[x]['volume'])),
  })

# print(share_data_array)
# exit()  

mydb.latest_prices.delete_many({})

mydb.latest_prices.insert_many(share_data_array)

mydb.day_minute_prices.insert_many(share_data_array)

mydb.minute_prices.insert_many(share_data_array)

myclient.close()
