import requests, datetime, pymongo, certifi
from bs4 import BeautifulSoup
from pytz import timezone
from variables import mongo_string

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient["stockanalyst"]

data_setting = mydb.settings.find_one()

if data_setting['dataInsertionEnable'] == 0:
    print('exiting script')
    exit()

stock_url  = 'https://www.dsebd.org'

response = requests.get(stock_url)

soup = BeautifulSoup(response.text, 'html.parser')
page_data_array = soup.find(attrs={'class': 'col-md-6 col-xs-12 col-sm-12 LeftColHome'}).getText().strip().splitlines()


today_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

today_time = datetime.datetime.now(timezone('Asia/Dhaka')).replace(second=0, microsecond=0)

data = {
    'dsex' : {
        'index' : float(page_data_array[3]),
        'change' : float(page_data_array[5]),
        'percentChange' : float(page_data_array[7].strip().replace('%',''))
    }, 
    'dses' : {
        'index' : float(page_data_array[12]),
        'change' : float(page_data_array[14]),
        'percentChange' : float(page_data_array[16].strip().replace('%',''))
    }, 
    'dse30' : {
        'index' : float(page_data_array[21]),
        'change' : float(page_data_array[23]),
        'percentChange' : float(page_data_array[25].strip().replace('%',''))
    }, 
    'totalTrade' : float(page_data_array[36]),
    'totalVolume' : float(page_data_array[38]),
    'totalValue' : float(page_data_array[40]),
    'issuesAdvanced' : float(page_data_array[48]),
    'issuesDeclined' : float(page_data_array[49]),
    'issuesUnchanged' : float(page_data_array[50]),
    'time': today_time,
    'date': today_date
    }

data_v2 = [
    {
        'date': today_date,
        'time': today_time,
        'tradingCode': '00DSEX',
        'index': data['dsex']['index'],
        'change': data['dsex']['change'],
        'percentChange': data['dsex']['percentChange'], 
        'trade': data['totalTrade'],
        'value': data['totalValue'],
        'volume': data['totalVolume'],
    },
    {
        'date': today_date,
        'time': today_time,
        'tradingCode': '00DSES',
        'index': data['dses']['index'],
        'change': data['dses']['change'],
        'percentChange': data['dses']['percentChange'], 
        'trade': data['totalTrade'],
        'value': data['totalValue'],
        'volume': data['totalVolume'],
    },
    {
        'date': today_date,
        'time': today_time,
        'tradingCode': '00DS30',
        'index': data['dse30']['index'],
        'change': data['dse30']['change'],
        'percentChange': data['dse30']['percentChange'], 
        'trade': data['totalTrade'],
        'value': data['totalValue'],
        'volume': data['totalVolume'],
    },
]

mydb.index_minute_values.insert_one(data)

mydb.index_day_minute_values.insert_many(data_v2)
