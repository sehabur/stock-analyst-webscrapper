import requests, datetime, pymongo
from bs4 import BeautifulSoup
from variables import mongo_string

stock_url  = 'https://www.dsebd.org'

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
}, "date": datetime.datetime.now().replace(
    hour=0, minute=0, second=0, microsecond=0
)}

myclient = pymongo.MongoClient(mongo_string)
mydb = myclient["stockAnalyst"]
mycol = mydb["index_daily_values"]

mycol.insert_one(data)