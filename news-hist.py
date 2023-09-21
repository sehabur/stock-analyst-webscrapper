import requests
from bs4 import BeautifulSoup
import pymongo, datetime
from pytz import timezone
from variables import mongo_string

# startDate = '2021-09-15'
startDate = '2023-07-10'
endDate = '2023-07-13'

stock_url = 'https://www.dsebd.org/old_news.php?startDate='+startDate+'&endDate='+endDate+'&criteria=4&archive=news'

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

myclient = pymongo.MongoClient(mongo_string)
mydb = myclient["stockAnalyst"]
mycol = mydb["news"]

mycol.insert_many(data)