import pymongo, certifi, datetime
from variables import mongo_string

"""
    This script will run everyday regardless 
    of share opening or close day
"""

sector_list = [
  { "name": "Bank", "tag": "bank" },
  { "name": "Cement", "tag": "cement" },
  { "name": "Ceramics Sector", "tag": "ceramics" },
  { "name": "Engineering", "tag": "engineering" },
  { "name": "Financial Institutions", "tag": "financial" },
  { "name": "Food & Allied", "tag": "food" },
  { "name": "Fuel & Power", "tag": "fuel" },
  { "name": "General Insurance", "tag": "general" },
  { "name": "Life Insurance", "tag": "life" },
  { "name": "IT Sector", "tag": "it" },
  { "name": "Jute", "tag": "jute" },
  { "name": "Miscellaneous", "tag": "miscellaneous" },
  { "name": "Mutual Funds", "tag": "mutual" },
  { "name": "Paper & Printing", "tag": "paper" },
  { "name": "Pharmaceuticals & Chemicals", "tag": "pharmaceuticals" },
  { "name": "Services & Real Estate", "tag": "services" },
  { "name": "Tannery Industries", "tag": "tannery" },
  { "name": "Telecommunication", "tag": "telecommunication" },
  { "name": "Textile", "tag": "textile" },
  { "name": "Travel & Leisure", "tag": "travel" },
]

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

today = datetime.date.today()

query_date = {
    'weekly': calculate_query_date('weekly', today),
    'monthly': calculate_query_date('monthly', today),
    'sixMonthly': calculate_query_date('sixMonthly', today),
    'yearly': calculate_query_date('yearly', today),
    'fiveYearly': calculate_query_date('fiveYearly', today),
}

def basic_data_update(trading_code):    
    initialdata = mydb.daily_sectors.aggregate([
        {
            '$match': {
                'sector': trading_code,
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
                        '$group': {
                            '_id': None,
                            'high': { '$max': '$high' },
                            'low': { '$min': '$low' },
                            'totalVolume': { '$sum': '$volume' },
                            'totalValue': { '$sum': '$value' },
                            'totalTrade': { '$sum': '$trade' },
                        }
                    }
                ],
                'fiveYear': [
                    {
                        '$match': {
                            'date': {
                                '$gt': query_date['fiveYearly']
                            }
                        }
                    },
                    {
                        '$group': {
                            '_id': None,
                            'high': { '$max': '$high' },
                            'low': { '$min': '$low' },
                            'totalVolume': { '$sum': '$volume' },
                            'totalValue': { '$sum': '$value' },
                            'totalTrade': { '$sum': '$trade' },
                        }
                    }
                ],
                'oneYear': [
                    {
                        '$match': {
                            'date': {
                                '$gt': query_date['yearly']
                            }
                        }
                    },
                    {
                        '$group': {
                            '_id': None,
                            'high': { '$max': '$high' },
                            'low': { '$min': '$low' },
                            'totalVolume': { '$sum': '$volume' },
                            'totalValue': { '$sum': '$value' },
                            'totalTrade': { '$sum': '$trade' },
                        }
                    }
                ],
                'sixMonth': [
                    {
                        '$match': {
                            'date': {
                                '$gt': query_date['sixMonthly']
                            }
                        }
                    },
                    {
                        '$group': {
                            '_id': None,
                            'high': { '$max': '$high' },
                            'low': { '$min': '$low' },                             
                            'totalVolume': { '$sum': '$volume' },
                            'totalValue': { '$sum': '$value' },
                            'totalTrade': { '$sum': '$trade' },
                        }
                    }
                ],
                'oneMonth': [
                    {
                        '$match': {
                            'date': {
                                '$gt': query_date['monthly']
                            }
                        }
                    },
                    {
                        '$group': {
                            '_id': None,
                            'high': { '$max': '$high' },
                            'low': { '$min': '$low' },                            
                            'totalVolume': { '$sum': '$volume' },
                            'totalValue': { '$sum': '$value' },
                            'totalTrade': { '$sum': '$trade' },
                        }
                    }
                ],
                'oneWeek': [
                    {
                        '$match': {
                            'date': {
                                '$gt': query_date['weekly']
                            }
                        }
                    },
                    {
                        '$group': {
                            '_id': None,
                            'high': { '$max': '$high' },
                            'low': { '$min': '$low' },
                            'totalVolume': { '$sum': '$volume' },
                            'totalValue': { '$sum': '$value' },
                            'totalTrade': { '$sum': '$trade' },
                        }
                    }
                ]
            }
        }
    ]) 

    data = list(initialdata)[0]

    rawdata = data['rawData']

    check_element = [
        'weekly',
        'monthly',
        'sixMonthly',
        'yearly',
        'fiveYearly',
    ]
    before_data = {}

    for item in rawdata:
        if len(check_element) > 0:
            if item['date'] <= query_date[check_element[0]]:
                before_data[check_element[0]] = item['close'] if item['close'] != 0 else item['ycp']
                check_element.pop(0)
                
    fiveYearBeforeData = before_data['fiveYearly'] if 'fiveYearly' in before_data  else 0
    oneYearBeforeData = before_data['yearly'] if 'yearly' in before_data  else 0
    sixMonthBeforeData = before_data['sixMonthly'] if 'sixMonthly' in before_data  else 0
    oneMonthBeforeData = before_data['monthly'] if 'monthly' in before_data  else 0
    oneWeekBeforeData = before_data['weekly'] if 'weekly' in before_data  else 0

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

    newvalues = {
        'tradingCode': trading_code, 
        'date': datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),

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
    }
    # print(newvalues)

    mydb.yesterday_prices.insert_one(newvalues)

total_items = 0

for sector in sector_list:
    stock = sector['name']
    try:
        basic_data_update(stock)
        total_items += 1
        # print(stock, 'success') 

    except Exception as excp:
        print("Error: ", excp, ' : ', stock)
        mydb.data_script_errors.insert_one({
            'script': 'calc-sector-gain-lose-daily',
            'message': str(excp),
            'tradingCode': stock,
            'time': datetime.datetime.now()
        })

mydb.data_script_logs.insert_one({
    'script': 'calc-sector-gain-lose-daily',
    'message': f"Total items: {total_items}",
    'time': datetime.datetime.now()
})   
   