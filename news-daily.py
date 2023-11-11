import pymongo, datetime, certifi, requests
from bs4 import BeautifulSoup
from variables import mongo_string

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

data = []
table_data = []
for row in news_data_array.find_all('td')[0:]:
  table_data.append(row.text.strip())

x=0
for y in range (int(len(table_data)/4)):
  data.append ({
    'tradingCode': table_data[x] ,
    'title': table_data[x+1],
    'description': table_data[x+2],
    'date': datetime.datetime.strptime(table_data[x+3], '%Y-%m-%d'),
    })
  x=x+4

mydb.news.insert_many(data)