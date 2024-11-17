import pymongo, certifi
from variables import mongo_string, db_name

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient[db_name]

data = mydb.fundamentals.find({ 'isActive': True, 'type': 'stock' }, 
                              {'tradingCode': 1, 'companyName': 1, 'sector': 1, 'yearEnd': 1, 'category': 1, '_id': 0 })

stocks_list = []
stocks_list_details = []

for stock in data:
    stocks_list.append(stock['tradingCode'])
    stocks_list_details.append(stock)

# print(stocks_list)    