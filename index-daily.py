import datetime, pymongo, certifi
from variables import mongo_string, db_name

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient[db_name]

data_setting = mydb.settings.find_one()

if data_setting['dataInsertionEnable'] == 0:
    print('exiting script')
    exit()

# today_date = datetime.datetime(2024, 7, 10, 0, 0)
today_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

data = mydb.index_minute_values.aggregate([
    {
        '$match': {
            'date': today_date,
            'dsex.index': { '$ne': 0 },
            'dses.index': { '$ne': 0 },
            'dse30.index': { '$ne': 0 },
        }
    },
    {
        '$sort': {
            'time': 1,
      },   
    },
    {
        '$group': {
            '_id': None,
            'dsex_index': { '$last': "$dsex.index" },
            'dsex_open': { '$first': "$dsex.index" },
            'dsex_high': { '$max': "$dsex.index" },
            'dsex_low': { '$min': "$dsex.index" },
            'dsex_close': { '$last': "$dsex.index" },
            'dsex_change': { '$last': "$dsex.change" },
            'dsex_percentChange': { '$last': "$dsex.percentChange" },

            'dses_index': { '$last': "$dses.index" },
            'dses_open': { '$first': "$dses.index" },
            'dses_high': { '$max': "$dses.index" },
            'dses_low': { '$min': "$dses.index" },
            'dses_close': { '$last': "$dses.index" },
            'dses_change': { '$last': "$dses.change" },
            'dses_percentChange': { '$last': "$dses.percentChange" },
            
            'dse30_index': { '$last': "$dse30.index" },
            'dse30_open': { '$first': "$dse30.index" },
            'dse30_high': { '$max': "$dse30.index" },
            'dse30_low': { '$min': "$dse30.index" },
            'dse30_close': { '$last': "$dse30.index" },
            'dse30_change': { '$last': "$dse30.change" },
            'dse30_percentChange': { '$last': "$dse30.percentChange" },

            'totalTrade': { '$last': "$totalTrade" },
            'totalVolume': { '$last': "$totalVolume" },
            'totalValue': { '$last': "$totalValue" },
            'issuesAdvanced': { '$last': "$issuesAdvanced" },
            'issuesDeclined': { '$last': "$issuesDeclined" },
            'issuesUnchanged': { '$last': "$issuesUnchanged" },
        }
    },
    {
        '$project': {
            '_id': 0,
            'date': today_date,
            'dsex': {
                'index': '$dsex_index',
                'open': '$dsex_open',
                'high': '$dsex_high',
                'low': '$dsex_low',
                'close': '$dsex_close',
                'change': '$dsex_change',
                'percentChange': '$dsex_percentChange',
            },
            'dses': {
                'index': '$dses_index',
                'open': '$dses_open',
                'high': '$dses_high',
                'low': '$dses_low',
                'close': '$dses_close',
                'change': '$dses_change',
                'percentChange': '$dses_percentChange',
            },
            'dse30': {
                'index': '$dse30_index',
                'open': '$dse30_open',
                'high': '$dse30_high',
                'low': '$dse30_low',
                'close': '$dse30_close',
                'change': '$dse30_change',
                'percentChange': '$dse30_percentChange',
            },
            'totalTrade': 1,
            'totalVolume': 1,
            'totalValue': 1,
            'issuesAdvanced': 1,
            'issuesDeclined': 1,
            'issuesUnchanged': 1,
        }
    }
])

for document in data:
    mydb.index_daily_values.insert_one(document)
    break

myquery = {}
newvalues = { "$set": { "dailyIndexUpdateDate": today_date } }

mydb.settings.update_one(myquery, newvalues)

mydb.data_script_logs.insert_one({
    'script': 'index-daily',
    'message': "Status: OK",
    'time': datetime.datetime.now()
})