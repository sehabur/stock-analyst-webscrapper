import pymongo, certifi, datetime
from variables import mongo_string, db_name

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient[db_name]

data_setting = mydb.settings.find_one()

if data_setting['dataInsertionEnable'] == 0:
    print('exiting script as data insertion disabled')
    exit()

# today_date = datetime.datetime(2024, 10, 11, 0, 0)
today_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

news_list = mydb.news.find({
    'date': today_date,
    'title': { '$regex': 'Price Limit Open', '$options': 'i' },
    'description': { '$regex': 'There will be no price limit', '$options': 'i' },  
})

for news in news_list:
    description = news['description'].split(" ")

    for i in range(len(description)):
        if (description[i].lower() == 'company' and description[i+1].lower() == 'today'):
            try:
              date = datetime.datetime.strptime(description[i+2].strip("()"), "%d.%m.%Y")
            except ValueError:
              date = None  
            break
        
    # print(news['tradingCode'], date)
    
    if date:
        mydb.fundamentals.update_one({ 'tradingCode': news['tradingCode'] }, { '$set': { 'declarationDate': date } })
    