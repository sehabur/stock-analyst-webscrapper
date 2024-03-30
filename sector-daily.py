import pymongo, datetime, certifi
from variables import mongo_string

today_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
# today_date = datetime.datetime.now().replace(year=2023, month=8, day=3, hour=0, minute=0, second=0, microsecond=0)

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient["stockanalyst"]

data_setting = mydb.settings.find_one()

if data_setting['dataInsertionEnable'] == 0:
    print('exiting script')
    exit()

data = mydb.daily_prices.aggregate([
    {
      '$match': {
        'date': today_date
      }
    },
    {
      '$unionWith': {
        'coll': "inactive_stocks",
        'pipeline': [
          {
            "$addFields": {
              "date": today_date,
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
        }
    },
    {
      '$project': {
        "_id": 0, 
        'date': today_date,
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

mydb.daily_sectors.insert_many(data)

myquery = {}
newvalues = { "$set": { "dailySectorUpdateDate": today_date } }

mydb.settings.update_one(myquery, newvalues)