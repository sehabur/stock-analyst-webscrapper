import pymongo, datetime, certifi, requests
from bs4 import BeautifulSoup
from variables import mongo_string

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient["stockanalyst"]

data_setting = mydb.settings.find_one()

if data_setting['dataInsertionEnable'] == 1:
    print('exiting script')
    exit()

stock_url = 'https://www.dsebd.org'
response = requests.get(stock_url)
soup = BeautifulSoup(response.text, 'html.parser')
page_data_array = soup.find(attrs={'class': 'col-md-6 col-xs-12 col-sm-12 LeftColHome'}).getText().strip().splitlines()

currentVolume = float(page_data_array[38])

if (currentVolume == data_setting['lastVolume']):
    print('exiting script')
    exit()

updateDate = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

myquery = {}
newvalues = { "$set": { "minuteDataUpdateDate": updateDate, "dataInsertionEnable": 1 } }

mydb.settings.update_one(myquery, newvalues)