import pymongo, certifi, datetime, re
from data import stocks_list_details
from variables import mongo_string

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient["stockanalyst"]

data_setting = mydb.settings.find_one()

if data_setting['dataInsertionEnable'] == 0:
    print('exiting script as data insertion disabled')
    exit()

today_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

news_list = mydb.news.find({
    # 'date':   { '$gte':  datetime.datetime(2023, 11, 19, 0, 0) } ,
    'date': today_date,
    'title': { '$regex': 'Dividend Declaration$', '$options': 'i' } ,
}).sort("date", 1)

temp_data = {}

for news in news_list: 
    title = news['title'].split()
    id = news['tradingCode'] + news['date'].strftime('%d%m%Y')

    if id in temp_data:
        if temp_data[id]['description'].startswith("(Continuation news") or temp_data[id]['description'].startswith("(Cont. news"):
            temp_data[id]['description'] = news['description'] + temp_data[id]['description']
        else:
            temp_data[id]['description'] = temp_data[id]['description'] + news['description']  
    else:
        temp_data[id] = {
            'title': news['title'] + ' ' + news['date'].strftime('%d%m%Y'),
            'tradingCode': news['tradingCode'],
            'description': news['description'],
            'date': news['date']
        }

# for news in temp_data.values():
#     print(news)
# exit()        

for news in temp_data.values():
    news_date = news['date']
    description = re.split(" |,", news['description'])
    trading_code = news['tradingCode']
    # print(trading_code, 'start')
    
    # YEAR 
    n = -1
    for i in range (len(description)):
        if (description[i].lower() == 'year' or description[i].lower() == 'period') and description[i+1].lower() == 'ended':
            for j in range (i+2, i+10):
                if description[j][:3] == '202' or description[j][:3] == '201': 
                    n = j
                    break
            break
    if n != -1:
        year = (description[n]).replace(".", '').replace(";", '').replace(",", '')
    else:
        year = 'n/a'    
                   
            
    # Stock Dividend
    n = -1
    for i in range (len(description)):
        if description[i].lower() == 'recommended' or description[i].lower() == 'declared' or description[i].lower() == 'approved':
            for j in range (i+1,len(description)):
                if "dividend" == description [j].lower() :
                    for k in range (j,0,-1):
                        if "stock" == description[k].lower():                   
                            for l in range (k,0,-1):
                                if '%' == description[l][-1:] :
                                    n = l
                                    break
                            break
                    break
            break    

    if n != -1:       
        stock_dividend = float((description[n]).replace("%", ""))  
    else:
        stock_dividend = 'n/a'

    # Cash Dividend 
    n = -1 
    for i in range (len(description)):
        if description[i].lower() == 'recommended' or description[i].lower() == 'declared' or description[i].lower() == 'approved':
            for j in range (i+1,len(description)):
                if "dividend" == description[j].lower() :
                    for k in range (j,1,-1):
                        if "cash" == description[k].lower():                 
                            for l in range (k,1,-1):
                                if '%' == description[l].lower()[-1:] :
                                    n = l
                                    dividend = True
                                    break
                            break    
                        elif description[k].lower() == 'no': 
                            n = k    
                            dividend = False            
                            break
                    break
            break 
          
    if n != -1:      
        if dividend:
            cash_dividend = float((description[n]).replace("%", ""))  
        else:
            cash_dividend = 0   
    else:
        cash_dividend = 'n/a'   
               
    # AGM Date
    n=-1
    for i in range (len(description)):
        if "Date" == description [i] and "of" == description [i+1] :
            for j in range (i+2, len(description)):
                if description [j] == 'AGM:':
                    n=j+1
                    break
            break
 
    if n != -1:
        agm_date = description[n]
    else:
        agm_date = 'n/a'
    
    # Record Date #
    n=-1    
    for i in range (len(description)):
        if "record" == description[i].lower() and description[i+1].lower().replace(":", "") == "date" :
            for j in range (i+1, i+5):
                if description[j][:10][-4:-1] == '202':
                    n = j
                    break
            break    
 
    record_date_temp = description[n][:10] if n != -1 else None
    
    if record_date_temp:
        record_date_string =  record_date_temp.split(".")
        record_date = datetime.datetime(int(record_date_string[2]), int(record_date_string[1]), int(record_date_string[0]), 0, 0) 
    else:
        record_date = 'n/a'

    # EPS
    n=-1
    for i in range (len(description)):
        if "EPS" == description [i] :
            for j in range (i+2, len(description)):
                if description [j] == 'Tk.':
                    n=j+1
                    break
            break
    eps_string = description[n] if n != -1 else None 

    if eps_string:
        if ("(" in eps_string):
            eps = - float(eps_string.strip('()'))
        else:
            eps = float(eps_string) 
    else:
        eps = 'n/a'

    # NOCFPS #
    n=-1
    for i in range (len(description)):
        if "NOCFPS" == description [i] and 'of' == description [i+1] :
            for j in range (i+2, len(description)):
                if description [j] == 'Tk.':
                    n=j+1
                    break
            break

    nocfps_string = description [n] if n != -1 else None

    if nocfps_string: 
        if ("(" in nocfps_string):
            nocfps = - float(nocfps_string.strip('()'))
        else:
            nocfps = float(nocfps_string)  
    else: 
        nocfps = 'n/a'

    # NAV #
    n=-1    
    for i in range (len(description)):
        if "NAV" == description [i] and 'per' == description [i+1]:
            for j in range (i+2, len(description)):
                if description [j] == 'Tk.':
                    n=j+1
                    break
            break
    nav_string = (description [n]).replace(",", '') if n != -1 else None 

    if nav_string:
        if ("(" in nav_string):
            nav = - float(nav_string.strip('()'))
        else:
            nav = float(nav_string)
    else:
        nav = 'n/a'
 
    # print(news_date, trading_code, year, agm_date, record_date, eps, nav, nocfps, cash_dividend, stock_dividend)  
    
    data = mydb.fundamentals.find_one({ 'tradingCode': trading_code })  

    eps_q_data = data['epsQuaterly'] if 'epsQuaterly' in data else []
    nav_q_data = data['navQuaterly'] if 'navQuaterly' in data else []
    nocfps_q_data = data['nocfpsQuaterly'] if 'nocfpsQuaterly' in data else []

    eps_y_data = data['epsYearly'] if 'epsYearly' in data else []
    nav_y_data = data['navYearly'] if 'navYearly' in data else []
    nocfps_y_data = data['nocfpsYearly'] if 'nocfpsYearly' in data else []
    
    cash_dividend_y_data = data['cashDividend'] if 'cashDividend' in data else []
    stock_dividend_y_data = data['stockDividend'] if 'stockDividend' in data else []
    dividend_yield_y_data = data['dividendYield'] if 'dividendYield' in data else []
    
    
    if year != 'n/a':  
        
        # # EPS # #
        if eps != 'n/a':
            index = -1
            for i in range (len(eps_q_data)):
                if str(eps_q_data[i]['year']) == year:
                    index = i
                    break  
            
            if index != -1 and ('q3' in eps_q_data[index] and 'q2' in eps_q_data[index] and 'q1' in eps_q_data[index]):
                eps_q4 = round((eps - eps_q_data[index]['q3'] - eps_q_data[index]['q2'] - eps_q_data[index]['q1']), 2)
                eps_q_data[index]['q4'] = eps_q4

            index = -1
            for i in range (len(eps_y_data)):
                if str(eps_y_data[i]['year']) == year:
                    index = i
                    break  
            if index != -1:
                eps_y_data[index]['value'] = eps
            else:
                eps_y_data.append({
                    'year': year,
                    'value': eps
                }) 

        # # NAV # #
        if nav != 'n/a':
            index = -1
            for i in range (len(nav_q_data)):
                if nav_q_data[i]['year'] == year or nav_q_data[i]['year'] == int(year):
                    index = i
                    break  
            if index != -1:
                nav_q_data[index]['q4'] = nav
            else:
                nav_q_data.append({
                    'year': year,
                    'q4': nav
                })    

            index = -1
            for i in range (len(nav_y_data)):
                if nav_y_data[i]['year'] == year or nav_y_data[i]['year'] == int(year):
                    index = i
                    break  
            if index != -1:
                nav_y_data[index]['value'] = nav
            else:
                nav_y_data.append({
                    'year': year,
                    'value': nav
                })  

        # # NOCFPS # #
        if nocfps != 'n/a':
            index = -1
            for i in range (len(nocfps_q_data)):
                if nocfps_q_data[i]['year'] == year or nocfps_q_data[i]['year'] == int(year):
                    index = i
                    break  
            if index != -1:
                nocfps_q_data[index]['q4'] = nocfps
            else:
                nocfps_q_data.append({
                    'year': year,
                    'q4': nocfps
                })    

            index = -1
            for i in range (len(nocfps_y_data)):
                if nocfps_y_data[i]['year'] == year or nocfps_y_data[i]['year'] == int(year):
                    index = i
                    break  
            if index != -1:
                nocfps_y_data[index]['value'] = nocfps
            else:
                nocfps_y_data.append({
                    'year': year,
                    'value': nocfps
                })  
        
        # Stock dividend 
        if stock_dividend != 'n/a':
            index = -1
            for i in range (len(stock_dividend_y_data)):
                if stock_dividend_y_data[i]['year'] == year:
                    index = i
                    break  
            if index != -1:
                stock_dividend_y_data[index]['value'] = stock_dividend
            else:
                stock_dividend_y_data.append({
                    'year': year,
                    'value': stock_dividend
                })    
                
        # Cash dividend        
        if cash_dividend != 'n/a':
            index = -1
            for i in range (len(cash_dividend_y_data)):
                if cash_dividend_y_data[i]['year'] == year or cash_dividend_y_data[i]['year'] == int(year):
                    index = i
                    break  
            if index != -1:
                cash_dividend_y_data[index]['value'] = cash_dividend
            else:
                cash_dividend_y_data.append({
                    'year': year,
                    'value': cash_dividend
                })    
                            
            # Dividend Yield         
            index = -1
            
            fundamentals = mydb.fundamentals.find_one({'tradingCode': trading_code})
            
            if fundamentals['yearEnd'] ==  '30-Jun':
                day = 30
                month = 6
            elif fundamentals['yearEnd'] ==  '31-Dec':
                day = 31
                month = 12
            elif fundamentals['yearEnd'] ==  '30-Sep':
                day = 30
                month = 9
            elif fundamentals['yearEnd'] ==  "31-Mar":
                day = 31
                month = 3
                 
            daily_prices_list = mydb.daily_prices.find({'tradingCode': trading_code, 'date': { '$lte':  datetime.datetime(int(year), month, day, 0, 0) }}).sort("date", -1).limit(10)
            
            if len(list(daily_prices_list.clone())) > 0:
                daily_price = daily_prices_list[0]
                
                ltp = daily_price['ltp'] if daily_price['ltp'] != 0 else daily_price['ycp'] 
                dividend_yield = round(cash_dividend * 100 / (data['faceValue'] * ltp), 2)
                            
                for i in range (len(dividend_yield_y_data)):
                    if dividend_yield_y_data[i]['year'] == year or dividend_yield_y_data[i]['year'] == int(year):
                        index = i
                        break  
                if index != -1:
                    dividend_yield_y_data[index]['value'] = dividend_yield 
                else:
                    dividend_yield_y_data.append({
                        'year': year,
                        'value': dividend_yield
                    })                

    newvalues = {
        'epsQuaterly': eps_q_data,
        'navQuaterly': nav_q_data,
        'nocfpsQuaterly': nocfps_q_data,
        'epsYearly': eps_y_data,
        'navYearly': nav_y_data,
        'nocfpsYearly': nocfps_y_data,
        'cashDividend': cash_dividend_y_data,
        'stockDividend': stock_dividend_y_data,
        'dividendYield': dividend_yield_y_data,
        'lastAgm': agm_date,
        'recordDate': record_date,
    }

    # print(newvalues)
    # exit()

    mydb.fundamentals.update_one({ 'tradingCode': trading_code }, { '$set': newvalues })
    
