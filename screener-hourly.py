import pymongo, datetime, certifi
from variables import mongo_string
import math
# from data import stocks_list

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient["stockanalyst"]

data_setting = mydb.settings.find_one()

if data_setting['dataInsertionEnable'] == 0:
    print('exiting script')
    exit()

today_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

screener_scripts = mydb.screener_scripts.find({ 'date': today_date})

stocks_list = []
for item in screener_scripts:
  stocks_list.append(item['tradingCode'])

stocks_list = list(set(stocks_list))

colors = ['#00A25B', '#2962ff', '#f23645']

def calc_year_growth(data, year_count):
  curr_year = data[0]['year']
  curr_year_value = data[0]['value']
  
  prev_year = int(curr_year) - year_count
  prev_year_value = 0
  for item in data:
    if item['year'] == str(prev_year):
      prev_year_value = item['value']
      break
    
  if prev_year_value == 0 or prev_year_value == None:  
    return None
    
  yearly_growth = round(((((curr_year_value / prev_year_value) ** (1 / year_count)).real - 1) * 100), 2)
  return yearly_growth  

def format_yearly_data(init_data, title, unit='', percentChangeReverse=False):

  data_temp = sorted(init_data, key=lambda x: x['year'], reverse=True)
  
  data = list(filter(lambda x: x['value'] != None, data_temp))

  if len(data) == 0 : return None

  if len(data) == 1 : 
    return {
      'period': data[0]['year'],
      'value': data[0]['value'],
      'percentChange': None,
      'percentChangeFiveYear': None,
      'comment': None,
      'overview': None,
      'color': None,
    }
  
  unit = ' ' + unit if unit != '' else '' 
  
  if data[1]['value'] == 0:
    if data[0]['value'] == 0:
      percent_change = 0
    else :
      percent_change = 100  
  else:  
    percent_change = round(((data[0]['value'] - data[1]['value'] ) / abs(data[1]['value']) * 100), 2)
  
  percent_change_abs_value = str(abs(percent_change))
  
  comment = ''
  overview = title + ' for the year ' +  data[0]['year'] + ' was ' + str(data[0]['value']) + unit + '. ' + title
  
  if percent_change > 0:
    comment = percent_change_abs_value + '%' + ' incr over last year'
    overview += ' increased by ' + percent_change_abs_value + '%' + ' over last year (' + data[1]['year'] + ').'
    color = colors[0] if percentChangeReverse == False else colors[2]
  elif percent_change < 0:
    comment = percent_change_abs_value + '%' + ' decr from last year' 
    overview += ' decreased by ' + percent_change_abs_value + '%' + ' from last year (' + data[1]['year'] + ').'
    color = colors[2] if percentChangeReverse == False else colors[0]
  elif percent_change == 0:
    comment = 'No change from last year'
    overview += ' remains same as last year (' + data[1]['year'] + ').'
    color = colors[1]
  else:
    color = colors[1]
    
  five_year_growth = calc_year_growth(data, 5)
    
  return {
    'period': data[0]['year'],
    'value': data[0]['value'],
    'percentChange': percent_change,
    'percentChangeFiveYear': five_year_growth,
    'comment': comment,
    'overview': overview,
    'color': color,
  }

def format_yearly_data_basic(init_data):

  data_temp = sorted(init_data, key=lambda x: x['year'], reverse=True)
  
  data = list(filter(lambda x: x['value'] != None, data_temp))

  if len(data) == 0 : return None

  if len(data) == 1 : 
    return {
      'period': data[0]['year'],
      'value': data[0]['value'],
      'percentChange': None,
      'percentChangeFiveYear': None,
    }
  
  if data[1]['value'] == 0:
    if data[0]['value'] == 0:
      percent_change = 0
    else :
      percent_change = 100  
  else:  
    percent_change = round(((data[0]['value'] - data[1]['value'] ) / abs(data[1]['value']) * 100), 2)
  
  five_year_growth = calc_year_growth(data, 5)
  return {
    'period': data[0]['year'],
    'value': data[0]['value'],
    'percentChange': percent_change,
    'percentChangeFiveYear': five_year_growth,
  }
  
def format_quarterly_data(init_data, title, unit=''):
  data = sorted(init_data, key=lambda x: x['year'], reverse=True)

  if len(data) == 0 : return None

  q_current = sorted(data[0].items(), reverse=True)
  
  q_year = q_current[0][1]
  q_quarter = q_current[1][0]
  
  quarter_name = q_quarter.upper() + ' ' + str(q_year)
  
  q_value_this = q_current[1][1]

  if len(data) == 1 : 
    return {
    'period': quarter_name,
    'value': q_value_this,
    'percentChange': None,
    'comment': None,
    'overview': None,
    'color': None,
    }

  q_value_last = data[1][q_quarter] if q_quarter in data[1] else None
  
  if q_value_last == None:
    percent_change = None
  elif q_value_last == 0:
    percent_change = 100
  else:
    percent_change = round(((q_value_this - q_value_last) / abs(q_value_last) * 100), 2)

  percent_change_abs_value = str(abs(percent_change)) if percent_change else None
    
  unit = ' ' + unit if unit != '' else ''
  comment = ''
  overview = title + ' for ' +  quarter_name + ' was ' + str(q_value_this) + unit + '. ' + title
  
  if percent_change:
    if percent_change > 0:
      comment = percent_change_abs_value + '%' + ' qtr to qtr incr'
      overview += ' increased by ' + percent_change_abs_value + '%' + ' compared to same quarter of previous year'
      color = colors[0]
    elif percent_change < 0:
      comment = percent_change_abs_value + '%' + ' qtr to qtr decr'
      overview += ' decreased by ' + percent_change_abs_value + '%' + ' compared to same quarter of previous year'
      color = colors[2]
    elif percent_change == 0:
      comment = 'No qtr to qrt change'
      overview += ' remains unchanged compared to same quarter of previous year'
      color = colors[1]
  else:
    comment = 'Data not available'
    overview += ' data for same quarter of previous year is not available'
    color = colors[1]
    
  return {
    'period': quarter_name,
    'value': q_value_this,
    'percentChange': percent_change,
    'comment': comment,
    'overview': overview,
    'color': color,
  }
  
def format_eps_quarterly_data(init_data, ttmValue):
  data = sorted(init_data, key=lambda x: str(x['year']), reverse=True)
  q_current = sorted(data[0].items(), reverse=True)
  
  q_year = q_current[0][1]
  q_quarter = q_current[1][0]
  
  quarter_name = q_quarter.upper() + ' ' + str(q_year)
  
  q_value_this = q_current[1][1]
  q_value_last = data[1][q_quarter] if (len(data) > 1 and q_quarter in data[1]) else None
  
  if q_value_last == None:
    percent_change = None  
  else:
    percent_change = round(((q_value_this - q_value_last) / abs(q_value_last) * 100), 2)

  percent_change_abs_value = str(abs(percent_change)) if percent_change else None  
  
  comment = ''
  overview = '12 trailing month EPS is ' + str(ttmValue) + '. EPS for ' +  quarter_name + ' was ' + str(q_value_this) + '. EPS'
  
  if percent_change:
    if percent_change > 0:
      comment = percent_change_abs_value + '%' + ' qtr to qtr incr'
      overview += ' increased by ' + percent_change_abs_value + '%' + ' compared to same quarter of previous year'
      color = colors[0]
    elif percent_change < 0:
      comment = percent_change_abs_value + '%' + ' qtr to qtr decr'
      overview += ' decreased by ' + percent_change_abs_value + '%' + ' compared to same quarter of previous year'
      color = colors[2]
    elif percent_change == 0:
      comment = 'No qtr to qrt change'
      overview += ' remains unchanged compared to same quarter of previous year'
      color = colors[1]
  else:
    comment = 'Data not available'
    overview += ' data for same quarter of previous year is not available'
    color = colors[1]    
    
  return {
    'quarter': quarter_name,
    'quarterValue': q_value_this,
    'period': 'Audited' if len(q_current) == 5 else 'TTM',
    'value': ttmValue,
    'percentChange': percent_change,
    'comment': comment,
    'overview': overview,
    'color': color,
    
  }
  
def format_dividend_data(cash_div_raw_data, stock_div_raw_data):

  cash_div_data = sorted(cash_div_raw_data, key=lambda x: x['year'], reverse=True)
  stock_div_data = sorted(stock_div_raw_data, key=lambda x: x['year'], reverse=True)
    
  cash_dividend = cash_div_data[0] if len(cash_div_data) > 0 else { 'year': '1999', 'value': 0}
  stock_dividend = stock_div_data[0] if len(stock_div_data) > 0 else { 'year': '1999', 'value': 0}
  
  data = {}
  if cash_dividend['year'] == stock_dividend['year'] :
    data = {
      'year': cash_dividend['year'],
      'cash': cash_dividend['value'],
      'stock': stock_dividend['value']
    }
  elif cash_dividend['year'] > stock_dividend['year'] :
     data = {
      'year': cash_dividend['year'],
      'cash': cash_dividend['value'],
      'stock': 0
    }
  elif cash_dividend['year'] < stock_dividend['year'] :
    data = {
      'year': stock_dividend['year'],
      'cash': 0,
      'stock': stock_dividend['value']
    }
    
  year_list_temp = []
  for elem in cash_div_data:
    year_list_temp.append(elem['year'])
  for elem in stock_div_data:
    year_list_temp.append(elem['year'])
    
  year_list = sorted(list(set(year_list_temp)), key=lambda x: x) 
  
  total_div_data = []
  for year in year_list:
    cash_temp = [element for element in cash_div_data if element['year'] == year]
    stock_temp = [element for element in stock_div_data if element['year'] == year]
      
    total_div_data.append({
      'year': year,
      'cash': cash_temp[0]['value'] if len(cash_temp) > 0 else 0,
      'stock': stock_temp[0]['value'] if len(stock_temp) > 0 else 0
    })  
    
  data['data'] = total_div_data
  
  return data  

def format_dividend_payout_ratio(cash_div_raw_data, eps_yearly_raw_data, face_value, title):
  cash_div_data = sorted(cash_div_raw_data, key=lambda x: x['year'])
  eps_yearly_data = sorted(eps_yearly_raw_data, key=lambda x: x['year'])
  
  data = []
  for i in range(len(eps_yearly_data)):
    year = eps_yearly_data[i]['year']
    eps_value = eps_yearly_data[i]['value']
    
    cash_div_value = 0
    for i in range(len(cash_div_data)):
      if cash_div_data[i]['year'] == year:
        cash_div_value = cash_div_data[i]['value']
    
    if cash_div_value == 0:
      dividend_payout_ratio = 0
    else:
      dividend_payout_ratio = round((cash_div_value * 100 / (face_value * eps_value)), 3) if eps_value != 0 else 0 
      
    data.append({
      'year': year,
      'value': dividend_payout_ratio
      })  

  if len(data) < 2: return None  
  
  if data[-2]['value'] == 0:
    if data[-1]['value'] == 0:
      percent_change = 0
    else :
      percent_change = 100  
  else:  
    percent_change = round(((data[-1]['value'] - data[1]['value'] ) / data[-2]['value'] * 100), 2)
  
  percent_change_abs_value = str(abs(percent_change))
  
  comment = ''
  overview = title + ' for the year ' +  data[-1]['year'] + ' was ' + str(data[-1]['value']) + '. ' + title
  
  if percent_change > 0:
    comment = percent_change_abs_value + '%' + ' incr over last year'
    overview += ' increased by ' + percent_change_abs_value + '%' + ' over last year (' + data[-2]['year'] + ').'
    color = colors[0]
  elif percent_change < 0:
    comment = percent_change_abs_value + '%' + ' decr from last year' 
    overview += ' decreased by ' + percent_change_abs_value + '%' + ' from last year (' + data[-2]['year'] + ').'
    color = colors[2]
  elif percent_change == 0:
    comment = 'Same as last year'
    overview += ' remains same as last year (' + data[-2]['year'] + ').'
    color = colors[1]  
    
  return {
    'period': data[-1]['year'],
    'value': data[-1]['value'],
    'percentChange': percent_change,
    'comment': comment,
    'overview': overview,
    'color': color,
    'data': data,
  }  

def format_ps_data(trading_code, sector, revenue_init_data, market_cap):

  revenue_data = sorted(revenue_init_data, key=lambda x: x['year'])

  data = []
  for i in range(len(revenue_data)):
    year = revenue_data[i]['year']

    ps_value = round((market_cap * 1000000 / revenue_data[i]['value']), 3) if revenue_data[i]['value'] != None else None
    data.append({
      'year': year,
      'value': ps_value
    })  
    
  ps_sector_data = mydb.fundamentals.aggregate([
    {
      '$match': {
        'sector': sector
      }
    },
    {
      '$project': {
        '_id': 0,
        'tradingCode': 1,
        'ps': { 
          '$round': [ 
            { 
              '$divide': [ 
                { 
                  '$multiply': [ '$marketCap', 1000000 ] 
                }, 
                { '$last': '$revenue.value' } 
              ] 
            }, 
            3 
          ]  
        },
        'year': { '$last': '$revenue.year' }
      }
    },
    {
      '$sort': {
        'ps': 1
      }
    }
  ])
  
  index = 0
  index_matched = -1
  sector_data_list = []
  
  for item in ps_sector_data:
    sector_data_list.append(item['ps'])
    if item['tradingCode'] == trading_code:
      index_matched = index + 1
    index += 1  
  
  median = math.floor(index / 2)   
        
  position = ''
  textColor = ''
  
  if index_matched < median:
    textColor = colors[0]
  elif index_matched == median:
    textColor = colors[1]
  if index_matched > median:
    textColor = colors[2]

  if index_matched == 1:
    position = '1st'  
  elif index_matched == 2:
    position = '2nd'  
  elif index_matched == 3:
    position = '3rd'  
  elif index_matched > 3:
    position = str(index_matched) + 'th'  
    
  comment = position + ' in sector(out of ' + str(index)  + ')'   
  overview = 'P/S ratio of ' + trading_code + ' is at ' + position + ' position in sector where total number of stocks in sector is ' + str(index)
  
  return {
    'period': data[-1]['year'],
    'value': data[-1]['value'],
    'comment': comment,
    'overview': overview,
    'color': textColor,
    'position': index_matched,
    'min': 1,
    'max': index,
    # 'min': sector_data_list[0],
    # 'max': sector_data_list[-1],
    'data': data,
  } 
  
def format_shareholding(shareholding):

  if shareholding[-2]['institute'] == 0:
    if shareholding[-1]['institute'] == 0:
      percent_change_inst = 0
    else :
      percent_change_inst = 100  
  else:  
    percent_change_inst = round(((shareholding[-1]['institute'] - shareholding[-2]['institute'] ) / shareholding[-2]['institute'] * 100), 2)
    
  if shareholding[-2]['director'] == 0:
    if shareholding[-1]['director'] == 0:
      percent_change_dir = 0
    else :
      percent_change_dir = 100  
  else:  
    percent_change_dir = round(((shareholding[-1]['director'] - shareholding[-2]['director'] ) / shareholding[-2]['director'] * 100), 2)
    
  return {
    'current': shareholding[-1],
    'percentChange': {
      'institute': percent_change_inst,
      'director': percent_change_dir,
    }
  }

def format_reserve(reserve):
  data_length = len(reserve)

  if data_length == 0:
    return None
  elif data_length == 1:
    return {
      'period': reserve[0]['date'][-4:],
      'value': reserve[0]['value'],
      'percentChange': None,
      'comment': "--",
      'overview': 'Reserve and Surplus for the year ' +  reserve[0]['date'][-4:] + ' was ' + str(round(reserve[0]['value']/10, 2)) + ' crore BDT',
      'color': colors[1],
    } 
  elif data_length >= 2:

    if reserve[-2]['value'] == 0:
      if reserve[-1]['value'] == 0:
        percent_change = 0
      else :
        percent_change = 100  
    else:  
      percent_change = round(((reserve[-1]['value'] - reserve[-2]['value'] ) / abs(reserve[-2]['value']) * 100), 2)
      
    percent_change_abs_value = str(abs(percent_change))

    reserve_year = reserve[-1]['date'][-4:]
    reserve_value = round((reserve[-1]['value']/10), 2)

    comment = ''
    overview = 'Reserve and Surplus for the year ' +  reserve_year + ' was ' + str(reserve_value) + ' crore BDT'

    if percent_change > 0:
      comment = percent_change_abs_value + '%' + ' incr over last year'
      overview += 'Reserve and Surplus increased by ' + percent_change_abs_value + '%' + ' over last year (' + reserve_year + ').'
      color = colors[0] 
    elif percent_change < 0:
      comment = percent_change_abs_value + '%' + ' decr from last year' 
      overview += 'Reserve and Surplus decreased by ' + percent_change_abs_value + '%' + ' from last year (' + reserve_year + ').'
      color = colors[2]
    elif percent_change == 0:
      comment = 'No change from last year'
      overview += ' remains same as last year (' + reserve_year + ').'
      color = colors[1]
    else:
      color = colors[1]

    return {
      'period': reserve_year,
      'value': reserve_value,
      'percentChange': percent_change,
      'comment': comment,
      'overview': overview,
      'color': color,
    }

def data_calc(trading_code):
  rawdata = mydb.fundamentals.find_one({ 'tradingCode': trading_code })

  data = {}
  
  data['ps'] = format_ps_data(trading_code, rawdata['sector'], rawdata['revenue'], rawdata['marketCap']) if 'revenue' in rawdata else None
       
  data['shareholding'] = format_shareholding(rawdata['shareHoldingPercentage']) if 'shareHoldingPercentage' in rawdata else None

  data['reserveSurplus'] = format_reserve(rawdata['reserveSurplus']) if 'reserveSurplus' in rawdata else None
      
  data['epsYearly'] = format_yearly_data_basic(rawdata['epsYearly']) if 'epsYearly' in rawdata and len(rawdata['epsYearly']) > 0 else None 
  data['navYearly'] = format_yearly_data_basic(rawdata['navYearly']) if 'navYearly' in rawdata and len(rawdata['navYearly']) > 0 else None 
  data['nocfpsYearly'] = format_yearly_data_basic(rawdata['nocfpsYearly']) if 'nocfpsYearly' in rawdata and len(rawdata['nocfpsYearly']) > 0 else None 
  data['bookValue'] = format_yearly_data_basic(rawdata['bookValue']) if 'bookValue' in rawdata else None 
  data['totalLiabilities'] = format_yearly_data_basic(rawdata['totalLiabilities']) if 'totalLiabilities' in rawdata else None
  data['ebit'] = format_yearly_data_basic(rawdata['ebit']) if 'ebit' in rawdata else None
  
  data['revenue'] = format_yearly_data(rawdata['revenue'], 'Revenue', 'BDT') if 'revenue' in rawdata else None
  data['roe'] = format_yearly_data(rawdata['roe'], 'ROE') if 'roe' in rawdata else None
  data['roce'] = format_yearly_data(rawdata['roce'], 'ROCE') if 'roce' in rawdata else None 
  data['roa'] = format_yearly_data(rawdata['roa'], 'ROA') if 'roa' in rawdata else None    
  data['currentRatio'] = format_yearly_data(rawdata['currentRatio'], 'Current Ratio') if 'currentRatio' in rawdata else None 
  data['netIncomeRatio'] = format_yearly_data(rawdata['netIncomeRatio'], 'Net Income Ratio') if 'netIncomeRatio' in rawdata else None 
  data['netIncome'] = format_yearly_data(rawdata['netIncome'], 'Net Income') if 'netIncome' in rawdata else None 
  data['operatingProfit'] = format_yearly_data(rawdata['operatingProfit'], 'Operating Profit') if 'operatingProfit' in rawdata else None 
  data['de'] = format_yearly_data(rawdata['de'], 'D/E ratio', '', True) if 'de' in rawdata else None 
  data['profitMargin'] = format_yearly_data(rawdata['profitMargin'], 'Profit Margin') if 'profitMargin' in rawdata else None 
  data['totalAsset'] = format_yearly_data(rawdata['totalAsset'], 'Total Asset') if 'totalAsset' in rawdata else None 
  data['dividendYield'] = format_yearly_data(rawdata['dividendYield'], 'Dividend Yield') if 'dividendYield' in rawdata else None 
  
  data['navQuarterly'] = format_quarterly_data(rawdata['navQuaterly'], 'NAV') if 'navQuaterly' in rawdata and len(rawdata['navQuaterly']) > 0 else None
  data['nocfpsQuarterly'] = format_quarterly_data(rawdata['nocfpsQuaterly'], 'NOCFPS') if 'nocfpsQuaterly' in rawdata and len(rawdata['nocfpsQuaterly']) > 0 else None
  
  data['epsQuarterly'] = format_eps_quarterly_data(rawdata['epsQuaterly'], rawdata['epsCurrent']) if 'epsQuaterly' in rawdata and len(rawdata['epsQuaterly']) > 0 else None
  
  data['dividend'] = format_dividend_data(rawdata['cashDividend'], rawdata['stockDividend']) if ('cashDividend' in rawdata and 'stockDividend' in rawdata) else None
  
  data['dividendPayoutRatio'] = format_dividend_payout_ratio(rawdata['cashDividend'], rawdata['epsYearly'], rawdata['faceValue'], 'Dividend payout ratio') if 'epsYearly' in rawdata and len(rawdata['epsYearly']) > 0 else None 
    
  mydb.fundamentals.update_one({ 'tradingCode': trading_code }, { "$set": { "screener": data } })
    
success_items = []
error_items = []    

for stock_code in stocks_list:
  try:
    data_calc(stock_code)
    # print(stock_code, "Success")
    success_items.append(stock_code)
  except:
    # print(stock_code, "Error")
    error_items.append(stock_code)

mydb.screener_scripts.delete_many({ 'date': today_date, 'tradingCode': { '$in': success_items } })

# print("Success: ", success_items)
# print("Error: ", error_items)

  