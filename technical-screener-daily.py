import pymongo, datetime, certifi
from variables import mongo_string
from data import stocks_list
import pandas as pd
from scipy.stats import linregress

from technical import calculate_sma, calculate_ema, calculate_rsi, detect_double_top, detect_double_bottom, detect_head_and_shoulders, detect_inverse_head_and_shoulders, detect_channel_up, detect_channel_down, detect_ascending_triangle, detect_descending_triangle, detect_candlestick_patterns, calculate_adx, calculate_stochastic_k, calculate_macd, calculate_williams_percent_r, calculate_money_flow_index, calculate_pivot_points

# stocks_list = ['PHENIXINS', 'YPL', 'GP', 'RSRMSTEEL', 'EHL']
# stocks_list = ['DBH']

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient["stockanalyst"]

data_setting = mydb.settings.find_one()

if data_setting['dataInsertionEnable'] == 0:
    print('exiting script')
    exit()

def calculate_beta(trading_code):
    query_start_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=365)

    stock_prices_cursor = mydb.daily_prices.aggregate([
      {
        '$addFields': {
          'ltp': {
            '$cond': [{ '$gt': ["$ltp", 0] }, "$ltp", "$ycp"],
          },
        },
      },
      {
        '$match': {
          'tradingCode': trading_code,
          'date': {
            '$gt': query_start_date,
          },
        },
      },
      {
        '$sort': {
          'date': -1,
        },
      },
      {
        '$project': { 'date': 1, 'ltp': 1 },
      },
    ])

    stock_prices = list(stock_prices_cursor)
    stock_df = pd.DataFrame(stock_prices)

    market_prices_cursor = mydb.daily_prices.aggregate([
      {
      '$match': {
        'tradingCode': '00DS30',
        'date': {
          '$gt': query_start_date,
        },
      },
      },
      {
        '$sort': {
          'date': -1,
        },
      },
      {
        '$project': { 'date': 1, 'ltp': 1 },
      },            
    ])

    market_prices = list(market_prices_cursor)
    market_df = pd.DataFrame(market_prices)
    
    # Calculate daily returns
    stock_returns = stock_df['ltp'].pct_change().dropna()
    benchmark_returns = market_df['ltp'].pct_change().dropna()
    
    # Align the data by date
    returns_data = pd.concat([stock_returns, benchmark_returns], axis=1).dropna()
    returns_data.columns = ['Stock', 'Benchmark']
    
    # Calculate the slope (beta) using linear regression
    slope, intercept, r_value, p_value, std_err = linregress(returns_data['Benchmark'], returns_data['Stock'])
    
    return round(slope, 2)

def get_one_year_prices(trading_code):

  daily_price = mydb.daily_prices.aggregate([
    {
      '$match': {
        'tradingCode': trading_code,
      },
    },
    {
      '$sort': {
        'date': -1,
      },
    },
    {
      '$limit': 320,
    },
    {
      '$sort': {
        'date': 1,
      },
    },
    {
      '$project': {
        'date': 1,
        'open': 1,
        'high': 1,
        'low': 1,
        'ltp': 1,
        'ycp': 1,
        'volume': 1,
      },
    },
  ])

  dates = []
  prices = []
  opens = []
  lows = []
  highs = []
  volumes = []

  for item in daily_price:
    dates.append(item['date'])
    prices.append(item['ltp'] if item['ltp'] != 0 else item['ycp'])
    opens.append(item['open'] if item['open'] != 0 else item['ycp'])
    lows.append(item['low'] if item['low'] != 0 else item['ycp'])
    highs.append(item['high'] if item['high'] != 0 else item['ycp'])
    volumes.append(item['volume'])

  return {
    'dates': dates,
    'prices': prices,
    'opens': opens,
    'lows': lows,
    'highs': highs,
    'volumes': volumes,
  }  

def get_one_year_candles(trading_code):
  daily_price = mydb.daily_prices.aggregate([
    {
      '$match': {
        'tradingCode': trading_code,
      },
    },
    {
      '$sort': {
        'date': -1,
      },
    },
    {
      '$limit': 500,
    },
    {
      '$sort': {
        'date': 1,
      },
    },
    {
      '$addFields': {
        'close': {
          '$cond': [{ '$gt': ['$close', 0] }, '$close', '$ycp']
        },
        'high': {
          '$cond': [{ '$gt': ['$high', 0] }, '$high', '$ycp']
        },
        'low': {
          '$cond': [{ '$gt': ['$low', 0] }, '$low', '$ycp']
        }
      }
    },
    {
      '$project': {
        'date': 1,
        'open': 1,
        'high': 1,
        'low': 1,
        'ltp': 1,
        'close': 1,
        'ycp': 1,
        'volume': 1,
      },
    },
  ])

  return list(daily_price)

def format_sma_ema(prices):
  sma10 = calculate_sma(prices, 10)
  sma20 = calculate_sma(prices, 20)
  sma30 = calculate_sma(prices, 30)
  sma50 = calculate_sma(prices, 50)
  sma100 = calculate_sma(prices, 100)
  sma200 = calculate_sma(prices, 200)

  ema10 = calculate_ema(prices, 10)
  ema20 = calculate_ema(prices, 20)
  ema30 = calculate_ema(prices, 30)
  ema50 = calculate_ema(prices, 50)
  ema100 = calculate_ema(prices, 100)
  ema200 = calculate_ema(prices, 200)

  return {
    'sma10': sma10,
    'sma20': sma20,
    'sma30': sma30,
    'sma50': sma50,
    'sma100': sma100,
    'sma200': sma200,
    'ema10': ema10,
    'ema20': ema20,
    'ema30': ema30,
    'ema50': ema50,
    'ema100': ema100,
    'ema200': ema200,

  }

def format_oscillators(prices, opens, highs, lows, volumes, one_year_candles):
  rsi = calculate_rsi(prices)
  adx = calculate_adx(highs, lows, prices)
  stoch = calculate_stochastic_k(one_year_candles)
  macd = calculate_macd(prices)
  williamR = calculate_williams_percent_r(highs, lows, prices)
  mfi = calculate_money_flow_index(highs, lows, prices, volumes)

  return {
    'rsi': rsi,
    'adx': adx,
    'stoch': stoch,
    'macd': macd,
    'williamR': williamR,
    'mfi': mfi
  }

def format_patterns(prices): 
  try:
    double_top_patterns = detect_double_top(prices)

    double_bottom_patterns = detect_double_bottom(prices)

    head_and_shoulders_patterns = detect_head_and_shoulders(prices)

    inverse_head_and_shoulders_patterns = detect_inverse_head_and_shoulders(prices)

    channel_up_patterns = detect_channel_up(prices)

    channel_down_patterns = detect_channel_down(prices)

    ascending_triangle_patterns = detect_ascending_triangle(prices)

    descending_triangle_patterns = detect_descending_triangle(prices)

    patterns = []

    if len(double_top_patterns) > 0:
      patterns.append('double_top')

    if len(double_bottom_patterns) > 0:
      patterns.append('double_bottom')

    if len(head_and_shoulders_patterns) > 0:
      patterns.append('head_and_shoulders')

    if len(inverse_head_and_shoulders_patterns) > 0:
      patterns.append('inverse_head_and_shoulders')

    if len(channel_up_patterns) > 0:
      patterns.append('channel_up')

    if len(channel_down_patterns) > 0:
      patterns.append('channel_down')

    if len(ascending_triangle_patterns) > 0:
      patterns.append('ascending_triangle')

    if len(descending_triangle_patterns) > 0:
      patterns.append('descending_triangle')

    return patterns
  
  except:
    return []

def format_candlestick(one_year_prices):
  candlestick_period = 3

  candle_data = {
    'Date': one_year_prices['dates'][-candlestick_period:],
    'Open': one_year_prices['opens'][-candlestick_period:],
    'High': one_year_prices['highs'][-candlestick_period:],
    'Low': one_year_prices['lows'][-candlestick_period:],
    'Close': one_year_prices['prices'][-candlestick_period:]
  }

  df = pd.DataFrame(candle_data)
  patterns = detect_candlestick_patterns(df)

  candlestick = []

  for pattern in patterns:
    candlestick.append({
      'date': pattern[0],
      'value': pattern[1],
    })

  return candlestick

def data_calc(trading_code):
  print(trading_code)
  one_year_prices = get_one_year_prices(trading_code)
  one_year_candles = get_one_year_candles(trading_code)

  prices = one_year_prices['prices']
  opens = one_year_prices['opens']
  highs = one_year_prices['highs']
  lows = one_year_prices['lows']
  volumes = one_year_prices['volumes']

  data = {}

  data['beta'] = calculate_beta(trading_code)

  data['movingAverages'] = format_sma_ema(prices)

  data['oscillators'] = format_oscillators(prices, opens, highs, lows, volumes, one_year_candles)

  data['patterns'] = format_patterns(prices)

  data['candlestick'] = format_candlestick(one_year_prices)

  data['pivots'] = calculate_pivot_points(highs[-1], lows[-1], prices[-1])

  print(data)
                                                            
  mydb.fundamentals.update_one({ 'tradingCode': trading_code }, { "$set": { "technicals": data } })

# success_items = []
# error_items = []    
total_shares = 0

for stock_code in stocks_list:
  # data_calc(stock_code)
  try:
    data_calc(stock_code)
    total_shares += 1
    # print(stock_code, "Success")
    # success_items.append(stock_code)
  except Exception as excp:
    mydb.data_script_errors.insert_one({
      'script': 'technical-screener-daily',
      'message': str(excp),
      'tradingCode': stock_code,
      'time': datetime.datetime.now()
    })
    # print(stock_code, "Error")
    # error_items.append(stock_code)

mydb.data_script_logs.insert_one({
    'script': 'technical-screener-daily',
    'message': f"Total stocks: {total_shares}",
    'time': datetime.datetime.now()
})


  