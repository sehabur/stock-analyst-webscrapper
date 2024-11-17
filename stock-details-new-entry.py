import requests, pymongo, certifi
from bs4 import BeautifulSoup
from variables import mongo_string, db_name

stocks_list = ['TECHNODRUG']

def basic_data(stock_code):
    print(stock_code, 'start')
    stock_url  = 'https://www.dsebd.org/displayCompany.php?name='+ stock_code
    response = requests.get(stock_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    data = {}
    
    data['tradingCode'] = stock_code
    data['companyName'] = soup.find('h2', attrs={'class': 'BodyHead topBodyHead'}).find('i').text.strip()
    data['lastAgm'] = soup.find('h2', attrs={'class': "BodyHead topBodyHead row"}).find('i').text.strip()

    page_data_array = soup.find_all('table', attrs={'class': 'table table-bordered background-white'})

    for item in page_data_array[0]:
        item = str(item)
        x = item.find("Market Capitalization (mn)")
        if x != -1:
            data['marketCap'] = float(item.split('<td>')[2].split('</td>')[0].replace(",", ''))
    
    table_data = []
    for row in page_data_array[1].find_all('td')[0:8]:
        table_data.append(row.text.strip())

    data['authCap'] = table_data[0] if table_data[0] == '-' else float(table_data[0].replace(",", ''))
    data['debutTradingDate'] = "-" if table_data[1]== '' else table_data[1]
    data['paidUpCap'] = float(table_data[2].replace(",", ''))
    data['instrumentType'] = table_data[3]
    data['faceValue'] = float(table_data[4].replace(",", ''))
    data['marketLot'] = float(table_data[5].replace(",", ''))
    data['totalShares'] = float(table_data[6].replace(",", ''))
    data['sector'] = table_data[7].replace(",", '')

    table_data = []
    for row in page_data_array[2].find_all('td')[0:]:
        table_data.append(row.text.strip())

    data['rightIssue'] = table_data[2]
    data['yearEnd'] = table_data[3]
    data['oci'] = float(table_data[5].replace(",", ''))
    
    table_data = []
    for row in page_data_array[9].find_all('td')[0:]:
        table_data.append(row.text.strip())

    data['listingYear'] = table_data[1]
    data['category'] = table_data[3]

    shareHoldings = []

    if 'Share Holding Percentage' in table_data[6].split("\r\n")[0]:
        shareHoldings.append({
            'date': table_data[6].split("\r\n")[1].strip('[as on (year ended)]'),
            'director': float(table_data[8].split("\r\n")[1].strip()),
            'govt': float(table_data[9].split("\r\n")[1].strip()),
            'institute': float(table_data[10].split("\r\n")[1].strip()),
            'foreign': float(table_data[11].split("\r\n")[1].strip()),
            'public': float(table_data[12].split("\r\n")[1].strip()),          
        })
    if 'Share Holding Percentage' in table_data[13].split("\r\n")[0]:
        shareHoldings.append({
            'date': table_data[13].split("\r\n")[1].strip('[as on]'),
            'director': float(table_data[15].split("\r\n")[1].strip()),
            'govt': float(table_data[16].split("\r\n")[1].strip()),
            'institute': float(table_data[17].split("\r\n")[1].strip()),
            'foreign': float(table_data[18].split("\r\n")[1].strip()),
            'public': float(table_data[19].split("\r\n")[1].strip()),          
        })
    if 'Share Holding Percentage' in table_data[20].split("\r\n")[0]:
        shareHoldings.append({
            'date': table_data[20].split("\r\n")[1].strip('[as on]'),
            'director': float(table_data[22].split("\r\n")[1].strip()),
            'govt': float(table_data[23].split("\r\n")[1].strip()),
            'institute': float(table_data[24].split("\r\n")[1].strip()),
            'foreign': float(table_data[25].split("\r\n")[1].strip()),
            'public': float(table_data[26].split("\r\n")[1].strip()),        
        })

    data['shareHoldingPercentage'] = shareHoldings    

    table_data = []
    for row in page_data_array[10].find_all('td')[0:]:
        table_data.append(row.text.strip())
  
    data['shortTermLoan'] = float(table_data[5].replace(",", '')) 
    data['longTermLoan'] = float(table_data[7].replace(",", ''))

    table_data = []
    for row in page_data_array[11].find_all('td')[0:]:
        table_data.append(row.text.strip())

    data['address'] = {
        "headOffice": table_data[2],
        "contact": table_data[18],
        "email": table_data[10],
        "website": table_data[12]
    }
    data['isActive'] = True
    data['type'] = "stock"

    return data

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient[db_name]

for stock in stocks_list: 
    data_to_insert = basic_data(stock)
    mydb.fundamentals.insert_one(data_to_insert)
    print(stock, 'success')
    



