import pymongo, certifi, requests
from bs4 import BeautifulSoup
from variables import mongo_string

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient["stockanalyst"]

data_setting = mydb.settings.find_one()

if data_setting['dataInsertionEnable'] == 0:
    print('exiting script')
    exit()

stock_url = 'https://www.dsebd.org'
response = requests.get(stock_url)
soup = BeautifulSoup(response.text, 'html.parser')
page_data_array = soup.find(attrs={'class': 'col-md-6 col-xs-12 col-sm-12 LeftColHome'}).getText().strip().splitlines()

currentVolume = float(page_data_array[38])

myquery = {}
newvalues = { "$set": { "dataInsertionEnable": 0, 'lastVolume': currentVolume } }

mydb.settings.update_one(myquery, newvalues)