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

last_document = mydb.index_minute_values.find_one(sort=[('_id', -1)])

newvalues = { 
   'totalTrade' : float(page_data_array[36]),
   'totalVolume' : float(page_data_array[38]),
   'totalValue' : float(page_data_array[40]), 
   'issuesAdvanced' : float(page_data_array[48]),
   'issuesDeclined' : float(page_data_array[49]),
   'issuesUnchanged' : float(page_data_array[50]),
}

mydb.index_minute_values.update_one({'_id': last_document['_id']}, { '$set': newvalues })

