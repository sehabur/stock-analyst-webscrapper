import pymongo, datetime, certifi, requests
from bs4 import BeautifulSoup
from variables import mongo_string
from data import stocks_list

# stocks_list = ['MARICO']

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient["stockanalyst"]

def shareholding_data(stock_code):
    stock_url  = 'https://www.dsebd.org/displayCompany.php?name='+ stock_code
    response = requests.get(stock_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    page_data_array = soup.find_all('table', attrs={'class': 'table table-bordered background-white'})

    table_data = []
    for row in page_data_array[9].find_all('td')[0:]:
        table_data.append(row.text.strip())

    shareHoldings = [
        {
            'date': table_data[6].split("\r\n")[1].strip('[as on (year ended)]'),
            'director': float(table_data[8].split("\r\n")[1].strip()),
            'govt': float(table_data[9].split("\r\n")[1].strip()),
            'institute': float(table_data[10].split("\r\n")[1].strip()),
            'foreign': float(table_data[11].split("\r\n")[1].strip()),
            'public': float(table_data[12].split("\r\n")[1].strip()),          
        },
        {
            'date': table_data[13].split("\r\n")[1].strip('[as on]'),
            'director': float(table_data[15].split("\r\n")[1].strip()),
            'govt': float(table_data[16].split("\r\n")[1].strip()),
            'institute': float(table_data[17].split("\r\n")[1].strip()),
            'foreign': float(table_data[18].split("\r\n")[1].strip()),
            'public': float(table_data[19].split("\r\n")[1].strip()),
        },
        {
            'date': table_data[20].split("\r\n")[1].strip('[as on]'),
            'director': float(table_data[22].split("\r\n")[1].strip()),
            'govt': float(table_data[23].split("\r\n")[1].strip()),
            'institute': float(table_data[24].split("\r\n")[1].strip()),
            'foreign': float(table_data[25].split("\r\n")[1].strip()),
            'public': float(table_data[26].split("\r\n")[1].strip()),
        }
    ]
    
    mydb.fundamentals.update_one({ 'tradingCode': stock_code }, { '$set': { 'shareHoldingPercentage': shareHoldings } })
    print(stock_code, 'success')

for stock in stocks_list:
    shareholding_data(stock)