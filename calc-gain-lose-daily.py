import pymongo, certifi, datetime
from variables import mongo_string
from data import stocks_list

# stocks_list = ['GP', 'ROBI']

"""
    This script will run everyday regardless 
    of share opening or close day
"""

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient["stockanalyst"]

def calculate_query_date(type, today):
    query_date = {}
    if type == 'monthly':
        month_temp = today.month - 1

        if month_temp == 0:
            query_date = {
                'year': today.year - 1,
                'month': month_temp + 12,
                'day': today.day
            }
        else:
            query_date = {
                'year': today.year,
                'month': month_temp,
                'day': today.day
            }

    elif type == 'yearly':
        query_date = {
            'year': today.year - 1,
            'month': today.month,
            'day': today.day
        }

    elif type == 'fiveYearly':
        query_date = {
            'year': today.year - 5,
            'month': today.month,
            'day': today.day
        }

    elif type == 'sixMonthly':
        month_temp = today.month - 6

        if month_temp < 1:
            query_date = {
                'year': today.year - 1,
                'month': month_temp + 12,
                'day': today.day
            }
        else:
            query_date = {
                'year': today.year,
                'month': month_temp,
                'day': today.day
            }

    elif type == 'fiveYearly':
        query_date = {
            'year': today.year - 5,
            'month': today.month,
            'day': today.day
        }

    elif type == 'weekly':
        month_day_map = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        day_temp = today.day - 7

        if day_temp < 1:
            day_final = month_day_map[today.month-2] + day_temp
            month_temp = today.month - 1

            if month_temp == 0:
                month_final = month_temp + 12
                year_final = today.year - 1
            else:
                month_final = month_temp
                year_final = today.year
        else:
            day_final = day_temp
            month_final = today.month
            year_final = today.year

        query_date = {
            'year': year_final,
            'month': month_final,
            'day': day_final
        }   
 
    return datetime.datetime(query_date['year'], query_date['month'], query_date['day'], 0, 0)

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
                'rawData': [
                    {
                        '$project': {
                            '_id': 0,
                            'date': 1,
                            'ltp': 1,
                            'close': 1,
                            'value': 1,
                            'volume': 1,
                            'trade': 1,
                            'ycp': 1
                        }
                    }
                ],
                'alltime': [
                    {
                        '$match': {
                            'ltp' : {
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
                            'ltp' : {
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
                            'ltp' : {
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
                            'ltp' : {
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
                            'ltp' : {
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
                            'ltp' : {
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

    rawdata = data['rawData']

    # today = datetime.datetime.fromisoformat('2023-11-06')
    today = datetime.date.today()

    query_date = {
        'weekly': calculate_query_date('weekly', today),
        'monthly': calculate_query_date('monthly', today),
        'sixMonthly': calculate_query_date('sixMonthly', today),
        'yearly': calculate_query_date('yearly', today),
        'fiveYearly': calculate_query_date('fiveYearly', today),
    }
    check_element = [
        'weekly',
        'monthly',
        'sixMonthly',
        'yearly',
        'fiveYearly',
    ]
    before_data = {}
    before_value = {}
    before_volume = {}
    before_trade = {}

    for item in rawdata:
        if len(check_element) > 0:
            if item['date'] <= query_date[check_element[0]]:
                before_data[check_element[0]] = item['ltp'] if item['ltp'] != 0 else item['ycp']
                before_value[check_element[0]] = item['value'] if item['value'] != 0 else 0.000001
                before_volume[check_element[0]] = item['volume'] if item['volume'] != 0 else 0.000001
                before_trade[check_element[0]] = item['trade'] if item['trade'] != 0 else 0.000001
                check_element.pop(0)

    fiveYearBeforeData = before_data['fiveYearly'] if 'fiveYearly' in before_data  else "-"
    oneYearBeforeData = before_data['yearly'] if 'yearly' in before_data  else "-"
    sixMonthBeforeData = before_data['sixMonthly'] if 'sixMonthly' in before_data  else "-"
    oneMonthBeforeData = before_data['monthly'] if 'monthly' in before_data  else "-"
    oneWeekBeforeData = before_data['weekly'] if 'weekly' in before_data  else "-"

    fiveYearBeforeValue = before_value['fiveYearly'] if 'fiveYearly' in before_value  else "-"
    oneYearBeforeValue = before_value['yearly'] if 'yearly' in before_value  else "-"
    sixMonthBeforeValue = before_value['sixMonthly'] if 'sixMonthly' in before_value  else "-"
    oneMonthBeforeValue = before_value['monthly'] if 'monthly' in before_value  else "-"
    oneWeekBeforeValue = before_value['weekly'] if 'weekly' in before_value  else "-"

    fiveYearBeforeVolume = before_volume['fiveYearly'] if 'fiveYearly' in before_volume  else "-"
    oneYearBeforeVolume = before_volume['yearly'] if 'yearly' in before_volume  else "-"
    sixMonthBeforeVolume = before_volume['sixMonthly'] if 'sixMonthly' in before_volume  else "-"
    oneMonthBeforeVolume = before_volume['monthly'] if 'monthly' in before_volume  else "-"
    oneWeekBeforeVolume = before_volume['weekly'] if 'weekly' in before_volume  else "-"

    fiveYearBeforeTrade = before_trade['fiveYearly'] if 'fiveYearly' in before_trade  else "-"
    oneYearBeforeTrade = before_trade['yearly'] if 'yearly' in before_trade  else "-"
    sixMonthBeforeTrade = before_trade['sixMonthly'] if 'sixMonthly' in before_trade  else "-"
    oneMonthBeforeTrade = before_trade['monthly'] if 'monthly' in before_trade  else "-"
    oneWeekBeforeTrade = before_trade['weekly'] if 'weekly' in before_trade  else "-"

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
    
    data_setting = mydb.settings.find_one()

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
        "sixMonthBeforeData": sixMonthBeforeData,
        "oneMonthBeforeData": oneMonthBeforeData,
        "oneWeekBeforeData": oneWeekBeforeData,

        "fiveYearBeforeValue": fiveYearBeforeValue,
        "oneYearBeforeValue": oneYearBeforeValue,
        "sixMonthBeforeValue": sixMonthBeforeValue,
        "oneMonthBeforeValue": oneMonthBeforeValue,
        "oneWeekBeforeValue": oneWeekBeforeValue,

        "fiveYearBeforeVolume": fiveYearBeforeVolume,
        "oneYearBeforeVolume": oneYearBeforeVolume,
        "sixMonthBeforeVolume": sixMonthBeforeVolume,
        "oneMonthBeforeVolume": oneMonthBeforeVolume,
        "oneWeekBeforeVolume": oneWeekBeforeVolume,

        "fiveYearBeforeTrade": fiveYearBeforeTrade,
        "oneYearBeforeTrade": oneYearBeforeTrade,
        "sixMonthBeforeTrade": sixMonthBeforeTrade,
        "oneMonthBeforeTrade": oneMonthBeforeTrade,
        "oneWeekBeforeTrade": oneWeekBeforeTrade,
    } }

    mydb.daily_prices.update_one(myquery, newvalues)

try:
    for stock in stocks_list:
        basic_data_update(stock)
        print(stock, 'success') 
except Exception as excp:
    print("Error: ", excp)
    mydb.errors.insert_one({
        'script': 'calc-gain-lose-daily',
        'message': str(excp),
        'createdAt': datetime.datetime.now()
    })
   