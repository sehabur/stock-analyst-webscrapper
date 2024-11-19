import pymongo, certifi, datetime
from variables import mongo_string, db_name

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient[db_name]

data_setting = mydb.settings.find_one()

if data_setting['dataInsertionEnable'] == 0:
    print('exiting script as data insertion disabled')
    exit()

# today_date = datetime.datetime(2024, 11, 19, 0, 0)
today_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

news_list = mydb.news.find({
    'date': today_date,
    'title': { '$regex': 'Spot News', '$options': 'i' },
    'description': { '$regex': 'Trading of the shares of the company', '$options': 'i' },  
})

for news in news_list:
    description = news['description'].split(" ")

    for i in range(len(description)):
        if (description[i].lower() == 'from'):
            try:
              from_date = datetime.datetime.strptime(description[i+1], "%d.%m.%Y")
            except ValueError:
              from_date = None   
            continue   
        if (description[i].lower() == 'to'):
            try:
              to_date = datetime.datetime.strptime(description[i+1].strip("."), "%d.%m.%Y").replace(hour=23, minute=59, second=0, microsecond=0)
            except ValueError:
              to_date = None  
            break
        
    # print(news['tradingCode'], from_date, to_date)
    
    if from_date and to_date:
        mydb.fundamentals.update_one({ 'tradingCode': news['tradingCode'] }, { '$set': { 'spotRange': [from_date, to_date] } })
    