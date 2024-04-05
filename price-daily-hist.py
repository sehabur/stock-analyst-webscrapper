from bdshare import *
import pymongo, datetime, certifi
from variables import mongo_string
import requests
from bs4 import BeautifulSoup
import pandas as pd

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient["stockanalyst"]

def get_hist_data(start=None, end=None, code='All Instrument'):
    """
        get historical stock price.
        :param start: str, Start date e.g.: '2020-03-01'
        :param end: str, End date e.g.: '2020-03-02'
        :param code: str, Instrument symbol e.g.: 'ACI'
        :return: dataframe
    """
    # data to be sent to post request
    data = {'startDate': start,
            'endDate': end,
            'inst': code,
            'archive': 'data'}
    # try:
    #     r = requests.get(url=vs.DSE_URL+vs.DSE_DEA_URL, params=data)
    #     if r.status_code != 200:
    #         r = requests.get(url=vs.DSE_ALT_URL+vs.DSE_DEA_URL, params=data)
    # except Exception as e:
    #         print(e)

    r = requests.get("https://www.dsebd.org/day_end_archive.php", params=data)

    soup = BeautifulSoup(r.text, 'html.parser')
    # soup = BeautifulSoup(r.content, 'html5lib')

    quotes = []  # a list to store quotes

    table = soup.find('table', attrs={
                      'class': 'table table-bordered background-white shares-table fixedHeader'})
    
    print(table)
    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        quotes.append({'date': cols[1].text.strip().replace(",", ""),
                       'symbol': cols[2].text.strip().replace(",", ""),
                       'ltp': cols[3].text.strip().replace(",", ""),
                       'high': cols[4].text.strip().replace(",", ""),
                       'low': cols[5].text.strip().replace(",", ""),
                       'open': cols[6].text.strip().replace(",", ""),
                       'close': cols[7].text.strip().replace(",", ""),
                       'ycp': cols[8].text.strip().replace(",", ""),
                       'trade': cols[9].text.strip().replace(",", ""),
                       'value': cols[10].text.strip().replace(",", ""),
                       'volume': cols[11].text.strip().replace(",", "")
                       })
    df = pd.DataFrame(quotes)
    if 'date' in df.columns:
        df = df.set_index('date')
        df = df.sort_index(ascending=False)
    else:
        print('No data found')
    return df
 
def insert_data(df): 
  share_data_array = []

  for x in range(df.shape[0]): 
    
    if (float(df.iloc[x]['ycp']) == 0 or float(df.iloc[x]['ltp']) == 0):
      change = 0
      percent_change = 0
    else:
      change = round(float(df.iloc[x]['ltp']) - float(df.iloc[x]['ycp']), 2)
      percent_change = round((float(df.iloc[x]['ltp'])-float(df.iloc[x]['ycp']))/float(df.iloc[x]['ycp'])*100, 2)

    share_data_array.append({
      'date': datetime.datetime.strptime(df.index[x] , '%Y-%m-%d'),
      'tradingCode': df.iloc[x]['symbol'],
      'ltp': (float(df.iloc[x]['ltp'])),
      'high': (float(df.iloc[x]['high'])),
      'low': (float(df.iloc[x]['low'])),
      'open': (float(df.iloc[x]['open'])),
      'close': (float(df.iloc[x]['close'])),
      'ycp': (float(df.iloc[x]['ycp'])),
      'change': change,
      'percentChange': percent_change,
      'trade': (float(df.iloc[x]['trade'])),
      'value': (float(df.iloc[x]['value'])),
      'volume': (float(df.iloc[x]['volume'])),
    })

  mydb.daily_prices_new.insert_many(share_data_array)

for x in range(1, 2):
  print(f'2022-{x}-01', " : start")
  df = get_hist_data(f'2022-{x}-01', f'2022-{x}-31',)
  # print(df)
  insert_data(df)
  print(f'2022-{x}-01', " : complete")


  