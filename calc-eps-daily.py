import pymongo, datetime, certifi, requests
from bs4 import BeautifulSoup
from variables import mongo_string, db_name
from data import stocks_list

# stocks_list = ['CLICL']

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient[db_name]

data_setting = mydb.settings.find_one()

if data_setting['dataInsertionEnable'] == 0:
  print('exiting script')
  exit()

for stock in stocks_list:
  stock_data = mydb.fundamentals.find_one({
    'tradingCode': stock
  })

  if 'epsQuaterly' in stock_data and len(stock_data['epsQuaterly']) > 0 :
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
      } 
    }

    mydb.fundamentals.update_one(myquery, newvalues)

  elif 'epsYearly' in stock_data and len(stock_data['epsYearly']) > 0 :  
    eps_yearly_data = sorted(stock_data['epsYearly'], key=lambda d: str(d['year']), reverse=True)

    eps = eps_yearly_data[0]['value']

    myquery = { 'tradingCode': stock }
    newvalues = { "$set": { 
        "epsCurrent": eps,
      } 
    }

    mydb.fundamentals.update_one(myquery, newvalues)

  else:
    print(stock, 'error occured. epsQuaterly not found')

mydb.data_script_logs.insert_one({
    'script': 'calc-eps-daily',
    'message': f"Status: Ok",
    'time': datetime.datetime.now()
})

  