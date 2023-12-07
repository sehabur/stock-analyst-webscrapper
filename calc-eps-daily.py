import pymongo, datetime, certifi, requests
from bs4 import BeautifulSoup
from variables import mongo_string
from data import stocks_list
# stocks_list = ['ANWARGALV', 'BSRMSTEEL']
myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient["stockanalyst"]

data_setting = mydb.settings.find_one()

# if data_setting['dataInsertionEnable'] == 0:
#   print('exiting script')
#   exit()

for stock in stocks_list:
  stock_data = mydb.fundamentals.find_one({
    'tradingCode': stock
  })

  if 'epsQuaterly' in stock_data :
    eps_data = sorted(stock_data['epsQuaterly'], key=lambda d: d['year'], reverse=True)[0] 

    count = 0

    if 'q4' in eps_data:
      count = count + 1
    if 'q3' in eps_data:
      count = count + 1
    if 'q2' in eps_data:
      count = count + 1
    if 'q1' in eps_data:
      count = count + 1

    if count == 0:
      eps = 0
    else:
      total = eps_data['q1'] if 'q1' in eps_data else 0 + eps_data['q2'] if 'q2' in eps_data else 0 + eps_data['q3'] if 'q3' in eps_data else 0 + eps_data['q4'] if 'q4' in eps_data else 0
      
      eps = round((total / count) * 4, 3)

    print(stock, eps)

    myquery = { 'tradingCode': stock }

    newvalues = { "$set": { 
        "epsCurrent": eps,
    } }

    mydb.fundamentals.update_one(myquery, newvalues)

  else:
    print(stock, 'error')
  