import pymongo, datetime, certifi, requests
from bs4 import BeautifulSoup
from variables import mongo_string
from data import stocks_list

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient["stockanalyst"]

data_setting = mydb.settings.find_one()

if data_setting['dataInsertionEnable'] == 0:
    print('exiting script')
    exit()

def shareholding_data(stock_code):
    stock_url  = 'https://www.dsebd.org/displayCompany.php?name='+ stock_code
    response = requests.get(stock_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    page_data_array = soup.find_all('table', attrs={'class': 'table table-bordered background-white'})

    table_data = []
    for row in page_data_array[9].find_all('td')[0:]:
        table_data.append(row.text.strip())

    shareHoldings = {
        'date': table_data[20].split("\r\n")[1].strip('[as on]'),
        'director': float(table_data[22].split("\r\n")[1].strip()),
        'govt': float(table_data[23].split("\r\n")[1].strip()),
        'institute': float(table_data[24].split("\r\n")[1].strip()),
        'foreign': float(table_data[25].split("\r\n")[1].strip()),
        'public': float(table_data[26].split("\r\n")[1].strip()),
    }
    
    old_data = mydb.fundamentals.find_one({ 'tradingCode': stock_code })
    length = len(old_data['shareHoldingPercentage'])

    old_date = old_data['shareHoldingPercentage'][length-1]['date']
    new_date = shareHoldings['date']

    if old_date != new_date:
        mydb.fundamentals.update_one({ 'tradingCode': stock_code }, { '$push': { 'shareHoldingPercentage': shareHoldings } })
        print(stock_code, 'success')
    else:
        print(stock_code, 'data already exists')

for stock in stocks_list:
    shareholding_data(stock)