import pymongo, certifi
from variables import mongo_string, db_name

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient[db_name]

old_trading_code = "AAGP"
new_trading_code = "NGP"
verifier = "arc456hfdr4d"

collections = ["block_transections", "daily_prices", "fundamentals", "minute_prices", "news", "yesterday_prices"]

if verifier == "arc456hfd3xd":
  for coll in collections:
    result = mydb[coll].update_one({ 'tradingCode': old_trading_code }, { "$set": { "tradingCode": new_trading_code } })
    print("col:", coll, "|", "documents_updated:", result.modified_count)

myclient.close()
