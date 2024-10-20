import pymongo, datetime, certifi
from variables import mongo_string
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_daily_data(start=None, end=None, code='All Instrument'):
    """
        get historical stock price.
        :param start: str, Start date e.g.: '2020-03-01'
        :param end: str, End date e.g.: '2020-03-02'
        :param code: str, Instrument symbol e.g.: 'ACI'
        :return: dataframe
    """
    data = {'startDate': start,
            'endDate': end,
            'inst': code,
            'archive': 'data'}
    # try:
    #     r = requests.get(url=vs.DSE_URL+vs.DSE_DEA_URL, params = data)
    #     if r.status_code != 200:
    #         r = requests.get(url=vs.DSE_ALT_URL+vs.DSE_DEA_URL, params = data)
    # except Exception as e:
    #         print(e)

    r = requests.get("https://www.dsebd.org/day_end_archive.php", params=data)

    soup = BeautifulSoup(r.text, 'html.parser')
    # soup = BeautifulSoup(r.content, 'html5lib')

    quotes = []

    table = soup.find('table', attrs={
                      'class': 'table table-bordered background-white shares-table fixedHeader'})
    
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

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient["stockanalyst"]

data_setting = mydb.settings.find_one()

if data_setting['dataInsertionEnable'] == 0:
    print('exiting script')
    exit()

# today_date = datetime.datetime(2024, 7, 16, 0, 0)  // debug purpose //
today_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

formatted_date = today_date.strftime("%Y-%m-%d")

df = get_daily_data(formatted_date, formatted_date)
 
share_data_array = []

for x in range(df.shape[0]): 

  ycp = float(df.iloc[x]['ycp'])
  open = float(df.iloc[x]['open']) if float(df.iloc[x]['open']) != 0 else ycp
  low = float(df.iloc[x]['low']) if float(df.iloc[x]['low']) != 0 else ycp
  high = float(df.iloc[x]['high']) if float(df.iloc[x]['high']) != 0 else ycp
  ltp = float(df.iloc[x]['ltp']) if float(df.iloc[x]['ltp']) != 0 else ycp

  if float(df.iloc[x]['close']) != 0:
    close = float(df.iloc[x]['close'])
  elif float(df.iloc[x]['ltp']) != 0:
    close = float(df.iloc[x]['ltp'])
  else:
    close = ycp

  if ycp == 0:
    change = 0
    percent_change = 0
  else:
    change = round(close - ycp, 2)
    percent_change = round((close - ycp) / ycp * 100 , 2)

  share_data_array.append({
    'date': datetime.datetime.strptime(df.index[x] , '%Y-%m-%d'),
    'tradingCode': df.iloc[x]['symbol'],
    'ltp': ltp,
    'high': high,
    'low': low,
    'open': open,
    'close': close,
    'ycp': ycp,
    'change': change,
    'percentChange': percent_change,
    'trade': float(df.iloc[x]['trade']),
    'value': float(df.iloc[x]['value']),
    'volume': float(df.iloc[x]['volume']),
  })

index_value = mydb.index_daily_values.find_one({ 'date': today_date })

index_data = [
   {
    'date': today_date,
    'tradingCode': '00DSEX',
    'ltp': round(index_value['dsex']['index'], 2),
    'high': round(index_value['dsex']['high'], 2),
    'low': round(index_value['dsex']['low'], 2),
    'open': round(index_value['dsex']['open'], 2),
    'close': round(index_value['dsex']['close'], 2),
    'ycp': round(index_value['dsex']['open'], 2),
    'change': round(index_value['dsex']['change'], 2),
    'percentChange': round(index_value['dsex']['percentChange'], 2), 
    'trade': index_value['totalTrade'],
    'value': index_value['totalVolume'],
    'volume': index_value['totalValue'] * 1000000
   },
   {
    'date': today_date,
    'tradingCode': '00DSES',
    'ltp': round(index_value['dses']['index'], 2),
    'high': round(index_value['dses']['high'], 2),
    'low': round(index_value['dses']['low'], 2),
    'open': round(index_value['dses']['open'], 2),
    'close': round(index_value['dses']['close'], 2),
    'ycp': round(index_value['dses']['open'], 2),
    'change': round(index_value['dses']['change'], 2),
    'percentChange': round(index_value['dses']['percentChange'], 2), 
    'trade': index_value['totalTrade'],
    'value': index_value['totalVolume'],
    'volume': index_value['totalValue'] * 1000000
   },
   {
    'date': today_date,
    'tradingCode': '00DS30',
    'ltp': round(index_value['dse30']['index'], 2),
    'high': round(index_value['dse30']['high'], 2),
    'low': round(index_value['dse30']['low'], 2),
    'open': round(index_value['dse30']['open'], 2),
    'close': round(index_value['dse30']['close'], 2),
    'ycp': round(index_value['dse30']['open'], 2),
    'change': round(index_value['dse30']['change'], 2),
    'percentChange': round(index_value['dse30']['percentChange'], 2), 
    'trade': index_value['totalTrade'],
    'value': index_value['totalVolume'],
    'volume': index_value['totalValue'] * 1000000
   },
]  

share_data_array.extend(index_data)

mydb.daily_prices.insert_many(share_data_array)

myquery = {}
newvalues = { "$set": { "dailyPriceUpdateDate": today_date } }

mydb.settings.update_one(myquery, newvalues)

mydb.data_script_logs.insert_one({
    'script': 'price-daily',
    'message': "Status: OK",
    'time': datetime.datetime.now()
})

myclient.close()

