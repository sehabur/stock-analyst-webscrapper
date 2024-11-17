import pymongo, datetime, certifi, requests, re
from bs4 import BeautifulSoup
from pytz import timezone
from variables import backend_url_dev, backend_url_prod, mongo_string, db_name

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient[db_name]

data_setting = mydb.settings.find_one()

if data_setting['dataInsertionEnable'] == 0:
    print('exiting script')
    exit()

# date = datetime.date(2024, 10, 11).strftime("%Y-%m-%d")
date = datetime.date.today().strftime("%Y-%m-%d")
stock_url  = 'https://www.dsebd.org/old_news.php?startDate=' + date + '&endDate=' + date + '&criteria=4&archive=news'

response = requests.get(stock_url)
soup = BeautifulSoup(response.text, 'html.parser')

news_data_array = soup.find('table', attrs={'class':'table-news'})

table_data = []
for row in news_data_array.find_all('td')[0:]:
  table_data.append(row.text.strip())

x = 0
news_data = []
for y in range (int(len(table_data)/4)):
  news_data.append ({
    "tradingCode": table_data[x] ,
    "title": table_data[x+1],
    "description": table_data[x+2],
    "date": datetime.datetime.strptime(table_data[x+3], "%Y-%m-%d"),
    "time": datetime.datetime.now(timezone("Asia/Dhaka")).replace(second=0, microsecond=0), 
    })
  x = x + 4

today_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

today_news_temp = mydb.news.find({ "date": today_date }, {'tradingCode': 1, 'title': 1, "_id": 0 })  

today_news_title = []
for news in today_news_temp:
  today_news_title.append(news['title'])

news_to_insert = []
screener_news_script_array = []

for item in news_data:
  if item['title'] not in today_news_title:

    news_to_insert.append(item)

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

if len(news_to_insert) > 0:
  mydb.news.insert_many(news_to_insert)

if len(screener_news_script_array) > 0:
  mydb.screener_scripts.insert_many(screener_news_script_array)

# mydb.data_script_logs.insert_one({
#     'script': 'news-hourly',
#     'message': f"Total news inserted: {len(news_to_insert)}",
#     'time': datetime.datetime.now()
# })

server = backend_url_prod
url = server + "/api/users/scheduleNewsAlert"

keys_to_keep = ["tradingCode", "title", "description"]
payload_new_list = [{k: obj[k] for k in keys_to_keep if k in obj} for obj in news_to_insert]

response = requests.post(url, json={ "news": news_to_insert })

if response.status_code == 200:
    print('Success')
else:
    print("Fail")