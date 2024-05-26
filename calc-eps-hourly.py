import pymongo, datetime, certifi, requests
from bs4 import BeautifulSoup
from variables import mongo_string
# from data import stocks_list

# stocks_list = ['BESTHLDNG', 'NRBBANK', 'SICL', 'GP']

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient["stockanalyst"]

data_setting = mydb.settings.find_one()

if data_setting['dataInsertionEnable'] == 0:
  print('exiting script')
  exit()

today_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

screener_scripts = mydb.screener_scripts.find({ 'date': today_date})  

stocks_list = []
for item in screener_scripts:
  stocks_list.append(item['tradingCode'])

stocks_list = list(set(stocks_list))

for stock in stocks_list:
  stock_data = mydb.fundamentals.find_one({
    'tradingCode': stock
  })

  if 'epsQuaterly' in stock_data :
    eps_quarterly_data = sorted(stock_data['epsQuaterly'], key=lambda d: str(d['year']), reverse=True)

    if len(eps_quarterly_data) < 1:
      continue

    eps_data = eps_quarterly_data[0] 

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
      eps_q1 = eps_data['q1'] if 'q1' in eps_data else 0
      eps_q2 = eps_data['q2'] if 'q2' in eps_data else 0
      eps_q3 = eps_data['q3'] if 'q3' in eps_data else 0
      eps_q4 = eps_data['q4'] if 'q4' in eps_data else 0

      total = eps_q1 + eps_q2 + eps_q3 + eps_q4

      eps = round((total / count) * 4, 3)

    myquery = { 'tradingCode': stock }

    newvalues = { "$set": { 
        "epsCurrent": eps,
    } }

    mydb.fundamentals.update_one(myquery, newvalues)

    print(stock, eps, 'Success')

  else:
    print(stock, 'error occured. epsQuaterly not found')
  