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

# stocks_list = ['BESTHLDNG', 'NRBBANK', 'SICL']

def shareholding_data(stock_code):
    stock_url  = 'https://www.dsebd.org/displayCompany.php?name='+ stock_code
    response = requests.get(stock_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    page_data_array = soup.find_all('table', attrs={'class': 'table table-bordered background-white'})

    table_data = []
    for row in page_data_array[9].find_all('td')[0:]:
        table_data.append(row.text.strip())


    # SET CATEGORY #
    category = table_data[3]    
    
    mydb.fundamentals.update_one({ 'tradingCode': stock_code }, { '$set': { 'category': category } })

    # SET SHAREHOLDING #
    if 'Share Holding Percentage' in table_data[20].split("\r\n")[0]: 
        shareHoldings = {
            'date': table_data[20].split("\r\n")[1].strip('[as on]'),
            'director': float(table_data[22].split("\r\n")[1].strip()),
            'govt': float(table_data[23].split("\r\n")[1].strip()),
            'institute': float(table_data[24].split("\r\n")[1].strip()),
            'foreign': float(table_data[25].split("\r\n")[1].strip()),
            'public': float(table_data[26].split("\r\n")[1].strip()),
        }
    elif 'Share Holding Percentage' in table_data[13].split("\r\n")[0]:        
        shareHoldings = {
            'date': table_data[13].split("\r\n")[1].strip('[as on]'),
            'director': float(table_data[15].split("\r\n")[1].strip()),
            'govt': float(table_data[16].split("\r\n")[1].strip()),
            'institute': float(table_data[17].split("\r\n")[1].strip()),
            'foreign': float(table_data[18].split("\r\n")[1].strip()),
            'public': float(table_data[19].split("\r\n")[1].strip()),
        }
    elif 'Share Holding Percentage' in table_data[6].split("\r\n")[0]:        
        shareHoldings = {
            'date': table_data[6].split("\r\n")[1].strip('[as on (year ended)]'),
            'director': float(table_data[8].split("\r\n")[1].strip()),
            'govt': float(table_data[9].split("\r\n")[1].strip()),
            'institute': float(table_data[10].split("\r\n")[1].strip()),
            'foreign': float(table_data[11].split("\r\n")[1].strip()),
            'public': float(table_data[12].split("\r\n")[1].strip()),
        }  
    else:
        return
    
    old_data = mydb.fundamentals.find_one({ 'tradingCode': stock_code })

    if 'shareHoldingPercentage' in old_data:
        length = len(old_data['shareHoldingPercentage'])

        old_date = old_data['shareHoldingPercentage'][length-1]['date']
        new_date = shareHoldings['date']

        if old_date != new_date:
            mydb.fundamentals.update_one({ 'tradingCode': stock_code }, { '$push': { 'shareHoldingPercentage': shareHoldings } })
            print(stock_code, 'success')
        else:
            print(stock_code, 'data already exists')
    else:
        mydb.fundamentals.update_one({ 'tradingCode': stock_code }, { '$set': { 'shareHoldingPercentage': [ shareHoldings ] } })
        print(stock_code, 'success first entry')

for stock in stocks_list:
    shareholding_data(stock)