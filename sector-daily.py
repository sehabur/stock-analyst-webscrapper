import pymongo, datetime, certifi
from variables import mongo_string

todayDate = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
# todayDate = datetime.datetime.now().replace(year=2023, month=8, day=3, hour=0, minute=0, second=0, microsecond=0)

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient["stockanalyst"]

data = mydb.latest_prices.aggregate([
    {
      '$lookup': {
        'from': 'fundamentals',
        'localField': 'tradingCode',
        'foreignField': 'tradingCode',
        'as': 'fundamentals',
      },
    },
    { '$addFields': { 'fundamentals': { '$first': '$fundamentals' } } },
    {
        '$group': {
            '_id': '$fundamentals.sector',
            'ltp': { '$avg': '$ltp' },
            'ycp': { '$avg': '$ycp' },
            'high': { '$avg': '$high' },
            'low': { '$avg': '$low' },
            'close': { '$avg': '$close' },
            'change': { '$avg': '$change' },
            'trade': { '$sum': '$trade' },
            'value': { '$sum': '$value' },
            'volume': { '$sum': '$volume' },
        }
    },
    {
      '$project': {
        "_id": 0, 
        'date': todayDate,
        'time': todayDate,
        'sector': '$_id',
        'ltp': { '$round': ['$ltp', 2] },
        'ycp': { '$round': ['$ycp', 2] },
        'high': { '$round': ['$high', 2] },
        'low': { '$round': ['$low', 2] },
        'close': { '$round': ['$close', 2] },
        'change': { '$round': ['$change', 2] },
        'trade': { '$round': ['$trade', 2] },
        'value': { '$round': ['$value', 2] },
        'volume': { '$round': ['$volume', 2] },        
      },
    },
])

mydb.daily_sectors.insert_many(data)