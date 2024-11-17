import pymongo, datetime, certifi, requests
from bs4 import BeautifulSoup
from variables import mongo_string, db_name
from data import stocks_list

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient[db_name]

data_setting = mydb.settings.find_one()

if data_setting['dataInsertionEnable'] == 0:
    print('exiting script')
    exit()

# stocks_list = ['BESTHLDNG', 'NRBBANK']

def reserve_data(stock_code):

    stock_url  = 'https://www.dsebd.org/displayCompany.php?name='+ stock_code
    response = requests.get(stock_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    page_data_array = soup.find_all('table', attrs={'class': 'table table-bordered background-white'})

    table_head = soup.find('div',attrs={'class':"col-sm-6 pull-right"}).text

    year_end = table_head.replace("For the year ended:",'').strip()

    table_data = []
    for row in page_data_array[2].find_all('td')[0:]:
        table_data.append(row.text.strip())

    reserve_surplus_value = float(table_data[4].replace(",", ''))

    mydb.fundamentals.update_one({ 'tradingCode': stock_code }, { '$set': { 'reserveSurplus': [{ "date": year_end, "value": reserve_surplus_value }] } })

    old_data = mydb.fundamentals.find_one({ 'tradingCode': stock_code })

    if 'reserveSurplus' in old_data:
        length = len(old_data['reserveSurplus'])
        old_value = old_data['reserveSurplus'][length-1]['value']

        if old_value != reserve_surplus_value:
            mydb.fundamentals.update_one({ 'tradingCode': stock_code }, { '$push': { 'reserveSurplus': { "date": year_end, "value": reserve_surplus_value } } })
            print(stock_code, 'success!')
        else:
            print(stock_code, 'data already exists')
    else:
        mydb.fundamentals.update_one({ 'tradingCode': stock_code }, { '$set': { 'reserveSurplus': [{ "date": year_end, "value": reserve_surplus_value }] } }) 
        print(stock_code, 'success! first load')  

for stock in stocks_list:
    reserve_data(stock)

mydb.data_script_logs.insert_one({
    'script': 'reserve-surplus-daily',
    'message': "Status: OK",
    'time': datetime.datetime.now()
})    

