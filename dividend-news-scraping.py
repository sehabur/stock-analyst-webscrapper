import pymongo, certifi, datetime, re
from data import stocks_list_details
from variables import mongo_string

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient["stockanalyst"]

data_setting = mydb.settings.find_one()

# if data_setting['dataInsertionEnable'] == 0:
#     print('exiting script as data insertion disabled')
#     exit()

today_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

news_list = mydb.news.find({
    'date':   { '$gt':  datetime.datetime(2023, 6, 30, 0, 0) } ,
    'title': { '$regex': 'Dividend Declaration', '$options': 'i' } ,
})

data = {}

for news in news_list: 

    title = news['title'].split()
    trading_code = news['tradingCode'] + (title[-1] if len(title) > 4 else '')

    if trading_code in data:
        data[trading_code]['description'] = news['description'] + data[trading_code]['description']
    else:
        data[trading_code] = {
            'title': news['title'],
            'description': news['description']
        }

print(data.keys())