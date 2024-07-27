
import requests, pymongo, certifi, datetime
from pytz import timezone
from variables import mongo_string
from data import stocks_list

# stocks_list = ['GP', 'EHL']

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient["stockanalyst"]

for trading_code in stocks_list:

    r = requests.get("http://localhost:5000/api/prices/marketDepth", params={ 'inst': trading_code })

    data = r.json()

    stock_found = mydb.halt_shares.find_one({ 'tradingCode': trading_code }, { "tradingCode": 1})

    newvalues = {
        'tradingCode': trading_code,
        'date': datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0), 
        'time': datetime.datetime.now(timezone('Asia/Dhaka')).replace(second=0, microsecond=0), 
        'status': data['status'], 
    }

    if stock_found:
        mydb.halt_shares.update_one({ 'tradingCode': trading_code }, { '$set': newvalues } )
    else:
        mydb.halt_shares.insert_one(newvalues)

myclient.close()