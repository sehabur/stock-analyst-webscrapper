import pymongo, certifi
from variables import mongo_string
from data import stocks_list

# stocks_list = ['ACMEPL']

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient["stockanalyst"]

data_setting = mydb.settings.find_one()

if data_setting['dataInsertionEnable'] == 0:
    print('exiting script as data insertion disabled')
    exit()

def basic_data_update(trading_code):

    initialdata = mydb.daily_prices.aggregate([
        {
            '$match': {
                'tradingCode': trading_code,
            },
        },
        {
            '$sort': {
                'date': -1,
            }
        },
        {
            '$facet': {
                'rawData': [],
                'alltime': [
                    {
                        '$match': {
                            'low' : {
                                '$gt': 0
                            }
                        }
                    },
                    {
                        '$group': {
                            '_id': None,
                            'high': { '$max': '$high' },
                            'low': { '$min': '$low' }
                        }
                    }
                ],
                'fiveYear': [
                    {
                        '$limit': 1250
                    },
                    {
                        '$match': {
                            'low' : {
                                '$gt': 0
                            }
                        }
                    },
                    {
                        '$group': {
                            '_id': None,
                            'high': { '$max': '$high' },
                            'low': { '$min': '$low' }
                        }
                    }
                ],
                'oneYear': [
                    {
                        '$limit': 250
                    },
                    {
                        '$match': {
                            'low' : {
                                '$gt': 0
                            }
                        }
                    },
                    {
                        '$group': {
                            '_id': None,
                            'high': { '$max': '$high' },
                            'low': { '$min': '$low' }
                        }
                    }
                ],
                'sixMonth': [
                    {
                        '$limit': 130
                    },
                    {
                        '$match': {
                            'low' : {
                                '$gt': 0
                            }
                        }
                    },
                    {
                        '$group': {
                            '_id': None,
                            'high': { '$max': '$high' },
                            'low': { '$min': '$low' }
                        }
                    }
                ],
                'oneMonth': [
                    {
                        '$limit': 22
                    },
                    {
                        '$match': {
                            'low' : {
                                '$gt': 0
                            }
                        }
                    },
                    {
                        '$group': {
                            '_id': None,
                            'high': { '$max': '$high' },
                            'low': { '$min': '$low' }
                        }
                    }
                ],
                'oneWeek': [
                    {
                        '$limit': 5
                    },
                    {
                        '$match': {
                            'low' : {
                                '$gt': 0
                            }
                        }
                    },
                    {
                        '$group': {
                            '_id': None,
                            'high': { '$max': '$high' },
                            'low': { '$min': '$low' }
                        }
                    }
                ]
            }
        }
    ]) 

    data = list(initialdata)[0]

    # print(data['oneWeek'])
    # exit()
    rawdata = data['rawData']

    fiveYearBeforeData = rawdata[1250]['close'] if len(rawdata) > 1250 else "-"
    oneYearBeforeData = rawdata[250]['close'] if len(rawdata) > 250 else "-"
    sixMonthBeforeData = rawdata[130]['close'] if len(rawdata) > 130 else "-"
    oneMonthBeforeData = rawdata[22]['close'] if len(rawdata) > 22 else "-"
    oneWeekBeforeData = rawdata[5]['close'] if len(rawdata) > 5 else "-"

    alltimeHigh = data['alltime'][0]['high'] if len(data['alltime']) > 0 else "-"
    fiveYearHigh = data['fiveYear'][0]['high']  if len(data['fiveYear']) > 0 else "-"
    oneYearHigh = data['oneYear'][0]['high']  if len(data['oneYear']) > 0 else "-"
    sixMonthHigh = data['sixMonth'][0]['high'] if len(data['sixMonth']) > 0 else "-"
    oneMonthHigh = data['oneMonth'][0]['high'] if len(data['oneMonth']) > 0 else "-"
    oneWeekHigh = data['oneWeek'][0]['high'] if len(data['oneWeek']) > 0 else "-"

    alltimeLow = data['alltime'][0]['low']  if len(data['alltime']) > 0 else "-"
    fiveYearLow = data['fiveYear'][0]['low']  if len(data['fiveYear']) > 0 else "-"
    oneYearLow = data['oneYear'][0]['low']  if len(data['oneYear']) > 0 else "-"
    sixMonthLow = data['sixMonth'][0]['low'] if len(data['sixMonth']) > 0 else "-"
    oneMonthLow = data['oneMonth'][0]['low'] if len(data['oneMonth']) > 0 else "-"
    oneWeekLow = data['oneWeek'][0]['low'] if len(data['oneWeek']) > 0 else "-"
    
    myquery = { 'tradingCode': trading_code, 'date': data_setting['dailyPriceUpdateDate'] }

    newvalues = { "$set": { 
        "alltimeHigh": alltimeHigh,
        "fiveYearHigh": fiveYearHigh,
        "oneYearHigh": oneYearHigh,
        "sixMonthHigh": sixMonthHigh,
        "oneMonthHigh": oneMonthHigh,
        "oneWeekHigh": oneWeekHigh,
        "alltimeLow": alltimeLow,
        "fiveYearLow": fiveYearLow,
        "oneYearLow": oneYearLow,
        "sixMonthLow": sixMonthLow,
        "oneMonthLow": oneMonthLow,
        "oneWeekLow": oneWeekLow,
        "fiveYearBeforeData": fiveYearBeforeData,
        "oneYearBeforeData": oneYearBeforeData,
        "oneYearBeforeData": oneYearBeforeData,
        "sixMonthBeforeData": sixMonthBeforeData,
        "oneMonthBeforeData": oneMonthBeforeData,
        "oneWeekBeforeData": oneWeekBeforeData,
    } }

    mydb.daily_prices.update_one(myquery, newvalues)

for stock in stocks_list:
    basic_data_update(stock)
    print(stock, 'success')