import pymongo, datetime, certifi
from variables import mongo_string

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient["stockanalyst"]   

def sector_data(date):
  data = mydb.daily_prices.aggregate([
      {
        '$match': {
          'date': date,
        }
      },
      {
        '$project': {
          'ltp': {
            '$cond': [
              { '$gt': ["$ltp", 0] },
              "$ltp",
              "$ycp",
            ],
          },
          'open': {
            '$cond': [
              { '$gt': ["$ltp", 0] },
              "$open",
              "$ycp",
            ],
          },
          'high': {
            '$cond': [
              { '$gt': ["$ltp", 0] },
              "$high",
              "$ycp",
            ],
          },
          'low': {
            '$cond': [
              { '$gt': ["$ltp", 0] },
              "$low",
              "$ycp",
            ],
          },
          'close': {
            '$cond': [
              { '$gt': ["$ltp", 0] },
              "$close",
              "$ycp",
            ],
          },
          'change': 1,
          'ycp': 1,
          'trade': 1,
          'value': 1,
          'volume': 1,
          'tradingCode': 1,
        } 
      },
      {
        '$unionWith': {
          'coll': "inactive_stocks",
          'pipeline': [
            {
              "$addFields": {
                "date": date,
                'ltp':  '$price',
                'ycp':  '$price',
                'high':  '$price',
                'low':  '$price',
                'close':  '$price',
                'open':  '$price',
                'change':  0,
                'trade':  0,
                'value':  0,
                'volume':  0,
              },
            }
          ]
        },
      },
      {
        '$lookup': {
          'from': 'fundamentals',
          'localField': 'tradingCode',
          'foreignField': 'tradingCode',
          'as': 'fundamentals',
        },
      },
      { '$unwind': '$fundamentals' },
      {
          '$group': {
              '_id': '$fundamentals.sector',
              'ltp': { '$avg': '$ltp' },
              'ycp': { '$avg': '$ycp' },
              'high': { '$avg': '$high' },
              'low': { '$avg': '$low' },
              'close': { '$avg': '$close' },
              'open': { '$avg': '$open' },
              'change': { '$avg': '$change' },
              'trade': { '$sum': '$trade' },
              'value': { '$sum': '$value' },
              'volume': { '$sum': '$volume' },
              'totalStocks': { "$sum": 1 }
          }
      },
      {
        '$project': {
          "_id": 0, 
          'date': date,
          'sector': '$_id',
          'ltp': { '$round': ['$ltp', 2] },
          'ycp': { '$round': ['$ycp', 2] },
          'high': { '$round': ['$high', 2] },
          'low': { '$round': ['$low', 2] },
          'close': { '$round': ['$close', 2] },
          'open': { '$round': ['$open', 2] },
          'change': { '$round': ['$change', 2] },
          'trade': { '$round': ['$trade', 2] },
          'value': { '$round': ['$value', 2] },
          'volume': { '$round': ['$volume', 2] },        
        },
      },
  ])
  # for x in data:
  #   print(x)
  
  mydb.daily_sectors.insert_many(data)    


# today_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
start_date = datetime.datetime(2024, 4, 4)

for x in range(500):
    new_date = start_date - datetime.timedelta(days = x)

    cursor = mydb.daily_prices.find({ 'date': new_date })
    count = len(list(cursor))

    if count == 0:
       continue

    sector_data(new_date)
    print(new_date, " : success")
