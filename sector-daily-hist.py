import pymongo, datetime, certifi
from variables import mongo_string

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient["stockanalyst"]   

def sector_data(date):
  data = mydb.daily_prices.aggregate([
      {
        '$match': {
          'date': date
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

  mydb.daily_sectors_test.insert_many(data)

# today_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
start_date = datetime.datetime(2023, 3, 1)

for x in range(500):
    new_date = start_date - datetime.timedelta(days = x)
    sector_data(new_date)
    print(new_date, " : success")
