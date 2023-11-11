import requests, datetime, pymongo, certifi
from bs4 import BeautifulSoup
from variables import mongo_string

startDate = '2021-09-06'
# startDate = '2023-01-01'
endDate = '2022-12-31'

stock_url  = 'https://www.dsebd.org/market_summary.php?startDate='+startDate+'&endDate='+endDate+'&archive=data'
response = requests.get(stock_url)
soup = BeautifulSoup(response.text, 'html.parser')
data_array = soup.find_all('table', attrs={'table table-bordered table-striped background-white'})

data=[]

for x in range(len(data_array)):
    table_data = []
    for row in data_array[x].find_all('td')[0:]:
        table_data.append(row.text)
    data.append({
      'date': datetime.datetime.strptime(table_data[0].replace("Market Summary of ", ''), '%b %d, %Y'),
      'dsex': { 'index': float(table_data[2].replace(",", '')) },
      'dse30': { 'index': float(table_data[10].replace(",", '')) } ,
    })

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient["stockanalyst"]

mydb.index_daily_values.insert_many(data)
  