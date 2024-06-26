import pymongo, datetime, certifi, requests, re
from bs4 import BeautifulSoup
from variables import mongo_string
from pytz import timezone

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient["stockanalyst"]

data_setting = mydb.settings.find_one()

if data_setting['dataInsertionEnable'] == 0:
    print('exiting script')
    exit()

date = datetime.date.today().strftime("%Y-%m-%d")
stock_url  = 'https://www.dsebd.org/old_news.php?startDate='+date+'&endDate='+date+'&criteria=4&archive=news'

response = requests.get(stock_url)
soup = BeautifulSoup(response.text, 'html.parser')

news_data_array = soup.find('table', attrs={'class':'table-news'})

table_data = []
for row in news_data_array.find_all('td')[0:]:
  table_data.append(row.text.strip())

x = 0
news_data = []
test = []
for y in range (int(len(table_data)/4)):
  news_data.append ({
    'tradingCode': table_data[x] ,
    'title': table_data[x+1],
    'description': table_data[x+2],
    'date': datetime.datetime.strptime(table_data[x+3], '%Y-%m-%d'),
    'time': datetime.datetime.now(timezone('Asia/Dhaka')).replace(second=0, microsecond=0), 
    })
  test.append(table_data[x+1])
  x = x + 4

today_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

today_news_temp = mydb.news.find({ "date": today_date }, {'tradingCode': 1, 'title': 1, "_id": 0 })  

today_news_title = []
for news in today_news_temp:
  today_news_title.append(news['title'])

screener_news_script_array = []

for item in news_data:
  if item['title'] not in today_news_title:

    mydb.news.insert_one(item)

    q_items = re.search(r'Financials', item['title'], re.IGNORECASE)

    y_items = re.search(r'Dividend Declaration$', item['title'], re.IGNORECASE)

    if q_items :
      screener_news_script_array.append({
        'tradingCode': item['tradingCode'],
        'date': item['date'],
        'title': item['title'],
        'script': 'quarterly',

      })
    elif y_items :
      screener_news_script_array.append({
        'tradingCode': item['tradingCode'],
        'date': item['date'],
        'title': item['title'],
        'script': 'yearly'
      })

    print("Data insertion successful -> ", item)
  else:
    print('news already inserted')  

if len(screener_news_script_array) > 0:
  mydb.screener_scripts.insert_many(screener_news_script_array)
