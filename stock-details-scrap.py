import requests, re
import requests, re
from bs4 import BeautifulSoup
import pandas as pd
import pymongo, datetime, certifi
from zoneinfo import ZoneInfo
from variables import mongo_string
from data import stocks_list

stocks_list_test = [
    'RAKCERAMIC',
    'STANCERAM', 
    'MONNOCERA',
    "ACFL",
    "ACMELAB", 
    ]
stocks_issue_cash = [
     "DBH",
     "MEGHNACEM", 
]
stocks_issue_nav = [
     "BDWELDING",
     "FAMILYTEX",
     "INTECH",
     "NURANI",
     "TUNGHAI",
]

def basic_data(stock_code):
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
    for row in page_data_array[2].find_all('td')[0:]:
        table_data.append(row.text.strip())
    stock_div_text = re.split('% |, |,|%| ',table_data[1])
    
    x=0
    stockDividend = []
    for i in range (int((len(stock_div_text))/2)):
        if stock_div_text[x].replace('.','',1).isdigit() == True and stock_div_text[x+1][:2] == '20' :
            stockDividend.append({
                'year' : stock_div_text[x+1],
                'value' : float(stock_div_text[x])
            })
        x=x+2

        

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

    cashDivText = re.split('% |%|, |,',table_data[0])

    x=0
    cashDivData = []
    for i in range (int((len(cashDivText))/2)):
        cashDivData.append({
            'year' : cashDivText[x+1],
            'value' : float(cashDivText[x])
        })
        x=x+2

    data['cashDividend'] = cashDivData

    data['stockDividend'] = table_data[1]
    data['rightIssue'] = table_data[2]
    data['yearEnd'] = table_data[3]
    data['reserveSurplusWithoutOci'] = float(table_data[4].replace(",", ''))
    data['oci'] = float(table_data[5].replace(",", ''))
    
    table_data = []
    financialYear = soup.find('h2', attrs={'class': "BodyHead topBodyHead page-break"}).find('i').text.strip()

    for row in page_data_array[3].find_all('td')[0:]:
        table_data.append(row.text)

    if (financialYear != ''):
        data['epsQuaterly'] = [{
            'year': int(financialYear),
            'q1': 0 if table_data [19] == '-' else float(table_data [19]),
            'q2': 0 if table_data [20] == '-' else float(table_data [20]),
            'q3': 0 if table_data [22] == '-' else float(table_data [22]),
            'annual': 0 if table_data [24] == '-' else float(table_data [24])
        }]
    

    table_data = []
    for row in page_data_array[6].find_all('td')[0:]:
        table_data.append(row.text)

    for i in range (len(table_data)):
        if 'Diluted\n' == table_data[i]:
            n = i
    del table_data [0:n+1]
    yearlyNAV = []
    yearlyEPS = []
    yearlyPCO = []
    yearlyProfit = []
    yearlyTCI = []
    p=0
    for y in range (int(len(table_data)/13)):
        yearlyNAV.append({
            'year': table_data[p],
            'value' : 0 if table_data[p+7] == '-' else float(table_data[p+7].replace(",", ''))
        })
        yearlyEPS.append({
            'year': table_data[p],
            'value' : 0 if table_data[p+4] == '-' else float(table_data[p+4].replace(",", ''))
        })
        yearlyPCO.append({
            'year': table_data[p],
            'value' : 0 if table_data[p+10] == '-' else float(table_data[p+10].replace(",", '').replace(" ", ''))
        })
        yearlyProfit.append({
            'year': table_data[p],
            'value' : 0 if table_data[p+11] == '-' else float(table_data[p+11].replace(",", '').replace(" ", ''))
        })
        yearlyTCI.append({
            'year': table_data[p],
            'value' : 0 if table_data[p+12] == '-' else float(table_data[p+12].replace(",", '').replace(" ", ''))
        })
        p=p+13
    
    data['navYearly'] = yearlyNAV
    data['epsYearly'] = yearlyEPS
    data['pcoYearly'] = yearlyPCO
    data['profitYearly'] = yearlyProfit
    data['tciYearly'] = yearlyTCI

    table_data = []
    for row in page_data_array[7].find_all('td')[0:]:
        table_data.append(row.text)

    for i in range (len(table_data)):
        if 'Restated\n' == table_data[i]:
            n = i
    del table_data [0:n+1]
    DividendYield = []
    p=0
    for y in range (int(len(table_data)/9)):
        DividendYield.append({
            'year': table_data[p],
            'value' : 0 if table_data[p+8] == '-' else float(table_data[p+8])
        })
        p=p+9

    data['dividendYield'] = DividendYield


    table_data = []
    for row in page_data_array[9].find_all('td')[0:]:
        table_data.append(row.text.strip())

    data['listingYear'] = table_data[1]
    data['category'] = table_data[3]
    data['shareHoldingPercentage'] = {
        'director': float(table_data[22].split("\r\n")[1].strip()),
        'govt': float(table_data[23].split("\r\n")[1].strip()),
        'institute': float(table_data[24].split("\r\n")[1].strip()),
        'foreign': float(table_data[25].split("\r\n")[1].strip()),
        'public': float(table_data[26].split("\r\n")[1].strip()),
    }


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

    data['lastUpdate'] = datetime.datetime.now(ZoneInfo('Asia/Dhaka'))

    return data


myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient["stockanalyst"]
mycol = mydb["fundamentals"]

for stock in stocks_list:
    data_to_insert = basic_data(stock)
    mycol.update_one({ 'tradingCode': stock }, { '$set': { 'stockDividend': data_to_insert } })
    print(stock, 'success')

# for stock in stocks: 
#     data_to_insert = basic_data(stock)
#     mycol.insert_one(data_to_insert)
#     print(stock, 'success')


# final_data = []

# for stock in stocks:
#     final_data.append(basic_data(stock))

# myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
# mydb = myclient["stockanalyst"]
# mycol = mydb["fundamentals_test"]

# mycol.insert_many(final_data)


