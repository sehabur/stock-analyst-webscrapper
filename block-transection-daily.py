import requests, datetime, pymongo, certifi
from bs4 import BeautifulSoup
from variables import mongo_string, db_name

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient[db_name]

data_setting = mydb.settings.find_one()

if data_setting['dataInsertionEnable'] == 0:
    print('exiting script')
    exit()

date = datetime.datetime.now().replace(
    hour=0, minute=0, second=0, microsecond=0
)

stock_url  = 'https://www.dsebd.org/market-statistics.php'
response = requests.get(stock_url)
soup = BeautifulSoup(response.text, 'html.parser')
page_data_array = soup.find('code').getText().strip().split()
data=[]

for i in range (len(page_data_array)):
  if 'Instr' == page_data_array [i] and 'Code' == page_data_array [i+1]:
      n=i
del page_data_array [0:n+10]

for j in range (len(page_data_array)):
  if '------' == page_data_array [j]:
    m = j
del page_data_array [m:]

x=0
for y in range (int(len(page_data_array)/6)):
  data.append({
    'date': date,
    'tradingCode' : page_data_array[x],
    'maxPrice' : float(page_data_array[x+1]),
    'minPrice' : float(page_data_array[x+2]),
    'trades' : float(page_data_array[x+3]),
    'quantity' : float(page_data_array[x+4]),
    'value' : float(page_data_array[x+5])})
  x=x+6

mydb.block_transections.insert_many(data)

myquery = {}
newvalues = { "$set": { "dailyBlockTrUpdateDate": date } }

mydb.settings.update_one(myquery, newvalues)

myclient.close()

mydb.data_script_logs.insert_one({
    'script': 'lock-transection-daily',
    'message': "Status: OK",
    'time': datetime.datetime.now()
})