import pymongo, datetime, certifi
from variables import mongo_string

inactiveStocks = [
  "UNITEDAIR",
  "ONEBANK",
  "Monno jute stafllers ltd",
  "CAPITECGBF",
  "ICB2NDNRB",
  "NLI1STMF",
  "SEBL1STMF",
  "BXSYNTH",
  "GLAXOSMITH",
]

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient["stockanalyst"]

# mydb.fundamentals.update_many({}, { '$set': { 'isActive': True } })

for stock_code in inactiveStocks:
    mydb.fundamentals.update_one({ 'tradingCode': stock_code }, { '$set': { 'isActive': False } })