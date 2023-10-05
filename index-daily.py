import requests, datetime, pymongo, certifi
from bs4 import BeautifulSoup
from variables import mongo_string

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient["stockanalyst"]

data_setting = mydb.settings.find_one()

if data_setting['dataInsertionEnable'] == 0:
    print('exiting script')
    exit()

stock_url  = 'https://www.dsebd.org'
today_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
response = requests.get(stock_url)

soup = BeautifulSoup(response.text, 'html.parser')
page_data_array = soup.find(attrs={'class': 'col-md-6 col-xs-12 col-sm-12 LeftColHome'}).getText().strip().splitlines()

data = {'dsex' : {
    'index' : float(page_data_array[3]),
    'change' : float(page_data_array[5]),
    'percentChange' : float(page_data_array[7].strip().replace('%',''))
}, 'dses' : {
    'index' : float(page_data_array[12]),
    'change' : float(page_data_array[14]),
    'percentChange' : float(page_data_array[16].strip().replace('%',''))
}, 'dse30' : {
    'index' : float(page_data_array[21]),
    'change' : float(page_data_array[23]),
    'percentChange' : float(page_data_array[25].strip().replace('%',''))
}, 'totalTrade' : float(page_data_array[36]),
   'totalVolume' : float(page_data_array[38]),
   'totalValue' : float(page_data_array[40]),
    'issuesAdvanced' : float(page_data_array[48]),
    'issuesDeclined' : float(page_data_array[49]),
    'issuesUnchanged' : float(page_data_array[50]),
    "date": today_date, 
    "time": today_date
}

mydb.index_daily_values.insert_one(data)

myquery = {}
newvalues = { "$set": { "dailyIndexUpdateDate": today_date } }

mydb.settings.update_one(myquery, newvalues)